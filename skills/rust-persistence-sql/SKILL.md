---
name: rust-persistence-sql
description: Rust persistence and SQLx guidance. Use when adding, changing, reviewing, or testing SQLx queries/macros, Rust database adapters, pools, transactions, offline query metadata, migrations invoked from Rust, SQLite support, database-backed Rust tests, or persistence boundaries. Use postgresql-sql-engineering for database-native PostgreSQL or general SQL design.
---

# Rust Persistence And SQLx

Use this skill for database-backed Rust work. Keep persistence adapters explicit,
keep core domain rules independent of database mechanics where practical, and
validate both Rust types and database behavior. For language-independent
PostgreSQL schema, SQL, query-plan, security, and migration design, use
[`postgresql-sql-engineering`](../postgresql-sql-engineering/SKILL.md).

## Workflow

1. Inspect the persistence setup: `Cargo.toml` SQLx features, migrations,
   `DATABASE_URL` conventions, `.sqlx/` offline metadata, pool types,
   transaction helpers, repository recipes, seed/fixture strategy, and CI
   database services.
2. Model the boundary. Use DDD language for tables, aggregates, invariants, and
   repository/service responsibilities. Do not let query row shapes become the
   core domain model by accident.
3. When storage behavior changes, design SQL and migrations with the database
   skill first, then implement the Rust adapter.
4. Implement SQLx access with typed parameters, explicit result mapping, narrow
   transactions, and safe error conversion.
5. Test at the right layer: pure domain tests, SQLx integration tests against
   the target database, and end-to-end tests only for user-visible workflows.
6. Update SQLx offline query metadata or document why it is not used by the
   repo.

## SQLx Checklist

- Prefer compile-checked SQLx macros such as `query!` or `query_as!` when the
  query shape is static and the repository supports online or offline checking.
- Use dynamic SQL only when the shape is genuinely dynamic; bind values instead
  of formatting user input into SQL.
- Map nullable columns, database enums, time types, UUIDs, JSON, and numeric
  precision deliberately.
- Keep pool acquisition, transaction scope, and timeout behavior explicit.
- Convert database errors at the adapter edge. Preserve enough context for logs
  while returning safe domain or API errors.
- For PostgreSQL and SQLite support in one codebase, test both. SQL dialects,
  type affinity, locking, migrations, and constraint behavior differ.

Common commands:

```sh
sqlx migrate info
sqlx migrate run
sqlx migrate revert
cargo sqlx prepare
cargo sqlx prepare --check --workspace
SQLX_OFFLINE=true cargo check --workspace --all-targets
```

Adapt command names to the repository's SQLx CLI version and recipes. Some
projects use `cargo sqlx ...`; others install a standalone `sqlx` binary.

## Schema And Migration Review

- Database invariants live in the database skill; the Rust review checks that
  Rust types, query mappings, migrations, and domain errors line up with them.
- SQLx migrations are invoked through the repository's chosen workflow. Do not
  assume `sqlx migrate add/run/revert` is authoritative when the repo has a
  custom migration generator or schema source of truth.
- Rust migration code, embedded migrations, and startup migration hooks have a
  rollback and deployment story. Avoid surprise DDL on application boot unless
  that is explicit repository policy.
- Seed data and fixtures are deterministic, isolated, and safe for repeated test
  runs.

## SQLite Guidance

- Do not assume SQLite is a drop-in PostgreSQL substitute. Type affinity,
  locking, datetime handling, DDL support, and concurrency behavior differ.
- Ensure foreign keys are enabled when tests or application logic rely on them.
- Keep migrations compatible with SQLite's DDL limits, or isolate SQLite-specific
  migrations when the repository already supports multiple database backends.
- Use SQLite for local or embedded workflows when that is the product choice,
  not as proof that PostgreSQL-specific SQL is correct.

## SQL Review Checklist

- Queries select explicit columns and return only the data the caller needs.
- Predicates are sargable where possible and match available indexes.
- Pagination is stable under inserts/deletes; keyset pagination is considered
  for large ordered result sets.
- Joins preserve intended cardinality and do not accidentally multiply rows.
- `NULL` handling, collation, case sensitivity, timezone, and numeric precision
  are explicit where they affect behavior.
- Transactions cover exactly the consistency boundary and no more.
- User-controlled values are bound parameters, never interpolated SQL.
- Observability exists for slow queries, migration failures, and pool exhaustion
  when the repository has a logging/tracing pattern.
- For PostgreSQL-specific index, constraint, RLS, privilege, and query-plan
  review, load `postgresql-sql-engineering`.

## Testing And Acceptance Criteria

- Write a failing test or migration check before fixing a query bug when
  practical.
- Use BDD-style examples for user-visible persistence behavior, such as
  "Given an existing account, when a duplicate email is saved, then the caller
  receives a conflict and no partial write remains."
- Use integration tests against the database engine whose behavior matters.
- Verify migrations from an empty database and, when compatibility matters, from
  a representative previous schema.
- Run SQLx prepare/check commands after changing compile-checked queries,
  schema, or migrations.

## Anti-Patterns

- Treating application validation as a substitute for database constraints on
  critical invariants.
- Returning raw SQLx or driver errors through domain or HTTP APIs.
- Building SQL by string concatenation with user input.
- Adding indexes speculatively without a query and write-cost rationale.
- Hiding long transactions behind generic repository helpers.
- Claiming PostgreSQL behavior from SQLite-only tests, or the reverse.
