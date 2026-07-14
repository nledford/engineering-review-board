---
description: Convert and revalidate a legacy Tapestry plan into the native implementation-plan format
agent: engineering-lead
subtask: false
---

Convert and revalidate the Tapestry plan at:

$ARGUMENTS

Do not implement it.

Required process:

1. Read the complete source plan and current project guidance.
2. Validate its file paths, symbols, behavior claims, dependencies, sequencing, acceptance criteria, and verification commands against the current repository.
3. Determine whether it has been partially implemented, superseded, or invalidated by repository drift.
4. Gather only the specialist input that could materially change the converted plan.
5. Delegate synthesis to `planning-coordinator`.
6. Write the result under `docs/implementation-plans/` using the current template.
7. Preserve provenance with `source_format: tapestry`, `source_plan`, conversion date, original baseline when known, and current baseline.
8. Keep `status: draft` and `review_decision: pending`.
9. Include `Conversion Notes` describing stale assumptions, completed work, and structural changes.

Return the source path, converted path, conversion type, major changes, open decisions, and recommendation to run `/review-plan`.
