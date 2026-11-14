import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { after, test } from "node:test";
import feGate from "./fe-gate.ts";

type Handler = (event: unknown, ctx: unknown) => unknown;

interface Denial {
  block: boolean;
  reason: string;
}

interface ModificationView {
  texts: string[];
  isError: boolean;
}

interface EditEvent {
  type?: string;
  parentToolCallId?: string;
  toolName: string;
  input: { path: string; old_string?: string; new_string?: string };
}

const handlers: Record<string, Handler> = {};
feGate({
  on(event: string, handler: Handler) {
    handlers[event] = handler;
  },
});

const root = fs.mkdtempSync(path.join(os.tmpdir(), "fe-gate-test-"));
after(() => fs.rmSync(root, { recursive: true, force: true }));

function handlerFor(name: string): Handler {
  const handler = handlers[name];
  assert.ok(handler, `missing handler for ${name}`);
  return handler;
}

function makeCtx(entries: unknown[]): unknown {
  return { cwd: root, sessionManager: { getEntries: () => entries } };
}

function editEvent(filePath: string, oldString: string, newString: string): EditEvent {
  return { type: "tool_call", toolName: "edit", input: { path: filePath, old_string: oldString, new_string: newString } };
}

function readDenial(result: unknown): Denial | undefined {
  if (typeof result !== "object" || result === null) return undefined;
  if (!("block" in result) || !("reason" in result)) return undefined;
  if (result.block !== true || typeof result.reason !== "string") return undefined;
  return { block: true, reason: result.reason };
}

function readModification(result: unknown): ModificationView | undefined {
  if (typeof result !== "object" || result === null) return undefined;
  if (!("content" in result) || !Array.isArray(result.content)) return undefined;
  const texts: string[] = [];
  for (const block of result.content) {
    if (typeof block === "object" && block !== null && "text" in block && typeof block.text === "string") {
      texts.push(block.text);
    }
  }
  return { texts, isError: "isError" in result && result.isError === true };
}

const codeChange = ["const a = 1;", "const a = 2;"] as const;

test("allows a gated edit when the transcript has owner and decision", async () => {
  const entries = [
    { type: "message", message: { role: "user", content: "add a checkout button" } },
    {
      type: "message",
      message: { role: "assistant", content: [{ type: "text", text: "Runtime owner: X.tsx\nDecision: reuse" }] },
    },
  ];
  const result = await handlerFor("tool_call")(editEvent("src/X.tsx", ...codeChange), makeCtx(entries));
  assert.equal(result, undefined);
});

test("denies a gated edit when the transcript is empty", async () => {
  const result = await handlerFor("tool_call")(editEvent("src/X.tsx", ...codeChange), makeCtx([]));
  const denial = readDenial(result);
  assert.ok(denial, `expected a denial, got ${JSON.stringify(result)}`);
  assert.equal(denial.block, true);
  assert.match(denial.reason, /Runtime owner/);
});

test("passes files the gate does not cover", async () => {
  const result = await handlerFor("tool_call")(editEvent("notes.md", ...codeChange), makeCtx([]));
  assert.equal(result, undefined);
});

test("ignores tools outside the gate", async () => {
  const event = { type: "tool_call", toolName: "bash", input: { command: "ls" } };
  const result = await handlerFor("tool_call")(event, makeCtx([]));
  assert.equal(result, undefined);
});

test("ignores nested tool calls", async () => {
  const event = { ...editEvent("src/X.tsx", ...codeChange), parentToolCallId: "x/1" };
  const result = await handlerFor("tool_call")(event, makeCtx([]));
  assert.equal(result, undefined);
});

test("keeps the behaviorless one-line wording bypass", async () => {
  const result = await handlerFor("tool_call")(
    editEvent("src/Button.tsx", 'const label = "Submit";', 'const label = "Send";'),
    makeCtx([]),
  );
  assert.equal(result, undefined);
});

test("reports conflict markers left in the written file", async () => {
  const conflictPath = path.join(root, "Conflicted.tsx");
  fs.writeFileSync(
    conflictPath,
    "<<<<<<< HEAD\nconst a = 1;\n=======\nconst a = 2;\n>>>>>>> branch\n",
  );
  const event = {
    type: "tool_result",
    toolCallId: "r1",
    toolName: "edit",
    input: { path: conflictPath },
    content: [{ type: "text", text: "Successfully replaced 1 block(s)." }],
    isError: false,
  };
  const result = await handlerFor("tool_result")(event, makeCtx([]));
  const view = readModification(result);
  assert.ok(view, `expected a result modification, got ${JSON.stringify(result)}`);
  assert.match(view.texts[0] ?? "", /^Conflict markers remain/);
  assert.equal(view.isError, true);
  assert.ok(view.texts.includes("Successfully replaced 1 block(s)."), "keeps the tool's own result");
});

test("leaves a clean written file untouched", async () => {
  const cleanPath = path.join(root, "Clean.tsx");
  fs.writeFileSync(cleanPath, "export const A = () => null;\n");
  const event = {
    type: "tool_result",
    toolCallId: "r2",
    toolName: "write",
    input: { path: cleanPath, content: "export const A = () => null;\n" },
    content: [],
    isError: false,
  };
  const result = await handlerFor("tool_result")(event, makeCtx([]));
  assert.equal(result, undefined);
});
