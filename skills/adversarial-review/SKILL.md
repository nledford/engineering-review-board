---
name: adversarial-review
description: Skeptically verify completed changes, agent work, merge readiness, and hidden regressions. Use after implementation when claims need independent proof; do not use as the primary implementation or ordinary code-review workflow.
---

# Adversarial Review Skill

Use this skill for an independent final challenge after implementation or a
primary review is complete. Always load
[`review-verification-protocol`](../review-verification-protocol/SKILL.md)
before reporting findings. For repository changes, also load
[`code-review`](../code-review/SKILL.md).

Do not use it to implement changes, debug an active unexplained failure, or
replace the first focused review of a diff.

## Workflow

1. Compare the request, acceptance criteria, diff, tests, documentation, and
   prior agent claims.
2. Re-run or independently inspect the strongest available evidence instead of
   accepting summaries at face value.
3. Challenge one plausible hidden failure mode, including invalid states,
   untested boundaries, scope creep, and regressions.
4. Report only findings supported by reproducible evidence. Distinguish blockers
   from follow-ups and explicitly clear disproved concerns.
5. Record skipped checks, assumptions, and residual risk before recommending a
   merge or handoff.

## Output

Return a merge recommendation with verified evidence, blockers, follow-ups,
skipped validation, and assumptions that still need proof.
