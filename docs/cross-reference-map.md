# Cross-Reference Map

This is a routing overlay for relationships between existing skills. It is not a
second inventory; keep full skill purposes, category boundaries, and coverage in
[`skill-taxonomy.md`](skill-taxonomy.md).

## Row Shape

Use one row per decision point where routing can involve more than one skill or a
validator-enforced relationship.

| Column | Meaning |
| --- | --- |
| Route | Short task surface or conflict being routed. |
| Primary skill | The first skill that owns the work. Use one primary unless the route is explicitly review-composed. |
| Related required skill(s) | Skills that must be loaded, linked, or handed off to for this route. Use `load:`, `link:`, or `handoff:` prefixes. |
| Optional companion skills | Skills to add only when local evidence matches their trigger. |
| Should-trigger examples | Short phrases that should activate the row. |
| Should-not-trigger examples | Near misses that should route elsewhere or avoid the row. |
| Validation source notes | Where enforcement or authority comes from: validator constant, taxonomy scenario, or skill frontmatter/body. |

Notation:

- `load:` agent routing requirement for the active task.
- `link:` repository validation expects a `SKILL.md` cross-link.
- `handoff:` use the named skill before reporting that class of finding.
- `—` means no required companion for the row; optional companions may still
  apply.

## Routing Matrix

### Security Routes

| Route | Primary skill | Related required skill(s) | Optional companion skills | Should-trigger examples | Should-not-trigger examples | Validation source notes |
| --- | --- | --- | --- | --- | --- | --- |
| Security-sensitive code review | `code-review` | load: `security-review`, `security-review-evidence`; link: validator-required security skills link both | Language/data review skills, `rust-code-review` | Auth, crypto, secrets, sessions, CORS/CSP/CSRF, OAuth, tokens, file paths, command execution, dependency trust | Design-only risk mapping before controls exist; supply-chain-only advisory review | Taxonomy security scenarios; `tools/skills_manager.py` `SECURITY_LINK_REQUIRED_SKILLS` + `REQUIRED_SECURITY_LINKS` warns on missing links |
| Trust-boundary design | `threat-modeling` | handoff: `security-review`, `security-review-evidence` for concrete implemented-control findings | BDD/TDD, architecture, language, data skills | New trust boundary, actor/asset/data-flow map, webhook, upload, tenant/admin distinction, abuse case | Ordinary code review; confirmed vulnerability validation; SBOM/CVE-only work | Taxonomy security boundaries and threat-modeling scenario |
| Dependency and supply-chain risk | `dependency-supply-chain-review` | load: `security-review`, `security-review-evidence` | Language package workflow skills, `justfiles`, CI/container review context | Manifest or lockfile risk, SBOM/SCA, CVE/GHSA, provenance, registry, install script, container/base image, vendored or generated code | Routine package-manager usage; third-party API docs lookup | Taxonomy dependency supply-chain scenario |

### Data Routes

| Route | Primary skill | Related required skill(s) | Optional companion skills | Should-trigger examples | Should-not-trigger examples | Validation source notes |
| --- | --- | --- | --- | --- | --- | --- |
| Database-neutral SQL | `sql-engineering` | load: matching engine skill when PostgreSQL or SQLite behavior matters | Language persistence skills, security review for data-access controls | SQL, schema, migration, transaction, index, view, function, trigger, query performance | ORM/package API usage with no SQL or schema behavior | Taxonomy database-neutral SQL escalation scenario |
| PostgreSQL-specific SQL | `postgresql-sql-engineering` | load: `sql-engineering` | `rust-persistence-sql`, language skills, `security-review` for RLS/privileges | JSONB, RLS, privileges, `EXPLAIN`, indexes, constraints, maintenance | SQLite behavior; Rust SQLx typing without database-native change | Taxonomy language/data boundaries |
| SQLite-specific SQL | `sqlite-sql-engineering` | load: `sql-engineering` | `rust-persistence-sql`, language test skills | PRAGMAs, WAL, locking, temporary DB tests, one-writer behavior, SQLite migrations | PostgreSQL-native features; using SQLite as proof for another engine | Taxonomy language/data boundaries |
| Rust database adapter work | `rust-persistence-sql` | load: engine data skill for database-native schema/query/index/security changes | `rust-engineering`, `rust-testing-quality`, `security-review` | SQLx macros/offline data, SeaQuery, pools, transactions, dynamic SQL, Rust repository adapter | Pure database DDL/query review with no Rust adapter concern | Taxonomy Rust and data boundaries |
| Randomness and identifiers | `random-data-identifiers` | load: `security-review` when randomness creates secrets, tokens, or security-sensitive IDs | Language/test skills, data skills | UUID/CUID/ULID choice, nonce, token, random filenames, seeded fixtures, collision risk | Fixed examples; database-native ID/index design without generated-value decision | Taxonomy randomness scenario |

### Language Routes

| Route | Primary skill | Related required skill(s) | Optional companion skills | Should-trigger examples | Should-not-trigger examples | Validation source notes |
| --- | --- | --- | --- | --- | --- | --- |
| Python implementation or workflow | `python-engineering` | link: `security-review`, `security-review-evidence`; load both when security-sensitive | `python-design-patterns`, `python-antipatterns`, `documentation-engineering`, data skills | Python source/tests, `pyproject.toml`, `uv.lock`, Ruff, typing, docstrings | Non-Python package managers; database-native schema-only work | Taxonomy Python boundary; validator security-link warnings |
| JavaScript or TypeScript implementation/workflow | `javascript-typescript-engineering` | link: `security-review`, `security-review-evidence`; load both when security-sensitive | `typescript-javascript-design-patterns`, `typescript-javascript-antipatterns`, `playwright-e2e`, `documentation-engineering`, data skills | JS/TS source, `package.json`, lockfiles, scripts, typecheck, lint, tests, build, dependencies | Checked-in Playwright spec design; Rust/Python/database-only work | Taxonomy JS/TS scenario; validator security-link warnings |
| Rust implementation | `rust-engineering` | link: `security-review`, `security-review-evidence`; load both when security-sensitive | `rust-testing-quality`, `rust-async-web`, `rust-persistence-sql`, `rust-design-patterns`, `rust-antipatterns` | Crates/modules/APIs, traits/generics, feature flags, errors, macros, refactors | Requested review with no implementation; database-only SQL work | Taxonomy Rust boundary; validator security-link warnings |
| Requested Rust review | `code-review` + `rust-code-review` | load: `review-verification-protocol`; load: security/data/async skills when their evidence appears | `rust-testing-quality`, `security-review`, `rust-persistence-sql`, `rust-async-web` | Review Rust PR/diff, ownership/API/async/persistence/unsafe concern | Implementing Rust changes without a review request | Taxonomy Rust review boundary; code-review evidence requirements |

## Validation Source Notes

Keep source notes terse and machine-updatable:

- `validator security-link warnings` means `tools/skills_manager.py validate`
  currently checks `SECURITY_LINK_REQUIRED_SKILLS` against
  `REQUIRED_SECURITY_LINKS` and emits warnings for missing first-party skill
  links. Extend that validator path for future required cross-skill links rather
  than adding a parallel warning system.
- `taxonomy ... scenario` points to executable acceptance criteria in
  `skill-taxonomy.md`.
- `taxonomy ... boundary` points to the boundary tables in `skill-taxonomy.md`.
- `skill frontmatter/body` should be used only when the route is not yet covered
  by taxonomy or validator rules.
