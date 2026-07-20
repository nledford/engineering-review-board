---
name: ruby-engineering
description: Ruby engineering guidance. Use when creating, changing, reviewing, testing, packaging, or scripting Ruby source, gems, Gemfiles, Bundler, Rake, Minitest, RSpec, Rails-adjacent Ruby, or Ruby CLIs. Do not use merely to choose among scripting languages without Ruby implementation, or for framework-specific behavior whose owning skill is more precise.
---

# Ruby Engineering

Use this skill for repository-backed Ruby implementation and workflow decisions.
Inspect the supported Ruby version, Bundler and gem policy, source layout, test
framework, style tools, and execution targets before assuming a universal Ruby
setup.

Use [`script-engineering`](../script-engineering/SKILL.md) when the primary
decision is whether automation should be a script or whether Ruby fits better
than shell, Python, PowerShell, or JavaScript. This skill owns the Ruby mechanics
after Ruby is selected.

## Workflow

1. Read repository instructions, `.ruby-version`, version-manager files,
   `Gemfile`, `Gemfile.lock`, gemspecs, `Rakefile`, source/tests, CI, and existing
   Ruby commands.
2. Identify supported Ruby and Bundler versions, target operating systems, and
   whether the code is an application, library, gem, CLI, or repository script.
3. Preserve the repository's framework and conventions. Do not introduce Rails,
   RSpec, Minitest, RuboCop, Sorbet, Steep, or another tool without evidence or
   an explicit adoption goal.
4. Define observable behavior and choose the narrowest useful test boundary.
5. Implement small explicit objects, modules, and functions; isolate external
   processes, filesystems, clocks, networks, and databases behind testable
   boundaries.
6. Run focused syntax, test, lint, and packaging checks before broader
   repository-native validation.
7. Report versions and commands observed, files and dependencies changed,
   validation run, skipped targets, and remaining compatibility risk.

## Runtime And Dependency Discipline

- Treat `.ruby-version`, `.tool-versions`, `mise.toml`, gem metadata, CI images,
  and deployment configuration as runtime evidence. A locally available `ruby`
  does not prove every target supports that version.
- Use the repository's Bundler workflow. Prefer `bundle exec <command>` for
  project-owned executables when that is the established way to bind commands to
  the lockfile.
- Keep `Gemfile` intent and `Gemfile.lock` changes aligned. Do not hand-edit
  lockfile resolution or introduce a global gem dependency for project behavior.
- Prefer the standard library for small needs when it is clear and sufficient.
  Add a gem only when its maintained behavior outweighs dependency, native
  extension, startup, licensing, and supply-chain cost.
- Load
  [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
  for new gems, lockfile churn, native extensions, sources, install hooks,
  provenance, or advisory questions.

## Idiomatic Ruby

- Prefer clear message-oriented objects, modules, blocks, enumerators, keyword
  arguments, and standard collection APIs over manual indexing or framework
  ceremony.
- Keep methods cohesive and make mutation visible. Return useful domain values
  instead of relying on unrelated global or process state.
- Use modules for shared behavior or namespaces deliberately; do not use mixins
  as an unstructured substitute for object boundaries.
- Make public APIs explicit about accepted values, returned values, exceptions,
  side effects, and destructive or mutating behavior. Use `?` and `!` names only
  when they follow established Ruby meaning in the repository.
- Prefer ordinary methods, delegation, and explicit registration over dynamic
  dispatch. Use metaprogramming only when it materially reduces repeated
  structure and leaves discoverable behavior, tests, and error messages.
- Preserve exception context. Rescue only errors the current boundary can
  handle, and convert them into a stable domain or CLI result where appropriate.
- Keep load-time work cheap and deterministic. Avoid network, filesystem,
  process, or environment-dependent side effects during `require`.
- Follow the repository's formatter and style configuration instead of applying
  a different community style mechanically.

## Ruby Anti-Patterns

Avoid:

- global monkey patches to core classes or dependencies;
- `method_missing`, callbacks, DSL magic, or reflection where an explicit API is
  simpler and easier to test;
- mutable constants, global variables, class variables used as shared state, or
  singleton service registries that hide ownership;
- rescuing `Exception`, broad rescue-and-continue behavior, swallowed failures,
  or retry loops without bounds and an error policy;
- shell command strings assembled from input, backticks for complex process
  control, or ignored subprocess exit status;
- implicit working-directory assumptions and unscoped temporary files;
- tests that stub the object under test, assert private call order, or replace so
  many collaborators that no real behavior remains; and
- framework models, callbacks, or persistence types leaking into domain APIs
  without an intentional boundary.

## Testing Ruby

Use the test framework already owned by the repository.

- **Unit:** test value objects, parsers, formatters, validation, domain rules,
  enumerators, and error behavior without external resources.
- **Integration:** exercise real filesystem, subprocess, database, framework,
  gem, serialization, and adapter boundaries in isolated fixtures.
- **CLI/process:** invoke the executable when arguments, environment, stdout,
  stderr, signals, or exit status are part of the contract.
- **End to end:** cover a complete supported user or operator workflow only when
  lower levels cannot prove the behavior. Use the repository's web/system-test
  stack; do not assume Rails, Capybara, Selenium, or a browser runner.

For Minitest, preserve the repository's spec-style or class-style convention and
run its configured Rake or direct Ruby lane. For RSpec, preserve configured
formatters, tags, helpers, and suite boundaries and use the Bundler-bound command.
Do not migrate between them merely for preference.

Keep tests deterministic and isolated. Use temporary directories, fake clocks,
seeded randomness, and boundary substitutes where needed; avoid live networks,
shared databases, process-global leakage, order dependence, and unbounded sleeps.
Mock external boundaries, not the behavior being specified.

Typical checks to derive from repository evidence include:

```sh
ruby -c path/to/file.rb
bundle exec ruby -Itest path/to/test_file.rb
bundle exec rake test
bundle exec rspec path/to/spec_file.rb
bundle exec rubocop
```

Do not claim a command exists or passed without observing it. Use
[`test-driven-development`](../test-driven-development/SKILL.md) for behavior
changes and regressions, and [`systematic-debugging`](../systematic-debugging/SKILL.md)
for an active unexplained Ruby failure.

## Ruby As A Script Choice

Prefer Ruby when all required targets provide the supported runtime and one or
more of these are true:

- the repository already uses Ruby and the script can reuse maintained code or
  locked gems;
- structured text, files, APIs, reusable functions, or CLI parsing have outgrown
  a small shell wrapper;
- Ruby's collection, string, regular-expression, or DSL capabilities express the
  task clearly without introducing an additional runtime; or
- the automation is naturally adjacent to a Ruby application, gem, or Rake
  workflow.

Do not choose Ruby when a short portable shell command is clearer, Ruby is
absent from a bootstrap or deployment target, the repository already has a
suitable supported automation language, or author familiarity is the only
advantage. Domain behavior that callers should import belongs in the application
or library, with a thin script or CLI entry point at most.

## Security And Completion

Load [`security-review`](../security-review/SKILL.md) when Ruby code handles
untrusted input, paths, serialization, templates, commands, credentials,
privileged operations, or remote targets. Use
[`security-review-evidence`](../security-review-evidence/SKILL.md) when logs,
fixtures, reports, or reproduced output may contain sensitive values.

Before handoff, report the Ruby and Bundler evidence, why Ruby fit the task,
tests and quality gates run, dependency or lockfile impact, skipped platforms,
and residual runtime, compatibility, or security risk.
