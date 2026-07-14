---
description: Execute an approved implementation plan through the Engineering Lead
agent: engineering-lead
subtask: false
---

Execute the implementation plan at:

$ARGUMENTS

Before editing:

1. Read the whole plan and applicable project guidance.
2. Confirm its status is `approved`, `in-progress`, or `blocked` with a resolved blocker.
3. Stop if it is `draft`, `under-review`, `superseded`, `abandoned`, or `completed`.
4. Compare its baseline and assumptions with the current repository.
5. Stop for material drift, unresolved decisions, unsafe overlap, unauthorized destructive work, or required scope expansion.
6. Translate the approved sequence into bounded work units.

Implement the approved scope only. Preserve guardrails and non-goals. Delegate only independent, bounded work units to `implementation-worker` or native `general`; prevent overlapping edits and unstable interface assumptions. Integrate and validate all worker output yourself.

Do not silently rewrite approved objectives, guardrails, or acceptance criteria. Stop and propose a formal amendment when material deviation is necessary.

At completion, update only lifecycle and execution-record sections of the plan, map acceptance criteria to evidence, report observed validation results, skipped checks, deviations, residual risk, and recommend `/review-implementation <plan-path>`.
