---
description: Persist a matching read-only ERB plan review record through the Planning Coordinator
agent: engineering-lead
subtask: false
---

Persist the latest ERB review record for the plan at `$1`, using review evidence
at `$2` when the complete record is not present in the active context.

This command records review evidence; it does not approve or revise the plan.
Re-read the plan and the complete structured ERB record. Stop unless the record's
canonical `plan_path`, `plan_id`, `revision`, and `baseline_commit` exactly match
the current plan and its decision is `ready`, `ready-with-revisions`, or
`not-ready`. Stop for missing, partial, stale, conflicting, or self-authored
evidence.

Invoke `planning-coordinator` for the only durable write. It must append the
verbatim structured record to `ERB Review History`, set `review_decision` and
`reviewed_at` from that record, preserve prior history, and leave `revision` and
approval fields unchanged. Re-read the persisted record.

Return the matching evidence and exactly one next step:

- `ready` → `/approve-plan $1`
- `ready-with-revisions` or `not-ready` → `/revise-plan $1`
