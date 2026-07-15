# Human-Controlled Plan Creation and Execution Routing

## TL;DR

Separate implementation planning into three explicit paths: read-only advice from
a constrained `plan-consultant`, human-authorized plan creation through a
plan-only command, and execution or resume of an existing plan through
`/start-work`. Drive each behavioral slice with focused failing contract tests,
make the smallest prompt and validator changes that satisfy them, and refactor
only while the tests remain green.

## Context

**Original request:**

Create a high-level implementation plan only for correcting agent routing so
`/start-work` is required only to execute or resume an existing plan. Use TDD
phases and the safe consultation design of a separate read-only
`plan-consultant` rather than exposing the mutation-capable Plan Orchestrator
through Task. Do not execute the plan.

**Key repository findings:**

- The Engineering Lead currently routes every explicit plan request, every
  durable-contract change, and all Complex work to `/start-work`.
- `/start-work` and the Plan Orchestrator currently accept a free-form request,
  create a plan, and execute it by default; they can also create a legacy
  successor or execute remaining work after a conversational update.
- The Plan Orchestrator is a primary agent with plan, trusted-state, delegation,
  staging, and commit authority. Making that definition Task-visible would give a
  consultation child an unnecessarily broad mutation surface.
- `tools/opencode_manager.py` and `tests/test_opencode_manager.py` deliberately
  require the current automatic-routing and execute-by-default prompt text, so
  agent-only edits would fail validation and leave contradictory policy.
- `opencode/manifest.json`, project templates, governance documentation, retained
  review and audit routes, and the linked OpenCode installation all participate
  in the routing contract. Definition changes take effect only after a full
  OpenCode restart.

**Dependencies:**

- The human-selected topology is authoritative: `plan-consultant` is a separate
  read-only subagent, while `plan-orchestrator` remains a top-level primary agent
  and never a Task child.
- A dedicated `/create-plan` command will represent explicit human authorization
  for plan-only creation; `/start-work` will accept only an existing canonical
  lean plan path or a validated no-argument resume pointer.
- Existing trusted-state acquisition, containment, pointer hashing, Worker
  prohibitions, ERB independence, and Git safety rules remain available and must
  not be weakened by the routing split.
- Repository validation uses Python `unittest` and the existing Just recipes;
  runtime smoke checks require a full OpenCode restart after definition changes.

## Objectives

- Make direct, unplanned implementation the Engineering Lead default regardless
  of complexity when scope and safety permit it.
- Require explicit human authorization before any durable plan is created, while
  allowing the Lead and ERB to recommend planning and obtain bounded read-only
  planning advice.
- Give the Lead and ERB access to a hard read-only `plan-consultant` without
  making the Plan Orchestrator Task-visible.
- Make `/create-plan` plan-only and make `/start-work` execution-only for an
  existing canonical plan or validated resume pointer.
- Encode the revised topology, permissions, command ownership, routing language,
  and negative safety constraints in deterministic tests and validators.
- Keep authoritative agents, commands, governance docs, retained routes, project
  templates, and installation inventory consistent.

## Guardrails

- Do not change `plan-orchestrator` to `mode: all`, add it to a Task allowlist, or
  rely on child-prompt wording to constrain its mutation-capable permissions.
- Give `plan-consultant` no edit, Bash, Task, TODO, commit, durable-plan, or
  `.start-work/**` authority; consultation cannot create a plan, authorize work,
  mutate state, or begin implementation.
- Preserve the Engineering Lead's existing MCP and predominantly non-destructive
  Git permission baseline, the ERB's read-only independence, and the
  Implementation Worker's prohibition on plans, state, delegation, staging, and
  commits.
- Complexity may trigger a planning recommendation, but never automatic plan
  creation or `/start-work`; the human decision to accept or decline the
  recommendation controls the route subject to ordinary safety stop conditions.
- Reject free-form new requests and immutable legacy plans at `/start-work`
  rather than silently creating a plan or successor. Route explicit creation to
  `/create-plan` and legacy conversion to the existing conversion boundary.
- Keep plan creation and execution lock-protected and fail closed on unsafe paths,
  state corruption, unresolved material choices, or unavailable trusted helpers.
- Observe each focused RED failure for the intended contract reason before the
  corresponding implementation, make the minimum GREEN change, and refactor only
  after the focused tests pass.
- Do not fold the separate plan-location, verification-checkbox, plan-immutability,
  or commit-policy changes into this routing correction unless they are strictly
  required to keep the new routing internally consistent.

## Deliverables

- A new read-only `opencode/agents/plan-consultant.md` definition, manifested and
  explicitly allowlisted only for bounded consultation by the Lead and ERB.
