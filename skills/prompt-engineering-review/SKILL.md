---
name: prompt-engineering-review
description: Review and improve prompts for Codex, OpenCode, Weave, Claude, and other coding agents. Use for prompt audits, rewrites, acceptance criteria, and agent instruction quality; do not use for application implementation or reusable SKILL.md authoring.
---

# Prompt Engineering Review Skill

Use this skill to review or rewrite a task prompt, system prompt, agent role, or
delegation instruction. Use
[`create-agent-skill`](../create-agent-skill/SKILL.md) instead when creating or
maintaining a reusable `SKILL.md` contract.

Do not use it to implement the task described by the prompt unless the user also
requests implementation.

## Workflow

1. Identify the intended agent, objective, inputs, scope, non-goals,
   deliverables, autonomy, and success criteria.
2. Find ambiguity, contradiction, missing context, unsafe authority, and
   instructions that cannot be verified.
3. Add sequencing only where order matters, and require repository or external
   evidence instead of invented context.
4. Specify editing boundaries, testing expectations, acceptance criteria,
   failure reporting, and escalation conditions when relevant.
5. Remove duplicated policy and unnecessary verbosity. Preserve the user's
   intent and state assumptions that remain unresolved.

## Output

Return prioritized issues, their likely effect on agent behavior, a polished
Markdown prompt, and any assumptions that still require confirmation.
