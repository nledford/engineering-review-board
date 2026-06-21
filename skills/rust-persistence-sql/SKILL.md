---
name: rust-persistence-sql
description: Rust persistence, SQLx, SQL, SQLite, and PostgreSQL guidance. Use when adding, changing, reviewing, or testing SQL, SQLx queries/macros, migrations, transactions, schema design, constraints, indexes, views, query plans, PostgreSQL behavior, SQLite behavior, database-backed Rust code, or persistence boundaries. Use rust-testing-quality for broader test lanes.
---

# Rust Persistence And SQL

Use this skill for database-backed Rust work. Keep SQL and persistence adapters
explicit, keep core domain rules independent of database mechanics where
practical, and validate both Rust types and database behavior.

## Workflow

1. Inspect the persistence setup: migrations, `DATABASE_URL` conventions,
   `.sqlx/` offline metadata, SQLx features, pool types, transaction helpers,
   repository recipes, seed/fixture strategy, and CI database services.
2. Model the boundary. Use DDD language for tables, aggregates, invariants, and
   repository/service responsibilities. Do not let query row shapes become the
   core domain model by accident.
3. Design schema and SQL first when storage behavior changes: constraints,
   indexes, transactions, backfill strategy, deploy order, and rollback story.
4. Implement SQLx access with typed parameters, explicit result mapping,
   narrow transactions, and safe error conversion.
5. Test at the right layer: pure domain tests, query/integration tests against
   the target database, and end-to-end tests only for user-visible workflows.
6. Update offline query metadata or document why it is not used by the repo.

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

- Tables have stable primary keys, meaningful foreign keys, `NOT NULL` where
  absence is not valid, and `CHECK`/`UNIQUE`/exclusion constraints for database
  invariants.
- Migrations are ordered for safe deployment. Expensive backfills, column
  rewrites, lock-heavy DDL, and incompatible app/schema transitions are called
  out.
- Indexes support real query predicates, joins, ordering, and uniqueness. Avoid
  indexes that duplicate existing access paths or slow writes without a query
  need.
- Views and materialized views have a refresh and ownership story. Do not hide
  security, performance, or staleness assumptions inside a view definition.
- Seed data and fixtures are deterministic and safe for repeated test runs.

## PostgreSQL Guidance

- Use PostgreSQL constraints to protect invariants that must hold regardless of
  application path.
- Choose indexes intentionally: B-tree for general equality/range/order, GIN for
  containment/search-like structures, GiST/SP-GiST/BRIN only when the data and
  query pattern justify them, partial indexes for selective predicates, and
  expression indexes only when query expressions match.
- Review query plans with `EXPLAIN` and, when safe, `EXPLAIN ANALYZE`. Avoid
  running mutating or expensive analysis against shared environments.
- Transactions should name isolation assumptions, lock ordering, retry behavior,
  and deadlock risk when concurrent writes matter.
- Use `TIMESTAMPTZ`-style semantics for instants unless the domain truly needs a
  local date/time without timezone. Be explicit about precision and clock
  source.
- `CREATE INDEX CONCURRENTLY` and similar PostgreSQL operations have transaction
  restrictions; verify the migration tool supports the required mode.

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