- Revised Engineering Lead, Engineering Review Board, and Plan Orchestrator
  contracts that distinguish recommendation, consultation, explicit creation,
  and execution without weakening existing authority boundaries.
- A new primary `/create-plan` command that creates and persists a plan without
  executing it, plus an execution-only `/start-work` command that rejects
  free-form creation and legacy succession.
- Updated manifest inventory, canonical command ownership, prompt contracts,
  permission/topology validation, fixtures, and regression tests.
- Synchronized root guidance, engineering-agent governance, cross-reference
  routing, retained review and audit commands, cleanup guidance, README text, and
  project templates.
- Focused RED/GREEN evidence, final repository validation, and a documented full
  restart plus bounded runtime smoke check.

## Definition of Done

- Tests prove that neither complexity nor a durable-contract change forces the
  Engineering Lead to invoke `/start-work`, and that both the Lead and ERB require
  human authorization before durable plan creation.
- `plan-consultant` is Task-visible to the Lead and ERB but is mechanically
  read-only, cannot delegate, and cannot read or mutate trusted planned-work
  state; `plan-orchestrator` remains primary-only and absent from Task allowlists.
- `/create-plan` is owned by the Plan Orchestrator, uses `subtask: false`, requires
  an explicit human request, and completes plan-only without beginning TODO
  execution.
- `/start-work` accepts only an existing valid lean plan path or validated resume
  pointer, rejects free-form and legacy creation routes, and retains lock,
  reconciliation, execution, checkbox, and failure-safety behavior.
- Validators and negative tests reject reintroduction of automatic planning,
  execute-by-default creation, consultant mutation permissions, recursive Task
  topology, or Plan Orchestrator child invocation.
- Every authoritative agent, command, retained route, governance document,
  project template, and manifest entry describes the same human-controlled
  lifecycle.
- Focused tests and the full required validation suite pass, and runtime smoke
  evidence is collected after a full OpenCode restart or explicitly reported as
  skipped with a reason.

## TODOs

1. [x] RED—add focused contract and permission tests for the missing `plan-consultant` topology, proving that the Lead and ERB may delegate bounded planning advice only to a manifested read-only, non-recursive subagent and that the mutation-capable Plan Orchestrator remains primary-only; run the focused tests and confirm they fail for the expected missing-agent and allowlist reasons.
2. [x] GREEN—add the minimal `plan-consultant` definition, manifest entry, Lead and ERB consultation rules and Task allowlists, validator contracts, and fixtures needed to pass the consultation tests without granting edit, Bash, TODO, Task, durable-plan, trusted-state, staging, or commit authority; rerun the focused tests to green before refactoring.
3. [x] RED—add focused command and prompt-contract tests that require human-controlled plan recommendations, explicit plan-only creation through `/create-plan`, execution-only `/start-work` behavior for an existing lean path or validated resume pointer, rejection of free-form and legacy creation routes, and removal of automatic Complex or durable-contract routing; run them and confirm the current policy fails for the intended reasons.
4. [x] GREEN—make the smallest coordinated changes to the Engineering Lead, Engineering Review Board, Plan Orchestrator, `/create-plan`, `/start-work`, manifest ownership, and prompt-contract validator needed to satisfy the new lifecycle tests while preserving trusted acquisition, plan/state ownership, Worker restrictions, ERB independence, and Git safety.
5. [x] REFACTOR—while focused tests remain green, remove obsolete route tokens and duplicated lifecycle prose, strengthen negative tests against consultant permission broadening and automatic plan creation, and reconcile retained review, audit, conversion, and cleanup routes with the explicit create-versus-execute split.
6. [x] Synchronize `AGENTS.md`, `README.md`, engineering-agent governance, the cross-reference map, project templates, and other repository-evidenced guidance; then run focused and broad validation, inspect the complete diff for policy contradictions or unrelated changes, and perform the post-restart bounded runtime smoke checks in a disposable repository.

## Verification

- Confirm each RED phase failed before its corresponding GREEN change and that
  the failure named the intended missing or obsolete contract rather than a test
  setup error.
- `python3 -m unittest discover -s tests -p 'test_opencode_manager.py' -v`
- `python3 -m unittest discover -s tests -p 'test_start_work_state.py' -v`
- `just validate-opencode`
- `just validate`
- `just check`
- `git diff --check`
- After a full OpenCode restart, use a disposable repository to verify that the
  Lead and ERB can obtain read-only `plan-consultant` advice, `/create-plan`
  creates without executing, `/start-work` rejects a free-form request, and
  `/start-work <existing-plan-path>` reaches only the execution route.
