---
description: Execute a lifecycle-valid approved plan through bounded implementation-worker units
agent: engineering-lead
subtask: false
---

Execute the plan at:

$ARGUMENTS

Before edits, re-read the complete plan and applicable guidance. Stop unless all
of the following are true: status is `approved` or `in-progress`, or `blocked`
with a documented resolved blocker; `review_decision` is `ready`;
`approved_revision == revision`; a matching approval record exists; relevant
baseline assumptions are unchanged or explicitly re-reviewed; every exact
`depends_on` plan is `completed`; and no open decision, overlap, destructive
work, or scope expansion remains.

Translate only the approved sequence into non-overlapping bounded Tasks for
`implementation-worker`—never `general`. Preserve guardrails and non-goals,
integrate output, and validate observed results. Route every durable lifecycle
and execution-record update (including `in-progress`, `blocked`, or `completed`)
through `planning-coordinator`; do not edit the plan directly. Material deviation
requires `/revise-plan`, then ERB review and explicit `/approve-plan` again.

Return acceptance-criteria evidence, worker IDs and ownership, validation,
skipped checks, deviations, residual risk, and `/review-implementation <path>`.
