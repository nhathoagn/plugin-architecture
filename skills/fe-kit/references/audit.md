# Senior Audit

Read this file when a playbook names it.

Look at the code as the tech lead who will own it for the next two years. The question is not "does it work". The question is "what does it cost later". Each lens below came from a review where working code was still rejected.

Project rules win. When the repo has its own architecture or error rules, follow them and treat this file as the fallback.

## How to run it

- Scope is the Code Quality sweep scope, plus the hooks, services, and schemas those files import. List each path.
- Write one row for each lens, from Reuse through Extension. Copy the lens name. A missing row means the audit is not done.
- A row names the search or the trace you ran. A `clean` row with no search is not a verdict.
- A finding names `file:line`, a severity, and the cost if it stays.
- Severity:
  - `high`: wrong data, lost user work, a security gap, or a load problem in production.
  - `medium`: a second path for one rule, a drift between two copies, or a cost on the next change.
  - `low`: readability only.
- "Cost if it stays" names the next change that gets harder: a new status, a new screen, a new field.

| Lens | Search or trace | Finding (`file:line`) | Severity | Cost if it stays |
|---|---|---|---|---|
| Reuse | | | | |
| Architecture | | | | |
| Operational flow | | | | |
| Error handling | | | | |
| Performance and load | | | | |
| Extension | | | | |

Fix an audit finding only when the task asks for it, or when you wrote it in this turn. Otherwise list it. For each `high` finding, name the first-fix owner and the canonical owner from `references/ownership.md`.

## Reuse

- Search by behavior, not by name. Does a component, hook, rule, or service already do this job?
- Search the literal values of each rule: a time such as `'23:59:59'`, a status number, a poll interval, a message code. Two declarations of one value are one finding.
- Find a second implementation of one flow: two progress watchers, two download paths, two error blocks. Record why they differ. A difference with no reason is a finding.
- A new shared abstraction needs two real consumers today. Name them.
- Find the exemplar screen: the one the project rules or the reviewer name, or the newest screen with the same flow (search, lock, submit). Compare the query hook, the cache options, the lock module, and the service with it, line by line. A difference with no recorded reason is a finding.
- A layout block rebuilt in the page (a label/value grid, a label column width, a cell class) when the shared form components already draw it is a finding. If the design needs a level the shared part lacks, add it to the shared part.
- Red flags: a copied function with one changed line; a constant declared again under another name; a wrapper around one call; a screen hook that wraps a shared hook.

## Architecture

- Imports go one way: page → feature → shared or domain → adapter. Search the imports of each file for another feature folder. A list screen that imports the constants of one feature is a finding.
- Each responsibility has one owner: fetching in hooks, wire shape in schemas, transport in services, display in components. A component that calls the HTTP client is a finding.
- A change to shared code sits behind an opt-in that only the new caller uses. Check one other caller after the change.
- New behavior added to existing UI sits behind one flag whose default is the old behavior, per `references/feature-isolation.md`. Grep for flag reads: one entry owner reads it. New logic interleaved into an existing file, or a flag with no owner and removal date, is a finding.
- After the change, search each removed or replaced export. An export with no caller is a finding. A helper file with one consumer belongs in the file that owns its data.
- A project rule that names a component for this case wins over the nearest example. A document that disagrees with the code is a finding on the document.

Judgement calls, not hard defects. In the spoken report say "có thể để sau". Check every bullet below against the scope: a true bullet with no sentence in the report is an incomplete audit. Do not write the English smell name. In the audit table the severity is `low`. A project rule that allows the shape wins. Skip a hit a linter already catches. Do not repeat a finding Names, Reuse, Form screens, or Extension already owns. Do not invent a type the repo does not have. Do not fix one of these unless the user asked to clean up the screen. A diff review does not score this list.

