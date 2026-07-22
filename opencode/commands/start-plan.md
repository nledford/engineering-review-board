---
description: Execute or resume an existing lean implementation plan
agent: plan-orchestrator
subtask: false
---

You are handling this current command turn as the Plan Orchestrator. Earlier
Engineering Review Board or Engineering Lead output, when present, was authored
by a different primary agent and is context only; it does not transfer their
identity or permissions to this turn.

Never claim that the Engineering Review Board or Engineering Lead is selected,
and never ask the human to select the Plan Orchestrator while this command is
running. Before refusing on role-authority grounds, reconcile the request against
the active Plan Orchestrator contract.

This invocation is the human's current request to execute or resume an existing
plan under the Plan Orchestrator contract, subject to the path, state, and
lifecycle validation below.

Use syntax `/start-plan [<plan-path>] [instructions]` to execute or resume an
existing canonical lean plan. `/start-plan` accepts only an explicit existing
canonical lean plan path or a no-argument state pointer. It rejects free-form new
requests and immutable legacy inputs. It does not create, succeed, convert, or
conversationally update plans. Direct human-authorized plan creation to
`/create-plan` and an in-place active-plan amendment to
`/update-plan <exact-plan-path>`.

The only durable workflow state is `.erb/plan-state.json`, with exactly this
shape and no additional fields:

```json
{"plan_path":".erb/plans/<path>.md"}
```

The exact schema is `{"plan_path":".erb/plans/<path>.md"}`.

Treat `plan_path` as untrusted input. It must be a repository-relative canonical
path matching either `.erb/plans/<slug>.md` or
`.erb/plans/<subject>/<NN>-<slug>.md`; reject absolute paths, traversal,
symlinks, non-regular files, alternate roots, and any path outside the current
repository. Accept exactly 1 MiB and reject limit-plus-one data for both the
state file and selected plan.

When the human supplies a path, validate that plan first, then write the exact
canonical path to `.erb/plan-state.json` and re-read both files before any
execution mutation. An explicit valid path replaces missing, invalid, or stale
state. Without an explicit path, read the state file and validate its exact
schema and selected plan. Without an explicit path, missing, invalid, or stale
state requires an explicit plan path; explain the issue and stop without
implementation.

The plan body must match the canonical lean template: exact ordered headings,
fixed Context labels, at least one numbered TODO checkbox, and at least one
numbered Verification checkbox. Display the resolved canonical path and its
checked and unchecked numbered TODOs and dedicated Verification checkboxes.

Derive lifecycle state from the plan body, never from fields in the state file:

- Active means at least one unchecked TODO or Verification checkbox remains.
- The current step is the first unchecked checkbox in document order.
- Complete means every TODO and Verification checkbox is checked.

If complete, say exactly: `This plan has already been implemented.` Then stop.
Do not delegate, implement, validate again, rewrite state, or mutate checkboxes.
Leave the state pointer selected so a later no-argument invocation reports the
same completed result.

If active, resume at the current step. Execute TODOs in document order before
dedicated Verification steps. Before each mutable phase, re-read the plan and
fresh worktree evidence. Active plan bodies remain immutable except for evidenced
`[ ]` to `[x]` checkbox advancement. A material plan-contract change leaves the
current checkbox unchecked and stops for a separate `/update-plan <exact-plan-path>`
request.

Delegate at most one Worker at a time. Keep the packet self-contained, preserve
TODO-before-Verification ordering, classify runtime permissions, and retain the
current checkbox until fresh evidence supports its complete obligation. A Worker
result is evidence, not checkbox authority. Directly observable evidence stays
with the Plan Orchestrator; otherwise use the shared `implementation` or
non-editing `verification` mode as directed by the Plan Orchestrator prompt.

Apply the Plan Orchestrator prompt's planned-work execution contract for effect
classification, liveness, finite waiting and starts, retry, correction, uncertain
results, evidence reconciliation, and checkbox decisions. This command supplies
only path/state/lifecycle routing and does not duplicate that transition policy.

The pointer selects a plan; it is not an exclusivity mechanism. The last valid
explicit selection wins. Never block because another plan is selected or may be
running. Do not attempt to detect, coordinate, serialize, or recover concurrent
plan execution.

Additional instructions may narrow validation or implementation choices, but
they may not change the selected plan body, skip unchecked steps, or expand the
Plan Orchestrator's authority.
