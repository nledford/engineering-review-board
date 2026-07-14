---
description: Review completed work against its approved plan
agent: engineering-review-board
subtask: false
---

Review the completed implementation associated with:

$ARGUMENTS

Read the approved plan, current repository, referenced commits or diff, and supplied validation evidence.

Use `change-verifier` to map objectives, guardrails, non-goals, implementation steps, acceptance criteria, and required validation to concrete evidence. Select the minimum additional specialist panel for the actual change surface. Use `adversarial-reviewer` after the primary review when an independent hidden-flaw challenge materially improves confidence.

Do not modify the repository.

Return Board summary, baseline and scope, specialist coverage, requirement-to-evidence matrix, guardrail compliance, consolidated findings, validation evidence, skipped validation, residual risk, and one decision:

- Approve
- Approve With Follow-ups
- Request Changes
