---
description: Independently review one or more canonical implementation plans before human approval
agent: engineering-review-board
subtask: false
---

Review these plan paths:

$ARGUMENTS

Operate as the read-only Engineering Review Board. Inspect each plan and current
repository evidence; select only critics that can materially change the decision.
Do not modify plans or source. Check canonical identity/path, revision, baseline,
authoritative `depends_on`, sequencing, scope, guardrails, open decisions,
acceptance criteria, and validation.

If a baseline predates the Board's exact permitted `HEAD`/`HEAD^` inspection
forms, require a supplied content-bearing baseline-to-current diff or equivalent
commit evidence. Without it, report the gap and do not return `ready`.

For every plan, return an independent structured review record containing exact
`plan_path`, `plan_id`, `revision`, `baseline_commit`, normalized `decision`
(`ready`, `ready-with-revisions`, or `not-ready`), `reviewed_at`, findings, and
`next_command`, which is always `/record-plan-review <path>` before any revision
or approval. A `ready` record is review evidence only; it is not approval.
For multi-plan reviews, identify cross-plan conflicts but do not collapse their
records. Return the Board summary, coverage, required actions, skipped
validation, residual risk, and one decision per plan.
