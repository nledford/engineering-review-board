---
description: Convert and revalidate a legacy Tapestry plan into a canonical native plan
agent: engineering-lead
subtask: false
---

Convert `$1` into series `$2`.

`$1` is a legacy Tapestry source plan. `$2` must match
`[a-z][a-z0-9-]{1,19}`. Do not implement or approve the plan.

Read the complete source, current guidance, and repository evidence. Revalidate
paths, symbols, behavior, dependencies, sequencing, acceptance criteria, and
validation commands; identify assumptions that are current, stale, superseded,
implemented, or unverified. Delegate only the durable conversion to
`planning-coordinator`. The Coordinator allocates the canonical destination
`docs/implementation-plans/plans/<series>/<NN>-<slug>.md` using max+1 without
gap reuse from `01` through `99`, preserves `source_format: tapestry` and `source_plan`, and starts
`status: draft`, `review_decision: pending`, `revision: 1`.

Return source and destination paths, identity, provenance, revalidation results,
open decisions, skipped validation, and `/review-plan <destination>`.
