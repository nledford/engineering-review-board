# Axum + Leptos Technical-Debt Audit

Use this reference with `technical-debt-audit` for a Rust application that
combines Axum, Leptos SSR, and `leptos_axum`. It refines the evidence procedure;
it does not grant command, edit, network, installation, or remediation authority.
Also use `rust-testing-quality` for test-lane semantics and `rust-antipatterns`
for code-level classification. Add dependency or security review skills only
when the audit includes those claims.

## 1. Establish The Build And Hydration Model

Read the workspace and package manifests before selecting commands.

- Locate cargo-leptos configuration. A single-package app commonly uses
  `[package.metadata.leptos]`; a workspace can use one or more
  `[[workspace.metadata.leptos]]` entries. Record the configured app/package,
  binary and library packages, server and browser features, output names,
  assets, and end-to-end command where present.
- Map the workspace members and the dependency direction between the server,
  app/UI library, shared domain code, and target-specific adapters. Confirm that
  metadata package names and feature names resolve to real packages and declared
  features.
- Trace `ssr`, `hydrate`, and `csr` through feature declarations, optional
  dependencies, and `cfg` gates. These modes are normally selected per build
  target; enabling all of them together can be invalid even when each lane is
  healthy independently.
- Inspect both the server entry point and the browser/WASM entry point. Confirm
  that the binary/library split in cargo-leptos metadata matches those entry
  points and that server-only dependencies do not leak into the WASM graph.

Determine the hydration mode before diagnosing hydration bugs, and state the
mode and evidence near the start of the report:

- **Islands architecture:** look for the Leptos `islands` feature, `#[island]`
  components, a client entry that calls `hydrate_islands`, and server markup
  configured with `HydrationScripts` in islands mode. One signal alone is not
  conclusive; the feature, server output, and client bootstrap must agree.
- **Full-page hydration:** look for a client entry that calls `hydrate_body` or
  the pinned version's equivalent, ordinary hydrated components, and hydration
  scripts without islands mode.
- **SSR without hydration or CSR-only:** record this explicitly. Browser-only
  behavior is still target-sensitive, but a hydration mismatch is not the right
  diagnosis when the application does not hydrate server markup.
- **Ambiguous or mixed evidence:** classify the mode as unconfirmed and name the
  missing configuration or runtime proof instead of assuming a hydration bug.

In islands mode, non-island server-rendered components are not expected to own a
full client reactive graph. In full-page hydration, server/client markup and
initial reactive state must match across the hydrated tree. Apply findings to
the detected model.

## 2. Execute Evidence Safely

Run commands only when the current request explicitly includes tooling evidence
and the active role permits them. Prefer repository recipes because they may
encode toolchains, packages, services, environment, targets, and feature policy.
Build scripts, procedural macros, tests, and repository-defined tools execute
repository-controlled code; inspect guidance and command definitions before
requesting approval.

Do not install missing tools, update dependencies or lockfiles, apply automatic
fixes, redirect output, or compose shell commands during a read-only audit.
Ordinary ignored `target` or tool-cache output is acceptable only when the role
permits the underlying command. Treat a missing tool, missing target, network
restriction, unavailable service, or invalid invocation as an evidence
limitation until repository evidence proves otherwise.

Use the active workspace and its checked-in Cargo configuration. Do not select
an alternate manifest, inject command-line Cargo configuration, select a custom
target-specification path, or choose custom target, output, lockfile, or artifact
directories; those options can escape the assigned scope, change executable
behavior, or write outside ordinary ignored build locations. The standard
`wasm32-unknown-unknown` target remains the expected direct hydration lane.
When a tracked `Cargo.lock` exists, use each command's supported `--locked` mode
and compare worktree status before and after execution. A stale lockfile is a
finding candidate or limitation to classify, not permission to update it.

For each attempted command, record:

1. tool availability or observed version;
2. the exact command;
3. exit status;
4. the smallest sanitized relevant excerpt, normally one to five lines; and
5. what the result proves and does not prove.

