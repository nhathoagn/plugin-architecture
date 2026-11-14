import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

type GateOutcome =
  | { kind: "pass" }
  | { kind: "deny"; reason: string }
  | { kind: "post-error"; text: string }
  | { kind: "post-note"; text: string };

interface ExtensionAPI {
  on(event: "tool_call" | "tool_result", handler: (event: GateEvent, ctx: GateCtx) => unknown): void;
}

interface GateCtx {
  cwd?: string;
  sessionManager?: { getEntries?: () => unknown };
}

interface GateEvent {
  type?: string;
  parentToolCallId?: string;
  toolName?: string;
  input?: unknown;
  content?: unknown;
  structuredContent?: unknown;
}

interface GatePayload {
  hook_event_name: "PreToolUse" | "PostToolUse";
  tool_name?: string;
  tool_input: Record<string, string>;
  cwd: string;
  transcript_path: string;
}

interface ResultModification {
  content: unknown[];
  isError?: boolean;
  structuredContent?: unknown;
}

interface GateHookOutput {
  permissionDecision?: unknown;
  permissionDecisionReason?: unknown;
  additionalContext?: unknown;
}

const GATE_SCRIPT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "scripts", "fe-gate.sh");
const GATE_TIMEOUT_MS = 10_000;

function contentBlocks(content: unknown, role: unknown): Record<string, unknown>[] {
  if (typeof content === "string") {
    return content ? [{ type: "text", text: content }] : [];
  }
  if (!Array.isArray(content)) return [];
  const blocks: Record<string, unknown>[] = [];
  for (const raw of content) {
    if (typeof raw !== "object" || raw === null || !("type" in raw)) continue;
    const kind: unknown = raw.type;
    if (kind === "text" && "text" in raw && typeof raw.text === "string") {
      blocks.push({ type: "text", text: raw.text });
    } else if (role === "assistant" && kind === "thinking" && "thinking" in raw && typeof raw.thinking === "string") {
      blocks.push({ type: "thinking", thinking: raw.thinking });
    }
  }
  return blocks;
}

function mapTranscript(entries: unknown): string {
  if (!Array.isArray(entries)) return "";
  const lines: string[] = [];
  for (const raw of entries) {
    if (typeof raw !== "object" || raw === null) continue;
    if (!("type" in raw) || !("message" in raw)) continue;
    if (raw.type !== "message") continue;
    const message: unknown = raw.message;
    if (typeof message !== "object" || message === null) continue;
    if (!("role" in message) || !("content" in message)) continue;
    if (message.role !== "user" && message.role !== "assistant") continue;
    const blocks = contentBlocks(message.content, message.role);
    if (blocks.length > 0) {
      lines.push(JSON.stringify({ type: message.role, message: { content: blocks } }));
    }
  }
  return lines.length > 0 ? lines.join("\n") + "\n" : "";
}

function filePaths(input: unknown): string[] {
  const out: string[] = [];
  if (typeof input !== "object" || input === null) return out;
  if ("paths" in input && Array.isArray(input.paths)) {
    for (const filePath of input.paths) {
      if (typeof filePath === "string" && filePath) out.push(filePath);
    }
  }
  if (out.length === 0 && "path" in input && typeof input.path === "string" && input.path) {
    out.push(input.path);
  }
  return out;
}

function postPayload(filePath: string, cwd: string, transcriptPath: string): GatePayload {
  return {
    hook_event_name: "PostToolUse",
    tool_input: { file_path: filePath },
    cwd,
    transcript_path: transcriptPath,
  };
}

function prePayload(
  claudeName: string,
  toolInput: Record<string, string>,
  cwd: string,
  transcriptPath: string,
): GatePayload {
  return {
    hook_event_name: "PreToolUse",
    tool_name: claudeName,
    tool_input: toolInput,
    cwd,
    transcript_path: transcriptPath,
  };
}

function toPayload(event: GateEvent, ctx: GateCtx, transcriptPath: string): GatePayload[] {
  const cwd = typeof ctx.cwd === "string" ? ctx.cwd : "";
  const pre = event.type === "tool_call";
  const paths = filePaths(event.input);

  if (event.toolName === "edit") {
    const filePath = paths[0];
    if (filePath === undefined) return [];
    if (!pre) return [postPayload(filePath, cwd, transcriptPath)];
    const input: unknown = event.input;
    if (
      typeof input === "object" && input !== null
      && "old_string" in input && typeof input.old_string === "string"
      && "new_string" in input && typeof input.new_string === "string"
    ) {
      return [
        prePayload(
          "Edit",
          { file_path: filePath, old_string: input.old_string, new_string: input.new_string },
          cwd,
          transcriptPath,
        ),
      ];
    }
    return [prePayload("MultiEdit", { file_path: filePath }, cwd, transcriptPath)];
  }

  if (event.toolName === "write" || event.toolName === "ast_edit") {
    const claudeName = event.toolName === "write" ? "Write" : "MultiEdit";
    return paths.map((filePath): GatePayload => (pre
      ? prePayload(claudeName, { file_path: filePath }, cwd, transcriptPath)
      : postPayload(filePath, cwd, transcriptPath)));
  }

  return [];
}

