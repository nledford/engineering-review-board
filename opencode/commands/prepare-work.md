---
description: Classify a task and create the lightest appropriate execution approach
agent: engineering-lead
subtask: false
---

Assess this work request:

$ARGUMENTS

Read applicable project guidance and inspect enough repository evidence to classify the task as:

- Trivial — proceed directly when later requested
- Bounded — use a short in-session checklist
- Complex — create a durable plan under `docs/implementation-plans/`
- Ambiguous / High-Risk — ask the human whether or how to proceed

Do not implement the task in this command.

If a durable plan is warranted:

1. Select the minimum useful specialists and gather bounded analyses.
2. Delegate plan synthesis to `planning-coordinator`.
3. Ensure the new plan begins with `status: draft` and `review_decision: pending`.
4. Return the plan path and recommend `/review-plan <path>`.

Return the classification, rationale, evidence inspected, uncertainties, recommended process, and next command.