## 3. Use A Target-Aware Rust Matrix

Start with repository recipes. The following are adaptable evidence shapes, not
commands to copy without checking packages and features:

```sh
cargo metadata --locked --no-deps --format-version 1
cargo leptos build --release
cargo clippy --locked -p <server-or-app-package> --no-default-features --features ssr --all-targets -- -D warnings
cargo build --locked -p <server-or-app-package> --release --no-default-features --features ssr
cargo clippy --locked -p <client-or-app-package> --lib --target wasm32-unknown-unknown --no-default-features --features hydrate -- -D warnings
cargo build --locked -p <client-or-app-package> --lib --release --target wasm32-unknown-unknown --no-default-features --features hydrate
cargo test --locked -p <server-or-app-package> --no-default-features --features ssr
```

`cargo leptos build --release` is normally the strongest integrated compile
check because cargo-leptos coordinates the configured server and browser builds.
Direct commands are useful for isolating a broken lane, but must select the
correct package, target, crate kind, default-feature policy, and feature.

Do not run `--all-features` blindly. It is appropriate only when repository
policy says the selected features are compatible on the selected target. In a
typical Leptos app, `ssr`, `hydrate`, and `csr` are target-specific modes and may
pull mutually incompatible dependency surfaces. A host-only
`cargo build --features hydrate` is not proof that the WASM hydration lane works;
the hydration lane normally needs `wasm32-unknown-unknown` and the client library.

Categorize Clippy or build output by package, target, feature lane, and warning
class. Do not report only a warning count. A lane that does not compile is often
higher-risk debt than warnings in an already healthy lane, but first rule out an
incorrect invocation or missing environment prerequisite.

## 4. Check Dependency Health In Context

When available and authorized, adapt these checks:

```sh
cargo audit
cargo outdated
cargo tree -d
cargo +nightly udeps
```

- Do not install a missing Cargo subcommand or nightly toolchain. Record it as an
  unrun check and continue with manifests, the lockfile, and available output.
- State advisory-database freshness and network limitations for `cargo audit`.
  Trace a relevant advisory to the resolved lockfile version and dependency path;
  emphasize Axum, Leptos, `leptos_axum`, Tokio, and exposed runtime dependencies
  only when the evidence makes them relevant.
- Treat `cargo outdated` output as upgrade evidence, not a finding by itself.
  A pre-1.0 crate or a dependency multiple releases behind needs compatibility,
  maintenance, risk, or blocked-work evidence before it becomes debt.
- Check that `leptos`, `leptos_axum`, and related Leptos crates belong to a
  compatible release family. Axum need not share their version number; verify
  that its resolved version satisfies the pinned `leptos_axum` constraints and
  that direct Axum usage does not create avoidable version skew.
- Classify `cargo tree -d` results by target and feature path. Duplicate versions
  can be legitimate transitions or target-specific dependencies; quantify build
  cost, type incompatibility, security maintenance, or upgrade blockage before
  reporting debt.
- Scope unused-dependency evidence to the feature/target matrix. A dependency
  unused in SSR can still be required by hydration, CSR, tests, examples, build
  scripts, or platform-specific code. Treat `udeps` output as a lead and verify
  references and feature gates.

## 5. Compare Axum And Leptos Routing Semantics

`generate_route_list` describes routes declared by the Leptos application. It is
not intended to enumerate health endpoints, static assets, APIs, webhooks,
server-function endpoints, fallbacks, or other ordinary manual Axum routes.
Therefore, ordinary manual Axum routes absent from the generated Leptos list are
not drift by themselves.

Inspect the pinned `leptos_axum` API and application assembly, then check:

- the generated Leptos route list is passed to the appropriate
  `LeptosRoutes`/`.leptos_routes*` wiring with the intended app function and
  options;
- manually declared routes do not duplicate, shadow, or unexpectedly pre-empt
  generated page paths;
- nesting, merge order, fallback handling, static-file serving, server-function
  handling, router state, and server-function context are consistent;
