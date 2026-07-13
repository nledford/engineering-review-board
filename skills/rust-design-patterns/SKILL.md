---
name: rust-design-patterns
description: Rust design pattern and idiom guidance. Use when choosing, implementing, or reviewing Rust patterns such as newtypes, builders, RAII guards, traits, strategy, visitor, command, compose-structs, small crates, contained unsafe modules, custom traits for complex bounds, macros, or ownership-driven API design. Use rust-antipatterns for smell-focused audits and load rust-engineering whenever applying or implementing a pattern.
---

# Rust Design Patterns

Use this skill to choose idiomatic Rust patterns that solve a real design
problem. Rust patterns should exploit ownership, enums, traits, modules, and the
type system rather than copying object-oriented patterns from other languages.

## Use When

- A Rust API, crate boundary, module structure, domain type, trait, macro, or
  refactor needs an idiomatic pattern choice.
- The code has multiple real implementations, construction complexity,
  ownership/lifetime constraints, state transitions, or safety boundaries.
- A DDD, TDD, Clean, Hexagonal, or Onion design needs Rust-specific expression.
- Review comments or implementation plans mention pattern names or ask for a
  more idiomatic Rust design.

Do not use this skill to justify decorative abstractions. Use
[`rust-antipatterns`](../rust-antipatterns/SKILL.md) when the task is mainly to
find or remove generated-code smells. Advice-only pattern selection may use this
skill independently; load [`rust-engineering`](../rust-engineering/SKILL.md)
whenever applying or implementing the pattern.

## Selection Rules

1. Inspect existing crate/module conventions before naming a pattern.
2. Name the design pressure: invariant, ownership, substitution, construction,
   lifetime, extensibility, safety, testing, or dependency direction.
3. Prefer simple language features before patterns: functions, enums, pattern
   matching, modules, visibility, iterators, and traits.
4. Add abstraction only when it removes real duplication, makes invalid states
   harder to express, protects a boundary, or improves caller ergonomics.
5. Keep public APIs explicit about ownership, errors, feature flags, and caller
   obligations.
6. Verify with tests, doctests, compile-fail examples, or review of generated
   macro expansion when the pattern creates caller-facing contracts.

## Patterns To Prefer

- **Newtype:** wrap primitive or external types when a domain concept, unit,
  validation rule, secrecy boundary, or API distinction matters.
- **Enums and type states:** represent mutually exclusive states, protocol
  phases, command variants, and impossible combinations instead of parallel
  booleans or optional fields.
- **RAII guards:** tie cleanup, lock release, resource lifetime, or scoped state
  restoration to ownership and `Drop`.
- **Builder:** use when construction has many optional fields, validation, or
  staged defaults. Prefer normal constructors for small required data.
- **Traits as ports or strategies:** use traits for real substitution,
  dependency inversion, test fakes, plugin points, or generic algorithms. Keep
  trait bounds close to the item that needs them.
- **Compose structs:** prefer composition and explicit fields over inheritance
  emulation or broad base traits.
- **Small crates or modules:** split only when release, dependency, compile-time,
  ownership, or architectural boundaries earn it.
- **Contained unsafe modules:** isolate unsafe code behind a small safe API with
  documented invariants and focused tests.
- **Custom traits for complex bounds:** hide repeated generic bounds when the
  alias expresses a real capability and improves diagnostics.
- **Macros:** use `macro_rules!` or procedural macros only when functions,
  traits, derives, builders, or generics cannot provide a clear caller
  experience.

## Architecture And Methods

- **DDD:** encode value objects, invariants, and state transitions with newtypes,
  enums, constructors, and domain methods. Keep persistence and framework types
  out of domain APIs.
- **Clean / Hexagonal / Onion:** use traits or functions for outbound ports only
  when adapters, infrastructure, or tests need a boundary. Use modules/crates and
  visibility to enforce inward dependencies.
- **BDD:** keep examples at public API, use-case, or adapter boundaries; avoid
  scenario wording that depends on private Rust types.
- **TDD:** drive small domain rules with synchronous unit tests, use-case
  workflows with fakes, adapters with integration tests, and macro misuse with
  doctests or compile-fail tests.

## Review Checklist

- Does the pattern solve a named problem in this codebase?
- Does ownership match responsibility without avoidable clones or shared
  mutation?
- Are invalid states unrepresentable where the type system can reasonably do so?
- Are traits, generics, lifetimes, and feature flags as narrow as the contract
  allows?
- Are error types appropriate for library versus application edges?
- Are examples, tests, or compile-time checks present for public contracts?

## Common Mistakes

- Importing class-heavy patterns when enums, traits, functions, or modules are
  simpler.
- Creating one trait per struct without real substitution or dependency
  inversion.
- Using builders for ordinary required construction.
- Turning every boundary into async because one adapter performs I/O.
- Adding macros before proving ordinary Rust cannot express the API clearly.
- Treating pattern catalog names as proof that a design belongs in production.

## Source Anchors

- Rust Design Patterns, [Design Patterns](https://rust-unofficial.github.io/patterns/patterns/index.html).
- Rust Design Patterns, [Summary](https://github.com/rust-unofficial/patterns/blob/main/src/SUMMARY.md).
