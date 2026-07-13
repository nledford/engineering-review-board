---
name: architecture-review
description: Review architectural boundaries, dependency direction, ports and adapters, Clean/Onion/Hexagonal/DDD hybrids, and modular monolith structure. Use for architecture-focused audits of existing systems or changes; do not use for ordinary implementation or architecture design without a review request.
---

# Architecture Review Skill

Use this skill as an architecture-specific review lens for an existing system,
proposal, or diff. Always load
[`review-verification-protocol`](../review-verification-protocol/SKILL.md)
before reporting findings. For repository change reviews, also load
[`code-review`](../code-review/SKILL.md).

Do not use it for simple code changes with no boundary impact. Use the matching
Clean, Hexagonal, Onion, or DDD skill when the primary task is designing or
implementing an architecture rather than reviewing one.

## Workflow

1. Read project-local guidance, architecture docs, module structure, and the
   relevant diff before inferring the intended architecture.
2. Map dependency direction, module and bounded-context boundaries, ports,
   adapters, and framework or persistence edges.
3. Identify concrete leakage, cycles, misplaced policy, and boundary bypasses.
4. Distinguish intentional hybrid choices from accidental drift; prefer
   coherent, testable structure over pattern purity.
5. Verify findings against imports, call paths, tests, or build rules. Record
   skipped checks and residual architectural risk.

## Output

Return findings ordered by severity with file-level evidence, impact, the
smallest practical correction, skipped validation, and residual risk.