- Leptos routes that exist in the component tree are reachable through the Axum
  router under the expected base path; and
- route-specific rendering modes or exclusions are intentional and tested.

There is no universal audit CLI that prints the fully merged runtime router.
Prefer an existing route inventory or router integration test. If none exists,
compare construction sites by inspection and recommend a focused test; do not
instrument or edit a repository during a read-only audit.

## 6. Inspect Async Runtime And Scaling Debt

Search request handlers, middleware, server functions, application services, and
background work for:

- synchronous filesystem, network, process, sleep, or database calls on Tokio
  runtime threads; CPU-heavy work without a bounded `spawn_blocking` or worker
  boundary;
- `std::sync::Mutex` or `RwLock` guards held across `.await`, broad critical
  sections, nested locks, unbounded queues, and global contention in Axum state;
- detached `tokio::spawn` work, dropped or ignored `JoinHandle` results, hidden
  panics, missing cancellation, and tasks with no shutdown owner;
- request-local data or transactions held across unrelated awaits; and
- process-local state for sessions, jobs, rate limits, caches, coordination, or
  identity that silently breaks under restart or more than one instance.

For horizontal-scaling findings, identify the exact state, consistency need,
failure mode, and deployment assumption. In-memory caches are not automatically
debt; they become blockers when correctness or coordination depends on one
process and no affinity, shared store, idempotency, or recovery contract exists.

## 7. Inspect Leptos-Specific Boundaries

- Treat every `#[server]` function as a public trust boundary. Verify input
  validation, authentication/authorization, idempotency where relevant, stable
  error mapping, and separation of reusable business logic from transport glue.
- Trace error propagation from server functions and resources to visible UI.
  Look for appropriate `ErrorBoundary`, `<Suspense>`, fallback, retry, and status
  behavior rather than panics or silent server errors.
- Classify `unwrap`, `expect`, and `panic!` by execution path. Startup invariant
  checks and tests differ from request handlers, server functions, rendering,
  resource loading, and spawned tasks.
- Review large components and signal graphs for repeated derivation, effects
  that write other signals unnecessarily, broad invalidation, duplicated
  resources, sequential independent loads, and business policy embedded in UI
  plumbing. Require a plausible rerun or maintenance cost before calling for a
  memo or abstraction.
- Check browser APIs against both target and lifecycle. Browser-only modules
  normally need the hydrate/CSR target gate, and DOM-dependent work should occur
  in an appropriate client lifecycle such as an effect rather than during SSR.
  A `cfg` gate alone does not prove hydration-safe timing.
- In islands mode, focus client graph and resource concerns on island boundaries
  and their serialized props. In full-page hydration, also inspect initial
  server/client state and markup across the whole hydrated tree.

## 8. Assess Tests And Documentation

Run the repository-supported test lane when authorized, then map confidence by
boundary rather than inventing coverage percentages:

- unit tests for domain logic and reusable services called by server functions;
- server-function tests for validation, authorization, errors, and side effects;
- Axum router integration tests for generated routes, manual routes, middleware,
  state/context, fallbacks, and error mapping;
- SSR rendering tests and target-specific compile checks;
- browser tests for hydration, islands, navigation, resources/actions, forms,
  and error boundaries where those are critical paths; and
- task, cancellation, contention, restart, and multi-instance assumptions where
  runtime behavior is decision-relevant.

Inspect skipped, ignored, quarantined, or retrying tests and distinguish a known
owner/exit condition from indefinite confidence debt. Check module-level `//!`
documentation on non-trivial public modules and Rustdoc for public server
functions, including input trust, authorization, errors, and side effects.

## 9. Report Actionable Findings

Every finding must include a file and line (or the narrowest configuration or
runtime location), description, SSR/Leptos-specific consequence, evidence,
smallest durable remediation, risk, effort, expected benefit, and verification.
When tool output is evidence, include its exact command, exit status, and focused
sanitized excerpt. Separate quick wins from structural work and call out any
evidenced blocker to upgrades, future features, operations, or horizontal
scaling.
