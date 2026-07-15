---
description: Run a general or focused technical-debt audit through the Engineering Review Board
agent: engineering-review-board
subtask: false
---

Perform a technical-debt audit for:

$ARGUMENTS

Treat the argument as either repository-wide scope or a focused concern such as cyclomatic complexity, database debt, frontend state debt, test reliability, Project Fluent resources, concurrency, or documentation drift.

Include `technical-debt-auditor` as the central specialist and select only additional specialists whose evidence could materially change prioritization or remediation.

Return between 0 and 30 distinct, evidence-supported findings. Do not pad the
list and do not confuse active defects, acceptable trade-offs, or cosmetic
preferences with compounding technical debt. When no material debt is found,
say so explicitly and summarize the evidence examined.

For each finding include priority, severity, confidence, classification, scope, concrete evidence, impact, durable fix, validation, effort, expected benefit, and dependencies.

Do not modify the repository or a durable plan. Return findings for direct Lead
remediation when safe. When the human wants a durable remediation initiative,
recommend top-level `/create-plan`; `/start-work <existing-plan-path>` is only a
separate human-chosen execution of an existing plan.

Conclude with:

- Healthy
- Improvement Program Recommended
- Material Remediation Required
