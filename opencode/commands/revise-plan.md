---
description: Materially revise an implementation plan from ERB findings and return it for review
agent: engineering-lead
subtask: false
---

Revise the plan at `$1` using its latest persisted ERB review-history record. Do
not implement or approve it.

Re-read the plan, guidance, and exact review record. Stop if no matching persisted
review exists or a required human decision remains unresolved. Classify every finding as
accepted, accepted with modification, rejected by explicit human decision,
already addressed, requires clarification, or obsolete due to drift.

Invoke `planning-coordinator` for the only durable write. Preserve objective,
provenance, prior reviews, amendments, execution evidence, valid guardrails, and
non-goals. For every material change, increment `revision`, set `status: draft`,
set `review_decision: pending`, clear `reviewed_at`, `approved_at`, and
`approved_revision`, and append amendment/review history. Metadata-only updates
do not increment revision. Re-read the result, map each required finding to the
change, and return `/review-plan $1`.