function parseHookOutput(stdout: string): GateHookOutput | undefined {
  let parsed: unknown;
  try {
    parsed = JSON.parse(stdout);
  } catch {
    // Unparseable gate output fails open.
    return undefined;
  }
  if (typeof parsed !== "object" || parsed === null) return undefined;
  if (!("hookSpecificOutput" in parsed)) return undefined;
  const body: unknown = parsed.hookSpecificOutput;
  if (typeof body !== "object" || body === null) return undefined;
  const output: GateHookOutput = {};
  if ("permissionDecision" in body) output.permissionDecision = body.permissionDecision;
  if ("permissionDecisionReason" in body) output.permissionDecisionReason = body.permissionDecisionReason;
  if ("additionalContext" in body) output.additionalContext = body.additionalContext;
  return output;
}

function parseOutcome(payload: GatePayload, code: number | null, stdout: string, stderr: string): GateOutcome {
  if (payload.hook_event_name === "PostToolUse") {
    if (code === 2 && stderr.trim()) return { kind: "post-error", text: stderr.trim() };
    if (code === 0) {
      const note = parseHookOutput(stdout)?.additionalContext;
      if (typeof note === "string" && note) return { kind: "post-note", text: note };
    }
    return { kind: "pass" };
  }
  if (code === 0) {
    const output = parseHookOutput(stdout);
    if (output?.permissionDecision === "deny") {
      const reason = output.permissionDecisionReason;
      if (typeof reason === "string" && reason) return { kind: "deny", reason };
    }
  }
  return { kind: "pass" };
}

function runGate(payload: GatePayload): Promise<GateOutcome> {
  const { promise, resolve } = Promise.withResolvers<GateOutcome>();
  const child = spawn(GATE_SCRIPT, { stdio: ["pipe", "pipe", "pipe"] });
  let settled = false;
  // Fail open: a gate that never answers must not block the session.
  const timer = setTimeout(() => {
    child.kill();
    settle({ kind: "pass" });
  }, GATE_TIMEOUT_MS);
  const settle = (outcome: GateOutcome): void => {
    if (settled) return;
    settled = true;
    clearTimeout(timer);
    resolve(outcome);
  };
  let stdout = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk: string) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk: string) => {
    stderr += chunk;
  });
  child.on("error", () => settle({ kind: "pass" }));
  child.on("close", (code) => settle(parseOutcome(payload, code, stdout, stderr)));
  // A gate that exits before reading stdin breaks the pipe; close still fires.
  child.stdin.on("error", () => {});
  child.stdin.end(JSON.stringify(payload));
  return promise;
}

async function withTranscript<T>(ctx: GateCtx, run: (transcriptPath: string) => Promise<T>): Promise<T> {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "fe-gate-"));
  try {
    const transcriptPath = path.join(dir, "session.jsonl");
    let entries: unknown;
    try {
      entries = ctx.sessionManager?.getEntries?.();
    } catch {
      entries = undefined;
    }
    fs.writeFileSync(transcriptPath, mapTranscript(entries));
    return await run(transcriptPath);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

function skipEvent(event: GateEvent): boolean {
  if (event.parentToolCallId) return true;
  return event.toolName !== "edit" && event.toolName !== "write" && event.toolName !== "ast_edit";
}

async function handleToolCall(
  event: GateEvent,
  ctx: GateCtx,
): Promise<{ block: boolean; reason: string } | undefined> {
  if (skipEvent(event)) return undefined;
  try {
    return await withTranscript(ctx, async (transcriptPath) => {
      for (const payload of toPayload(event, ctx, transcriptPath)) {
        const outcome = await runGate(payload);
        if (outcome.kind === "deny") return { block: true, reason: outcome.reason };
      }
      return undefined;
    });
  } catch {
    // Fail open: a broken gate never blocks the edit.
    return undefined;
  }
}

function resultModification(event: GateEvent, text: string, isError: boolean): ResultModification {
  const original: unknown[] = Array.isArray(event.content) ? event.content : [];
  const block = { type: "text", text };
  const modification: ResultModification = {
    content: isError ? [block, ...original] : [...original, block],
  };
  if (isError) modification.isError = true;
  if (event.structuredContent !== undefined) modification.structuredContent = event.structuredContent;
  return modification;
}

async function handleToolResult(event: GateEvent, ctx: GateCtx): Promise<ResultModification | undefined> {
  if (skipEvent(event)) return undefined;
  try {
    return await withTranscript(ctx, async (transcriptPath) => {
      let note: string | undefined;
      for (const payload of toPayload(event, ctx, transcriptPath)) {
        const outcome = await runGate(payload);
        if (outcome.kind === "post-error") return resultModification(event, outcome.text, true);
        if (outcome.kind === "post-note" && note === undefined) note = outcome.text;
      }
      return note === undefined ? undefined : resultModification(event, note, false);
    });
  } catch {
    // Fail open: a broken gate never rewrites the result.
    return undefined;
  }
}

export default function (pi: ExtensionAPI): void {
  pi.on("tool_call", handleToolCall);
  pi.on("tool_result", handleToolResult);
}