- The same few fields travel together through several calls. Use one existing type, or leave them.
- A string or number stands for a concept the repo already names with a type. Use that type.
- The same `if` or `switch` on one type appears in more than one file in the folder. Use one map. This bullet owns that finding even when the two functions are otherwise identical copies: one sentence, at `có thể để sau`. A picker that switches popups is a Form screens finding, not this one.
- A function reads another module's fields more than its own. Move it next to the file that owns those fields when the move stays inside the layer rules above, and name that target file in the report.
- A caller walks `a.b().c()` when one method on the first object would hide the walk.
- A component or function only forwards, and Reuse has not already flagged that wrapper. Call the target.
- A component or hook ignores most of what it extends. Use composition.
- One file changes for several unrelated reasons. That is two jobs in one file, `rules/modules.md`. Split it so each part changes for one reason. A file that is long but does one job stays whole.

## Operational flow

Write the states of the screen or action before you judge it, for example `idle → submitting → running → done | failed | cancelled`. For each transition, answer:

- What starts it, what ends it, and what the user sees.
- Double submit: can the user start it twice? Name what blocks it.
- A late reply: a reply that arrives after the user left or started again. Is it dropped?
- Reload, back, forward, and a deep link: does each one show the same state? Does the URL hold what must survive a reload?
- Unmount: timers, polling, and subscriptions stop.
- Long work: who ends a run that hangs, the client or the server? A client timeout is longer than the server limit, so the client does not give up on work the server still does.
- Polling stops when the run ends, when a poll fails, and when the screen unmounts.
- A query that opens a server session or a lock is not reused from cache on the next visit (`gcTime: 0`, no retry). A lock the screen holds is kept alive, and is released when the user leaves. Use the project's lock module, not a session id in the screen schema.
- Query options for one screen sit in one place. Do not split cache options between the query factory and a second options object.
- Red flags: an effect that copies navigation into state; a flag that is never reset; polling with no stop condition.

## Error handling

Name the one place that shows each class of failure:

| Class | Example | Expected handling |
|---|---|---|
| Input | a field rule fails | message at the field or in the form block; no request |
| Business | 409, 422 with codes | form block; the user can fix and try again |
| Auth | 401, 403 | the global handler: sign-in or the forbidden page |
| System | 5xx | one message, logged; the global handler or one screen block |
| Network or timeout | no response | a message that says to try again; no silent loop |
| Contract | the response does not match the schema | logged with the path; a general message |

- A `catch` that drops an error with no message, no log, and no comment is a finding.
- One class shows in one place. A screen that shows one class in two places is a finding.
- Each query and mutation that the screen owns has an explicit retry policy: a count, a backoff, or none.
- Messages come from one source: the message catalog or the server. The client does not write its own text for a message that the server also sends.
- One function classifies errors by status. A component that imports the HTTP client's error type or checks `status === 500` is a finding.
- An input error marks the field and goes to the form block. Text printed under one field, when the project shows it in the block, is a finding.
- Do not hide or override the form block title with a fixed value. A different title is a change request.

## Performance and load

`references/performance.md` covers render and bundle cost. This lens covers the load over time.

- Write the worst-case request rate: rows × polls per minute. A number, not "fine".
- Name who sets each poll interval, the server or the client. One interval has one constant.
- Polling in a hidden tab needs a reason.
- A poll reads a small snapshot when one exists, not the full record.
- A list has a cap on its result set. A long list is virtualized.

## Extension

Name the next likely change. Count the files it touches.

- A new status, mode, or type: one change at the owner (the server enum or one client map), not a search across the client.
- A new field: one change in the schema. Each hand-kept list it must also join (a mapping file, a date-field list, a field-order list) is a finding. A forgotten list loses the value with no error.
- A new screen of the same kind: it reuses the hook, the shell, and the schema helper. It does not copy them.
- Each client map that mirrors a server enum (labels, colors, message codes) breaks when the server adds a value. Prefer labels from the server. Keep a fallback for an unknown value.
- A hard-coded list of server identifiers in the client is a finding unless the server cannot send them.
- An unknown value goes to a default branch. It does not crash.
