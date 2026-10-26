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
- Red flags: a copied function with one changed line; a constant declared again under another name; a wrapper around one call.

## Architecture

- Imports go one way: page → feature → shared or domain → adapter. Search the imports of each file for another feature folder. A list screen that imports the constants of one feature is a finding.
- Each responsibility has one owner: fetching in hooks, wire shape in schemas, transport in services, display in components. A component that calls the HTTP client is a finding.
- A change to shared code sits behind an opt-in that only the new caller uses. Check one other caller after the change.
- After the change, search each removed or replaced export. An export with no caller is a finding. A helper file with one consumer belongs in the file that owns its data.
- A project rule that names a component for this case wins over the nearest example. A document that disagrees with the code is a finding on the document.

## Operational flow

Write the states of the screen or action before you judge it, for example `idle → submitting → running → done | failed | cancelled`. For each transition, answer:

- What starts it, what ends it, and what the user sees.
- Double submit: can the user start it twice? Name what blocks it.
- A late reply: a reply that arrives after the user left or started again. Is it dropped?
- Reload, back, forward, and a deep link: does each one show the same state? Does the URL hold what must survive a reload?
- Unmount: timers, polling, and subscriptions stop.
- Long work: who ends a run that hangs, the client or the server? A client timeout is longer than the server limit, so the client does not give up on work the server still does.
- Polling stops when the run ends, when a poll fails, and when the screen unmounts.
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
- A new screen of the same kind: it reuses the hook, the shell, and the schema helper. It does not copy them.
- Each client map that mirrors a server enum (labels, colors, message codes) breaks when the server adds a value. Prefer labels from the server. Keep a fallback for an unknown value.
- A hard-coded list of server identifiers in the client is a finding unless the server cannot send them.
- An unknown value goes to a default branch. It does not crash.
