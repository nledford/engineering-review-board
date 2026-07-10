---
name: testing-strategy
description: Review test strategy, confidence gaps, TDD and BDD fit, flaky tests, boundary coverage, and suite maintainability. Use for a risk-focused audit of tests or test plans; do not use to write a single test, debug an active failure, or run a routine TDD loop.
---

# Testing Strategy Skill

Use this skill when the primary task is assessing whether a test suite or test
plan provides the right confidence. For repository change reviews, also load
[`code-review`](../code-review/SKILL.md) and
[`review-verification-protocol`](../review-verification-protocol/SKILL.md).

Use [`test-driven-development`](../test-driven-development/SKILL.md) for
Red-Green-Refactor implementation, and `systematic-debugging` for an active
unexplained test failure.

## Workflow

1. Identify the behaviors, contracts, invariants, risks, and failure modes the
   tests need to protect.
2. Map existing unit, integration, contract, end-to-end, property, and manual
   checks to those risks.
3. Find confidence gaps, redundant coverage, brittle implementation coupling,
   over-mocking, flakiness, unclear fixtures, and slow feedback paths.
4. Recommend the narrowest test level that proves each missing behavior,
   including boundary tests for architecture-critical constraints.
5. Validate claims with test code and runner evidence. Record skipped checks,
   environmental limitations, and residual quality risk.

## Output

Return prioritized findings and a risk-focused improvement plan with evidence,
recommended test levels, skipped validation, and residual risk.
