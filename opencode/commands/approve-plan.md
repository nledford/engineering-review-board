---
description: Record explicit human approval for an ERB-ready implementation plan
agent: engineering-lead
subtask: false
---

Approve the plan at `$1` using its latest persisted ERB review-history record.

This command is an explicit human authorization workflow, not agent
self-approval. Re-read the whole plan before acting. Stop unless the latest ERB
review record is `ready` and exactly matches the plan's canonical path,
`plan_id`, current `revision`, and `baseline_commit`. Stop for stale evidence,
open decisions, `not-ready`, `ready-with-revisions`, identity mismatch, baseline
drift, a record that was not persisted through `/record-plan-review`, or missing
evidence.

After explicit human authorization, invoke `planning-coordinator` to persist a
metadata-only approval update: `status: approved`, `review_decision: ready`,
`reviewed_at`, `approved_at`, and `approved_revision` equal to current revision,
plus a matching ERB review-history and approval record. This update must not
increment revision. Do not edit the plan directly.

Re-read the persisted plan and return the exact matching evidence, approval
record, updated metadata, and `/execute-plan $1` only when all execution
preconditions can be checked.
