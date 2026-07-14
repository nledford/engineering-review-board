---
description: Audit one or more implementation plans before execution
agent: engineering-review-board
subtask: false
---

Review the following implementation plan path or paths before execution:

$ARGUMENTS

Operate as the Engineering Review Board.

Inspect the plans and current repository evidence. Determine whether the plans are correctly scoped, technically sound, sufficiently evidenced, properly sequenced, safely constrained, testable, and execution-ready. For multiple plans, also identify cross-plan conflicts, dependencies, duplicated work, and required ordering.

Select the minimum sufficient registered specialists. Do not modify source code or plan files.

Return Board summary, specialist coverage, strengths, omissions, sequencing issues, weak acceptance criteria, missing guardrails, missing verification, required revisions, residual risk, and one decision for each plan:

- Ready
- Ready With Revisions
- Not Ready
