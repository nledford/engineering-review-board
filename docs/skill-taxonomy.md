# Skill Taxonomy

This repository keeps first-party global agent skills small, focused, and
orthogonal. A skill is reusable operating guidance for a recurring task. It is
not a project diary, changelog, broad philosophy document, or dumping ground for
unloaded templates.

## Domain Model

- **Skill:** A directory under `skills/` with `SKILL.md` frontmatter and focused
  procedural guidance.
- **Trigger:** The frontmatter `description` tells the orchestrator when to load
  the skill. It must name the task surface and non-goals when confusion is
  likely.
- **Instructions:** The body explains what the agent should inspect, decide,
  change, verify, and report.
- **Constraints:** Guardrails that prevent misuse, overreach, unsafe actions, or
  stale evidence.
- **Examples:** Minimal scenarios only when they clarify activation or output
  quality.
- **Resources:** Optional `references/`, `scripts/`, `templates/`, or `assets/`
  files. First-party resources must be linked from `SKILL.md` and must not
  contain broken local links.
- **Validation:** `tools/skills_manager.py validate` checks metadata, first-party
  local links, and reachable resource files.

## Taxonomy

| Category | Skills | Boundary |
| --- | --- | --- |
| Skill authoring and governance | `create-agent-skill`, `code-review`, `review-verification-protocol`, `security-review-evidence` | Creating, validating, reviewing, and sanitizing durable agent guidance. |
| Design methods | `brainstorming`, `behavior-driven-development`, `domain-driven-design`, `test-driven-development`, `gherkin` | Use the direct method skill that matches the work; do not load a meta-selection skill. |
| Debugging and prevention | `systematic-debugging`, `root-cause-analysis` | Active symptom diagnosis first; postmortem and recurrence prevention after the direct cause is understood. |
| Rust engineering | `rust-code-review`, `rustdoc-guidance`, `cargo-clippy`, `cargo-nextest` | Rust-specific review, docs, linting, and test-runner guidance. |
| Project workflow tools | `git-commit`, `justfiles`, `playwright-e2e`, `context7-docs`, `suggest-lucide-icons` | Narrow operational guidance for common repository workflows and external documentation/icon checks. |
| Third-party runtime installs | `agent-browser`, `anti-ai-slop-writing`, `find-skills`, `playwright-cli` | Installed locally for runtime use but ignored or lockfile-owned; do not edit as first-party skills. |

## Method Selection

- Use **BDD** when externally observable behavior, workflows, or acceptance
  criteria need concrete examples.
- Use **DDD** when naming, boundaries, invariants, or long-term domain model
  clarity matter.
- Use **TDD** when implementation behavior can be specified and protected with
  executable tests.
- Use **Gherkin** when formal `.feature` syntax or durable Given/When/Then
  artifacts are useful.
- Use **Brainstorming** only when there are multiple credible paths and tradeoffs
  worth comparing before implementation.

Prefer one focused practice over several shallow ones.

## Inventory Decisions

| Skill | Decision | Rationale |
| --- | --- | --- |
| `behavior-driven-development` | Keep | Clear boundary for behavior examples and acceptance criteria. |
| `brainstorming` | Keep | Useful for ambiguous engineering choices; non-goals are explicit. |
| `cargo-clippy` | Keep, normalize | Narrow Rust linting skill; removed non-canonical timestamp/tool metadata. |
| `cargo-nextest` | Keep, normalize | Narrow Rust test-runner skill; removed non-canonical timestamp/tool metadata. |
| `code-review` | Split and rewrite | General review no longer owns Rust-only reference material. |
| `context7-docs` | Keep | Covers current third-party docs lookup without replacing repo inspection. |
| `create-agent-skill` | Keep | Canonical authoring workflow for new or updated skills. |
| `domain-driven-design` | Keep | Clear domain modeling boundary and anti-ceremony guidance. |
| `gherkin` | Keep | Focused syntax and quality guidance for `.feature` and scenario writing. |
| `git-commit` | Keep | Broad but coherent commit-quality workflow. |
| `justfiles` | Keep | Detailed because Justfile syntax and safety rules are operationally sharp. |
| `playwright-e2e` | Keep | Distinct from browser automation; owns checked-in Playwright tests. |
| `review-verification-protocol` | Keep | Required evidence gate for review findings. |
| `root-cause-analysis` | Keep, prune resources | Main skill is sufficient; generic references/templates were unreachable. |
| `rust-code-review` | Add | Owns Rust-specific review triggers and reference routing. |
| `rustdoc-guidance` | Keep | Focused Rust API documentation and doctest skill. |
| `security-review-evidence` | Keep, normalize | Sanitized evidence checklist for security-sensitive changes. |
| `software-design-practice-selection` | Remove | Duplicated direct BDD/DDD/TDD/Gherkin triggers; selection now lives in this taxonomy. |
| `suggest-lucide-icons` | Rewrite | Removed changelog/model metadata and made verification source-agnostic. |
| `systematic-debugging` | Keep | Strong active-failure workflow; clear handoff to RCA. |
| `test-driven-development` | Keep | Concise and directly actionable for behavior/test changes. |

## Acceptance Criteria

```gherkin
Scenario: General code review avoids Rust-only context
  Given an agent reviews a non-Rust diff
  When the code-review skill loads
  Then the agent follows general review and evidence rules
  And does not load Rust ownership, unsafe, or atomics references
```

```gherkin
Scenario: Rust review uses the specialist reference library
  Given an agent reviews Rust code involving unsafe, async, traits, or ownership
  When code-review identifies Rust-specific risk
  Then the agent also loads rust-code-review
  And reads only the reference files that match the touched surface
```

```gherkin
Scenario: Method selection uses direct skills
  Given implementation work involves behavior, domain modeling, or tests
  When an agent chooses a design practice
  Then it loads BDD, DDD, TDD, Gherkin, or Brainstorming directly as needed
  And does not load a separate meta-selection skill
```

```gherkin
Scenario: First-party resources are reachable
  Given a first-party skill contains a reference, script, template, or asset
  When repository validation runs
  Then every resource file is reachable from SKILL.md through local Markdown links
  And every local Markdown link resolves to an existing file
```

```gherkin
Scenario: RCA stays postmortem-focused
  Given a current test failure or crash has not been reproduced or understood
  When an agent starts diagnosis
  Then it uses systematic-debugging first
  And reserves root-cause-analysis for recurrence, incident, or prevention work
```
