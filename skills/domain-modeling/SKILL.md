---
name: domain-modeling
description: Review tactical DDD models, aggregates, entities, value objects, invariants, domain services, and ubiquitous language. Use for a focused audit of an existing domain model; do not use to design a new model or force DDD onto simple data-centric work.
---

# Domain Modeling Skill

Use this skill as a tactical domain-model review lens. For repository change
reviews, also load [`code-review`](../code-review/SKILL.md) and
[`review-verification-protocol`](../review-verification-protocol/SKILL.md).

Use [`domain-driven-design`](../domain-driven-design/SKILL.md) when the primary
task is discovering or implementing a model rather than reviewing one.

## Workflow

1. Identify the bounded context, ubiquitous language, business rules, and
   lifecycle boundaries represented by the code.
2. Review entities, value objects, aggregates, repositories, services, and
   events against those rules rather than against pattern names alone.
3. Verify consistency boundaries, ownership, identity, state transitions, and
   whether domain APIs protect invariants.
4. Look for primitive obsession, anemic behavior, invalid intermediate states,
   and DTO, framework, or persistence leakage.
5. Confirm that suggested modeling complexity is justified. Record missing
   evidence, skipped validation, and residual domain risk.

## Output

Map verified issues to domain concepts, affected files, business risk, the
smallest useful refactor, skipped validation, and residual risk.
