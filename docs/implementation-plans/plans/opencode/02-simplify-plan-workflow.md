---
plan_id: opencode-02
series: opencode
sequence: 2
title: Simplify the OpenCode Plan Workflow
status: draft
revision: 2
review_decision: pending
reviewed_at:
approved_at:
approved_revision:
depends_on: []
baseline_commit: 9bd28e3a15c237e1fb4cf6e1996da36b687db5e8
execution_owner: plan-orchestrator
source_format: native
source_plan:
created: 2026-07-14
updated: 2026-07-14
completed_at:
---

# OPENCODE-02 — Simplify the OpenCode Plan Workflow

## Executive Summary

Replace the current review-and-approval lifecycle with a lean plan contract for a
solo operator. New plans retain canonical series paths and collision-safe
sequence allocation, but their contents are limited to a title, `TL;DR`, Context,
Objectives, Guardrails, Deliverables, Definition of Done, numbered checkbox
TODOs, and Verification. They carry no frontmatter, lifecycle state, revision,
approval, review, amendment, attribution, alternative, or execution history.

Replace the `planning-coordinator` definition and ID with one dedicated top-level
`plan-orchestrator`; the manifest keeps 23 agents rather than adding another
role. The Plan Orchestrator writes, updates, self-checks, and executes lean plans,
including direct planned implementation or bounded delegation only to
`implementation-worker`. It owns plan checkboxes, native sidebar TODOs,
integration, validation, and completion reporting. Its self-check is an internal
quality pass, never ERB review, approval, readiness, or sign-off.

Unify new requests, lean-plan updates, legacy succession, and execution under
`/start-work <request-or-plan-path> [instructions]`. Keep
`/convert-tapestry-plan`, but conversion executes only when the human also asks
for execution. Independent `/review-plan` and `/review-implementation` sessions
remain optional, read-only ERB advice. The Engineering Lead stays the default
primary for ordinary unplanned work, but neither the Lead nor the ERB may write,
update, execute, or implement planned work; both route that work to
`/start-work`.

Execution uses native `todowrite` as a transient, five-item sliding window over
the plan's numbered TODOs. Prompt-contract tests, not claims about native UI
enforcement, protect ordering, status, content-length, resume, failure, and final
clearing behavior.

## Problem and Context

The repository currently treats plans as lifecycle records. Creation, persisted
review, revision, approval, execution state, normalization, and histories are
split across a Coordinator, nine plan-lifecycle commands, metadata-heavy
templates, governance prose, and validator constants. That ceremony conflicts
with the human-selected workflow: a plan is an editable execution contract, not
an approval or audit ledger.

The target workflow must support ordinary requests such as “roll these changes
into the plan” without a revision transition or special authorization. Review is
separate advice. Execution may start from a valid lean plan without a review or
approval record, but still stops for a real unresolved decision, unsafe action,
missing dependency, scope conflict, or failed acceptance evidence.

Canonical filenames remain useful for organization and allocation. Existing
verbose plans are therefore grandfathered as immutable legacy artifacts whose
filenames still count toward the series maximum. They are not executable in
place; the Plan Orchestrator creates a newly allocated lean successor when one is
needed.
The existing untracked `opencode-01` plan is such an artifact, is not a
dependency of this plan, and must remain byte-unchanged.

## Objectives

- Define one closed, metadata-free plan body with only the human-authorized
  sections and numbered Markdown-checkbox TODOs.
- Replace `planning-coordinator` with a primary `plan-orchestrator` that owns safe
  plan creation, conversational updates, legacy succession, Tapestry conversion,
  self-checking, planned execution, integration, and completion reporting.
- Reduce the plan command surface to `/start-work`, retained Tapestry conversion,
  optional plan review, and optional implementation review while preserving the
  two unrelated ERB commands.
- Keep the ERB independent, primary, read-only, and advisory while removing plan
  readiness and implementation approval/sign-off decisions.
- Keep `implementation-worker` as the only implementation subagent and preserve
  its existing plan, delegation, Git, push, and destructive-operation denials.
- Give only the Plan Orchestrator explicit planned-work checkbox and sidebar
  ownership, including flat `todowrite: allow` and the complete transient TODO
  contract.
- Keep the Lead's ordinary unplanned-work authority, MCP access, and clipboard
  authorization while denying plan edits and removing all Coordinator or Plan
  Orchestrator Task edges.
- Add prompt and validator guardrails that route planned work from the Lead and
  ERB to `/start-work` instead of allowing either role to bypass the Plan
  Orchestrator.
- Keep root and project-template plan guidance synchronized and update the
  manifest, validator, fixtures, and tests as one coherent contract.

## Non-Goals

- Rewrite, normalize, or execute historical plan files, including `opencode-01`.
- Copy Weave continuation hooks, internal imports, compaction state, idle
  mutation, plugin code, or `.weave` state machinery.
- Add a plugin, custom TODO tool, database, audit trail, approval state,
  persisted review result, compatibility alias, or a second planning role beside
  the selected Plan Orchestrator.
- Change unrelated specialist agents, audit/regression commands, the legacy
  cleanup checklist, or skills.
- Change skills, dependencies, credentials, providers, configured MCP access,
  live machine-local OpenCode configuration, or external repositories.
- Commit, push, deploy, or mutate the existing legacy plan during this work.

## Applicable Project Guidance

- `AGENTS.md` requires the repository README, skill taxonomy, cross-reference
  map, and engineering governance guide to be read before repository-doc changes.
  It requires `just validate` for routing or link changes and `just check` for
  tooling, tests, scripts, or validator changes.
- `README.md` makes `opencode/manifest.json` the reviewed inventory, treats the
  linked checkout as live after OpenCode restart, and keeps credentials and live
  configuration outside the repository.
- `docs/engineering-agent-governance.md` owns role authority, exact runtime Task
  IDs, one-level delegation, command ownership, and ERB independence.
- Until this plan is implemented, `docs/implementation-plans/README.md` and
  `TEMPLATE.md` require this transition plan's current frontmatter and lifecycle
  sections. The implementation replaces that contract only for new plans.
- Root and project-template implementation-plan README/template files are
  validator-enforced byte-for-byte copies.

## Current-State Evidence

- Planning-time `HEAD` is the supplied baseline
  `9bd28e3a15c237e1fb4cf6e1996da36b687db5e8` on `main`. Before this plan was
  added, `git status --short` reported only the pre-existing untracked
  `docs/implementation-plans/plans/` directory.
- The `opencode` series contained only
  `01-agent-definitions-improvement-program.md` when sequence `02` was allocated.
  The assignment and initial read identified it as an untracked legacy draft at
  revision 2. A post-persistence reread showed an external concurrent update to
  revision 3 and the supplied baseline; this Coordinator did not write that
  file. Its filename still makes the observed maximum `01`, and this plan does
  not depend on its content or identity.
- `opencode/manifest.json` currently inventories 23 agents and 11 commands. The
  plan-lifecycle commands are `prepare-work`, `review-plan`,
  `record-plan-review`, `revise-plan`, `approve-plan`, `execute-plan`,
  `review-implementation`, `convert-tapestry-plan`, and `normalize-plan`; the
  audit and regression commands remain separate primary entry points.
- The Lead currently has `ask` edit access for plan paths, a plan-path Bash deny,
  direct implementation authority, and Task access to both Coordinator and
  Worker. The Worker already denies plan edits and plan-path Bash access,
  delegation, commit, push, and destructive operations. The ERB is a separate
  read-only primary.
- `planning-coordinator` is currently a subagent with exclusive plan-write
  authority and no implementation or delegation authority. No
  `plan-orchestrator` definition or `/start-work` command exists at the supplied
  baseline.
- `PLAN_TEMPLATE_TOKENS` and `PLAN_TEMPLATE_HEADINGS` in
  `tools/opencode_manager.py` require the lifecycle metadata and history sections
  in the synchronized template. `tests/test_opencode_manager.py` builds the same
  verbose fixture and has mutation coverage for those requirements.
- The manager's known permission tools do not include `todowrite`, and no current
  repository definition contains that permission. The supplied OpenCode evidence
  establishes that `todowrite` is flat, each call replaces the whole session
  list, input order is display order, and `todos: []` clears it. Native OpenCode
  does not enforce this plan's five-item, one-active-item, or 30-character rules.
- The specialist inspection supplied by the human reports that
  `just validate-opencode` and all 58 focused OpenCode manager tests passed before
  planning. This Coordinator did not rerun those implementation checks; final
  execution validation is specified below.
- The revision request confirms that this plan had no ERB review or approval
  history before revision 2. The supplied baseline remains
  `9bd28e3a15c237e1fb4cf6e1996da36b687db5e8`, and the worktree still contains
  only the two untracked `opencode` plan files.

## Proposed Design

### Lean plan contract

Retain the canonical path
`docs/implementation-plans/plans/<series>/<NN>-<slug>.md`, the series regex,
zero-padded `01`–`99` range, maximum-plus-one allocation, gap non-reuse,
collision checks, and exhaustion behavior. Identity comes from the path; it is no
longer repeated inside the plan.

The complete body for every newly created, updated, succeeded, or converted plan
is:

```markdown
# <Title>

## TL;DR

## Context

**Original request:**

**Key repository findings:**

**Dependencies:**

## Objectives

## Guardrails

## Deliverables

## Definition of Done

## TODOs

1. [ ] <bounded implementation step>

## Verification
```

No other metadata or sections are allowed. In particular, omit frontmatter,
plan IDs, statuses, baselines, owners, dates, revision/review/approval fields,
provenance fields, histories, amendments, specialist attribution, alternatives,
execution records, and open-decision ledgers. Context retains only the original
request, decision-relevant repository findings, and actual prerequisites that an
executor cannot safely ignore. Do not copy inventories, Git history, current
diffs, or other state merely because it can be re-read from the repository.

Objectives state intended outcomes. Guardrails bind safety and exclusions.
Deliverables name the durable results. Definition of Done states behavioral
acceptance. TODOs are ordered, bounded, numbered checkbox work units, and
Verification names the checks needed to prove completion. Required unresolved
choices are settled conversationally and rolled into these sections before
execution rather than stored as lifecycle state.

### Plan Orchestrator authority and safe plan writes

Replace `opencode/agents/planning-coordinator.md` with
`opencode/agents/plan-orchestrator.md` and change the exact runtime ID to
`plan-orchestrator`. The new definition is a primary agent with broad `ask`
authority for safe direct implementation. It writes plan paths only through edit
tools, keeps `docs/implementation-plans/**: ask`, retains the plan-path Bash
deny, and re-reads every plan write before continuing or reporting success.

Before creation, update, succession, or conversion, the Plan Orchestrator rejects
a symlinked plan root, source, destination parent, or destination and proves that
the resolved target remains under `docs/implementation-plans/`. It validates the
series, calculates the existing-series maximum, allocates maximum plus one from
`01` through `99` without filling gaps, checks collision and exhaustion, and
blocks if an edit tool cannot safely create the required parent. It never uses
shell redirection, shell file mutation, an apply-patch move, or alternate path
spelling for a plan.

An existing lean plan may be updated in place from `/start-work` instructions or
ordinary Plan Orchestrator conversation, without revision semantics. If the
target has frontmatter or otherwise fails the closed lean shape, leave it
untouched and allocate a successor in the same series. Carry forward only useful
original-request context, current repository findings, real dependencies,
objectives, guardrails, deliverables, acceptance conditions, TODOs, and
verification. The predecessor still reserves its filename number; sequence order
does not create an execution dependency.

The Plan Orchestrator owns all planned implementation. It may implement directly
or delegate one bounded implementation unit at a time only to the exact
`implementation-worker` ID, then it integrates and validates the result. Its Task
map is broad-deny with only `implementation-worker: allow`; it cannot invoke the
ERB, the Engineering Lead, specialists, or any other primary agent through Task.
The Worker still cannot delegate, which preserves one-level delegation.

### `/start-work` and Tapestry conversion

`/start-work <request-or-plan-path> [instructions]` is the single create, update,
and execute entry point, owned by `plan-orchestrator`:

- For a new request, inspect current evidence, select a valid series, allocate and
  write a lean plan, self-check it, then execute by default. If series choice has
  material organizational consequences, stop for the human rather than guessing.
- For a lean plan path, apply requested conversational changes in place,
  self-check the complete result, then execute unchecked TODOs by default.
- For a legacy plan path, preserve the source byte-for-byte, allocate a lean
  successor under the same series, self-check it, and execute that successor by
  default.
- When the human explicitly requests plan-only behavior, complete the write and
  self-check but do not implement, delegate, update execution checkboxes, or
  populate the sidebar as though execution started.

Do not add `/create-plan`, `/update-plan`, or another execution command. The Plan
Orchestrator prompt applies the same operations during ordinary conversation, so
the command is a convenient top-level route rather than a separate authority
model.

`/convert-tapestry-plan <source> <series> [instructions]` also routes directly to
`plan-orchestrator`. It reads the complete source, revalidates referenced files,
symbols, behavior, dependencies, acceptance conditions, and commands against the
current repository, then writes and self-checks a newly allocated lean plan. It
keeps only still-useful source content in allowed sections, preserves the source,
and writes no provenance metadata. Conversion is plan-only by default; execute
the converted plan only when the human also requests execution.

### Self-check and optional independent review

Before planned execution, the Plan Orchestrator's self-check confirms the exact
lean shape, current repository grounding, objective-to-deliverable alignment,
bounded and ordered TODOs, guardrail coverage, behavioral Definition of Done,
usable verification, and absence of an unresolved central decision. It corrects
ordinary plan defects and re-reads the result. A real missing product or
architecture choice, unsafe action, absent prerequisite, scope conflict, or
unverifiable acceptance condition stops work for the human.

This self-check is not independent: never label or describe it as ERB review,
approval, readiness, sign-off, or equivalent evidence. It creates no review
record and is not a substitute for `/review-plan` or `/review-implementation`.

The Plan Orchestrator may report one out-of-band review-advice level:

- `none`: independent review is unlikely to change a narrow, well-evidenced
  execution.
- `recommended`: independent review could materially improve confidence, but
  execution may proceed without it.
- `strongly recommended`: risk or uncertainty makes independent review prudent,
  but the label itself is not an execution gate.

Never write the level into a plan or turn it into approval state. The ERB remains
a separate top-level, read-only primary. `/review-plan` and
`/review-implementation` return findings, evidence, uncertainty, suggested
corrections, skipped checks, and residual risk only; they produce no durable
record, plan readiness decision, implementation approval/sign-off, or mandatory
gate. After giving advice, the ERB directs the user to
`/start-work <plan-path>` to apply changes or execute, while stating that review
was optional.

### Lead, ERB, and Worker guardrails

The Engineering Lead remains the default primary for ordinary unplanned request
intake, classification, bounded implementation, integration, and validation. Set
its plan-path edit rule to `deny` while preserving the plan-path Bash denial,
human-authorized `pbcopy`, every configured MCP permission, root `ask` behavior,
and access to `implementation-worker` for non-plan bounded work. Remove the
`planning-coordinator` Task edge and do not add a `plan-orchestrator` edge. Keep
unrelated valid research and critic edges unless another existing invariant
requires their change.

The Lead prompt must say that it never writes, updates, executes, or implements a
plan. When a request asks it to create, update, execute, or implement planned work
or supplies a plan path, it directs the user to
`/start-work <request-or-plan-path>` instead of bypassing the Plan Orchestrator.
This guardrail does not remove the Lead's direct authority for ordinary unplanned
work.

The ERB stays read-only and must never execute or implement a plan. Remove its
plan `Ready`/`Ready With Revisions`/`Not Ready` decisions, implementation
`Approve`/`Approve With Follow-ups`/`Request Changes` decisions, structured
durable review-record language, and any suggestion that review gates execution.
Its plan and implementation commands remain optional advice, followed by the
same `/start-work <plan-path>` route when the human wants changes or execution.

Update the Worker prompt so it may receive one bounded implementation unit from
the Lead for unplanned work or from the Plan Orchestrator for planned work. It
reports acceptance and validation evidence to its caller, but cannot edit plans,
change checkboxes or sidebar state, delegate, commit, push, deploy, perform
destructive migrations, or broaden scope.

### Command and manifest inventory

Delete `/prepare-work`, `/record-plan-review`, `/revise-plan`, `/approve-plan`,
`/normalize-plan`, and `/execute-plan` without aliases. Add only `/start-work`.
Retain `/convert-tapestry-plan`, optional `/review-plan`, optional
`/review-implementation`, `/audit-technical-debt`, and
`/investigate-regression`; the two unrelated ERB commands remain byte-unchanged.

The resulting sorted manifest contains exactly 23 agents and 6 commands.
`plan-orchestrator.md` replaces `planning-coordinator.md`, so the agent count does
not change. Command ownership is:

- `plan-orchestrator`: `start-work`, `convert-tapestry-plan`;
- `engineering-review-board`: `review-plan`, `review-implementation`,
  `audit-technical-debt`, `investigate-regression`.

Every command keeps `subtask: false`. Keep the cleanup checklist unchanged.

### Native TODO sliding window

Add flat `todowrite: allow` to the Plan Orchestrator's permission map and
recognize that tool in validator policy. Do not give the Lead or Worker explicit
planned-work sidebar authority. Keep the Lead's `pbcopy`, every configured MCP
prefix, plan-path Bash denial, and all unrelated permission behavior unchanged.

The Plan Orchestrator treats plan checkboxes as the durable work contract and
native TODOs as a transient view:

1. Every `todowrite` call supplies the complete visible list because the call
   replaces, rather than patches, session TODOs.
2. Display at most five items and exactly zero or one `in_progress` item.
3. At start, select the current executable unchecked step, mark it
   `in_progress`, and follow it with up to four `pending` steps.
4. During execution, show the most recently accepted `completed` item first, the
   current `in_progress` item second, and then the next `pending` items, capped at
   five.
5. Each content string is `<step>. <summary>`, retains the original plan step
   number after earlier items leave the window, and limits `<summary>` to 30
   characters excluding the numeric prefix.
6. On resume, re-read the plan and acceptance evidence, treat checked items as
   complete, select the current unchecked step, and rebuild the whole window.
   Do not treat a stale sidebar as durable history or reconstruct old completed
   entries merely for display.
7. On a blocker or failed attempt, leave the current plan checkbox unchecked,
   keep at most that step `in_progress`, retain only the latest accepted
   completion when relevant, and report the blocker. Never batch or infer
   completions.
8. Only the Plan Orchestrator checks a plan TODO after the step's acceptance
   evidence and all required validation succeed. Worker completion reports are
   input evidence, not authority to update the plan or sidebar.
9. After the final step succeeds, briefly replace the sidebar with only that
   final `completed` item, then call `todowrite` with `todos: []` before the final
   report. No active, pending, or stale completed item remains.

OpenCode does not enforce the list-size, active-count, or summary-length rules.
The repository enforces them as prompt contracts and focused mutation tests; it
must not claim that native UI behavior supplies those constraints.

## Alternatives and Trade-offs

- **Retain the Coordinator, persisted review, or approval as optional modes:**
  rejected by the human. Keeping dormant lifecycle concepts would preserve the
  same ceremony and ambiguity under different wording.
- **Store review-advice levels or ERB findings in plans:** rejected. Review is
  out-of-band and advisory; durable storage would recreate state and gating.
- **Rewrite existing plans into the lean shape:** rejected. Historical files are
  left intact, continue to reserve their numbers, and receive successors only on
  demand.
- **Keep removed commands as aliases:** rejected. A minimal command surface is a
  stated objective, and aliases would perpetuate obsolete workflows.
- **Copy Weave's rolling-window machinery:** rejected. Native `todowrite` already
  provides replace-in-order and clear behavior; prompt policy and tests cover the
  repository-specific limits without plugin state.
- **Give the Lead plan-path Bash access:** rejected. Direct edit-tool writes are
  sufficient and preserve the existing defense-in-depth boundary, at the cost of
  blocking when an edit tool cannot create a required parent safely.

## Dependencies

`depends_on` is empty. `opencode-01` reserves sequence `01` but is neither an
execution prerequisite nor a source plan for this work. The implementation is
one coordinated repository change: prompt, command, manifest, validator, test,
and synchronized documentation changes must agree before rollout.

Within execution, `tools/opencode_manager.py` and
`tests/test_opencode_manager.py` have shared ownership and must be changed
serially or by one Worker. Root and project-template README/template pairs must
be updated together. Command deletion/addition and manifest inventory changes
must land together. No package, service, live OpenCode configuration, plugin, or
external repository is an implementation dependency.

## Specialist Contributions

- `technical-researcher` established native `todowrite` replacement, order,
  clear, and status behavior; confirmed that OpenCode does not enforce the
  requested five-item, one-active-item, or summary-length limits; and separated
  useful prompt policy from Weave-specific plugin machinery.
- `architecture-strategy-critic` recommended direct Lead plan writes, retirement
  of the Coordinator, retention of Worker and independent ERB boundaries,
  removal of lifecycle-only commands, and preservation of path, delegation, Git,
  destructive-action, validation, and machine-local configuration safeguards.
  Its recommendation to remove Tapestry conversion was superseded by the
  human's explicit decision to keep `/convert-tapestry-plan`.

## Risks and Guardrails

- Removing lifecycle metadata must not be replaced with hidden status fields,
  filename conventions, persisted review records, or command aliases.
- Lean plans can become vague if context and acceptance are over-pruned. Keep
  decision-relevant findings and real dependencies while excluding recoverable
  inventories and history.
- Direct Lead writes concentrate authority. Preserve series validation,
  max-plus-one allocation, gap non-reuse, collision/exhaustion checks, symlink
  containment, edit-tool-only writes, rereading, and plan-path Bash denial.
- Legacy detection must fail closed. Never mutate or execute a verbose plan as if
  it were lean, and never infer a dependency from sequence order.
- Optional review must not become an implicit gate through wording such as
  “ready,” “approved,” “signed off,” or “required before execution.”
- Native TODO state is session-scoped and replace-all. Never use it as history,
  claim it persists plan truth, or let stale completed items survive a successful
  final report.
- Prompt tests can protect repository instructions but cannot prove OpenCode UI
  enforcement. Keep claims bounded to the supplied native behavior.
- Preserve exact surviving runtime Task IDs, one-level delegation, ERB
  independence, Lead `pbcopy` and configured MCP permissions, Worker denials,
  Git safety, destructive-action stops, and machine-local configuration rules.
- Keep unrelated specialist prompts, audit/regression commands, the cleanup
  checklist, skill files, dependencies, and live config untouched.

### Execution stop conditions

Stop and return to the Lead if:

- repository drift after execution starts overlaps an owned file, or execution
  would modify `opencode-01`;
- any proposed new-plan shape adds a section or metadata outside the closed
  contract;
- implementation would retain or recreate approval, sign-off, lifecycle state,
  revision transitions, persisted review, normalization, or compatibility
  aliases;
- safe direct Lead writes require plan-path Bash access, cannot prove containment,
  collide, exhaust a series, or cannot create the destination parent with an
  available edit tool;
- a legacy plan would be rewritten or executed rather than succeeded;
- the ERB would become a Lead Task child or regain a readiness/approval decision;
- TODO prompt/tests cannot distinguish start, transition, resume,
  blocked/failure, final completion, and clearing, or would claim unsupported UI
  enforcement;
- a permission change removes/downgrades Lead `pbcopy` or configured MCP access,
  weakens Worker/Git/destructive safeguards, or changes live machine-local
  configuration; or
- root and project-template plan files cannot remain byte-identical.

## Implementation Sequence

### 1. Replace the documented plan contract

**Objective:** Define the lean format and direct-author workflow in every
authoritative and copied guide.

**Scope and stable interfaces:** Update `AGENTS.md`, `README.md`,
`docs/implementation-plans/README.md`,
`docs/implementation-plans/TEMPLATE.md`,
`docs/engineering-agent-governance.md`, and the synchronized files under
`opencode/project-template/`. Preserve canonical path/series allocation,
machine-local configuration boundaries, ERB independence, and byte equality for
the README/template pair.

**Dependencies:** None. Apply each root/project-template pair as one unit.

**Acceptance criteria:**

- The template contains one title and exactly the authorized sections, with
  numbered checkbox TODOs and no frontmatter or lifecycle/history content.
- Guidance explains direct Lead create/update, conversational plan changes,
  legacy succession, retained Tapestry conversion, optional review advice, and
  non-executable legacy shapes.
- No active guide describes review, approval, sign-off, revision, normalization,
  or execution history as plan state.
- Root and project-template README/template copies are byte-identical.

**Validation:** Run plan-template contract and synchronization tests, inspect
local links, and run `just validate-opencode` plus `just validate`.

### 2. Simplify runtime roles and permissions

**Objective:** Make the Lead the safe direct plan writer while preserving
implementation and independent-review boundaries.

**Scope and stable interfaces:** Update
`opencode/agents/engineering-lead.md`,
`opencode/agents/implementation-worker.md`, and
`opencode/agents/engineering-review-board.md`; delete
`opencode/agents/planning-coordinator.md`. Remove only the Coordinator Task edge,
add flat `todowrite: allow` to the Lead, retain the Lead's plan edit rule at
`ask`, and preserve every authorized MCP prefix, `pbcopy`, plan Bash deny,
surviving exact Task ID, one-level delegation rule, and Worker restriction.

**Dependencies:** Step 1 defines the contract these prompts implement.

**Acceptance criteria:**

- The Lead can create/update/check plan TODOs directly through edit tools and
  owns sidebar updates, with the complete safe-path and post-write checks.
- The Coordinator file and Lead Task edge are absent; no substitute planning
  role or recursive delegation is added.
- The Worker reports bounded acceptance/validation evidence and cannot edit the
  plan/sidebar, delegate, commit, push, or use plan-path Bash.
- The ERB remains primary/read-only and returns advisory findings without plan
  readiness or implementation approval/sign-off decisions.
- `todowrite: allow`, `pbcopy`, configured MCP prefixes, and all unrelated
  permission actions validate exactly.

**Validation:** Add permission, Task-topology, removed-agent, Worker-denial, and
ERB advisory-contract mutations; run the focused manager tests and
`just validate-opencode`.

### 3. Replace the plan command surface

**Objective:** Expose only the six selected plan commands and remove lifecycle
ceremony.

**Scope and stable interfaces:** Add `opencode/commands/create-plan.md` and
`opencode/commands/update-plan.md`; rewrite `convert-tapestry-plan.md`,
`review-plan.md`, `execute-plan.md`, and `review-implementation.md`; delete
`prepare-work.md`, `record-plan-review.md`, `revise-plan.md`, `approve-plan.md`,
and `normalize-plan.md`. Update `opencode/manifest.json` atomically with those
file changes. Leave the unrelated audit/regression definitions and cleanup
checklist untouched.

**Dependencies:** Steps 1 and 2 establish format and authority.

**Acceptance criteria:**

- Create/update/convert/execute are Lead-owned; both optional reviews and the two
  unrelated commands remain ERB-owned; every command keeps `subtask: false`.
- Create/update enforce safe direct writes, allocation/collision rules,
  rereading, and conversational update behavior. Update creates a successor for
  a legacy target rather than modifying it.
- Tapestry conversion remains available, revalidates the source, emits only lean
  content, and preserves the source without provenance metadata in the plan.
- Execution has no review/approval/lifecycle gate, rejects legacy shape, and
  applies the complete checkbox/sidebar evidence contract.
- Review commands are read-only advice with no durable record, readiness,
  approval, sign-off, or mandatory next gate.
- The manifest is sorted and contains exactly 22 agents and 8 commands; removed
  files and aliases are absent.
- Audit/regression commands and the cleanup checklist are byte-unchanged.

**Validation:** Add command-owner/inventory and prompt-contract mutations,
validate removed-command absence in changed workflow files, then run the focused
manager suite and `just validate-opencode`.

### 4. Rebase validator and fixtures on the lean contract

**Objective:** Make repository validation reject regressions to lifecycle
ceremony and protect the direct-Lead permissions and command inventory.

**Scope and stable interfaces:** Update `tools/opencode_manager.py` and
`tests/test_opencode_manager.py`. Replace lifecycle-oriented
`PLAN_TEMPLATE_TOKENS`, `PLAN_TEMPLATE_HEADINGS`, and fixture content with the
closed lean shape; recognize and require the Lead's flat `todowrite` permission;
remove Coordinator-specific ownership cases; retain support-file safety,
frontmatter parsing, manifest, synchronization, permission-ordering, command
owner, Task, setup/verify/uninstall, and Markdown-fence coverage.

**Dependencies:** The exact prompts, command inventory, and template from steps
1 through 3. One Worker owns both files or changes them serially.

**Acceptance criteria:**

- Removing any required lean heading/label or numbered checkbox example fails;
  adding frontmatter, lifecycle metadata, or removed history headings fails.
- Root/template drift and symlinked support/root plan files still fail closed.
- The Lead must have flat `todowrite: allow`, configured MCP access, `pbcopy`,
  plan edit `ask`, and the required plan-path Bash deny; Coordinator expectations
  are gone and Worker expectations remain.
- Manifest and command tests accept only the selected assets/owners and catch a
  removed command/agent reappearing or a new alias.
- Existing non-plan validator and installer behavior remains covered.

**Validation:** Run the focused unit test file after each contract group, then
`just validate-opencode`.

### 5. Prove the TODO window and execution transitions

**Objective:** Protect the transient sidebar behavior without inventing native
UI guarantees.

**Scope and stable interfaces:** Add focused prompt-contract cases in
`tests/test_opencode_manager.py` for the Lead and `/execute-plan` definitions.
Use deterministic plan-step examples and validate the contract text/associations,
not a simulated OpenCode plugin.

**Dependencies:** Steps 2 through 4 provide permission, prompts, and test
helpers.

**Acceptance criteria:**

- Start shows one current `in_progress` item followed by at most four pending
  items in source order.
- Transition shows only the latest accepted completed item first, current item
  second, and following pending items up to five.
- Resume rebuilds from plan/evidence with original step numbers and does not
  treat sidebar state as history.
- Blocked/failure leaves the current checkbox unchecked, never batch-completes,
  and keeps zero or one active item.
- Every content value follows `<step>. <summary>` with a summary of at most 30
  characters excluding the prefix.
- Final success writes only the last completed item, then `todos: []`, before the
  final report.
- Mutations to replacement semantics, order, count, active count, statuses,
  numbering, length, evidence ownership, or final clear fail with focused
  diagnostics.

**Validation:** Run the TODO prompt-contract cases alone, the complete focused
manager suite, and `just validate-opencode`. Report that runtime UI behavior was
not integration-tested unless separate target-machine evidence is supplied.

### 6. Reconcile and validate the complete workflow

**Objective:** Finish with one internally consistent lean workflow across the
files authorized by this plan.

**Scope and stable interfaces:** Re-read every changed document, template,
agent, command, manifest entry, validator rule, and test fixture. Inspect the
full diff and status. Exclude grandfathered plan files from stale-reference
cleanup and confirm `opencode-01` has no change.

**Dependencies:** Steps 1 through 5 complete without a stop condition.

**Acceptance criteria:**

- Active docs/definitions agree on the closed shape, direct Lead authority,
  optional advisory review, six-command plan surface, legacy succession,
  Tapestry conversion, and transient TODO behavior.
- No changed workflow file retains the Coordinator or removed lifecycle
  commands; grandfathered plans and explicitly excluded files remain untouched.
- Agent/command counts, owners, exact Task edges, plan permissions, MCP/clipboard
  access, Worker restrictions, and root/project-template synchronization match
  this plan.
- All required checks pass, or the Lead reports the exact failure and stops
  before rollout.

**Validation:** Execute Final Verification, inspect the diff for unrelated
changes and unsupported OpenCode claims, and request optional ERB implementation
review only at the human's chosen advice level.

## Test Strategy

Use the existing standard-library `unittest` temporary-repository fixtures and
mutation style. Keep tests deterministic and local; do not invoke OpenCode,
network services, MCP servers, live configuration, or Weave.

Required groups are:

- **Lean template:** exact allowed title/section labels, numbered checkboxes,
  forbidden frontmatter/lifecycle/history content, and root/template byte sync.
- **Authority and inventory:** Coordinator removal, 22-agent/8-command manifest,
  surviving exact IDs, command ownership, one-level Task graph, direct Lead plan
  edit contract, and unchanged Worker/ERB boundaries.
- **Permissions:** flat Lead `todowrite: allow`, retained `pbcopy` and all MCP
  prefixes, plan edit `ask`, plan-path Bash denial, and Worker Git/destructive/
  plan/delegation denials.
- **Plan operations:** series validation, max-plus-one with gap non-reuse,
  exhaustion/collision stops, symlink/containment checks, rereading,
  conversational lean updates, legacy succession, and lean Tapestry output.
- **Review semantics:** all three advice levels are defined out-of-band; plan and
  implementation reviews remain optional/read-only and emit no readiness,
  approval, sign-off, persistence, or execution gate.
- **Execution/TODO behavior:** start, transition, resume, blocked/failure,
  evidence-gated checkbox completion, final completed-only write, and final
  clear, including count/order/status/number/length mutations.
- **Compatibility:** retained support-file, frontmatter-parser, manifest,
  Markdown-fence, setup, verify, uninstall, and unrelated command behavior.

Tests of prompt contracts show that checked-in guidance contains the required
rules; they do not prove runtime compliance or native UI constraints. Preserve
that distinction in diagnostics and reports.

## Migration, Compatibility, and Recovery

This is an intentional workflow break with no compatibility aliases. Existing
plan files remain where they are and reserve their sequence numbers. Create a
lean successor only when a legacy plan needs changes or execution; never rewrite
or execute the predecessor. Newly converted Tapestry sources follow the same
allocation rules and remain intact after conversion.

Roll out agents, commands, manifest, validator/tests, docs, and project-template
copies as one validated repository change. The linked OpenCode definitions take
effect after restart. Do not create a lean plan under partially updated runtime
definitions, and do not modify live configuration during rollout.

If validation fails before restart, recover by reverting only this coordinated
implementation as one unit; do not restore ceremony through aliases or alter a
legacy plan. If definitions were already loaded, restore a coherent reviewed
repository state and restart OpenCode again. No database, persisted review
record, plugin state, credential, or external service needs migration or
rollback.

## Documentation Impact

- `AGENTS.md` and `README.md`: replace Coordinator/lifecycle language with direct
  Lead authoring, lean execution, optional review, and legacy succession.
- `docs/implementation-plans/{README,TEMPLATE}.md`: become the authoritative
  closed contract and exact starter shape.
- `docs/engineering-agent-governance.md`: update roles, Task topology, command
  ownership, review advice, execution, and Lead/Worker/ERB boundaries.
- `opencode/project-template/`: mirror portable workflow guidance and keep both
  plan files byte-identical to root copies.
- Agent and command Markdown: implement direct plan authority, optional advisory
  review, legacy handling, and the native TODO prompt contract.

`docs/skill-taxonomy.md` and `docs/cross-reference-map.md` require no edit: this
work changes OpenCode runtime governance, not first-party skill inventory or
skill routing.

## Final Verification

From the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_opencode_manager.py' -v
just validate-opencode
just validate
just check
git diff --check
```

Then:

- re-read root and project-template plan README/template files and confirm the
  validator reports byte equality;
- inspect the manifest and definition directories for exactly 22 agents and 8
  commands with no retired file or alias;
- search changed workflow docs, agents, commands, manager code, and tests for
  Coordinator and removed-command references; do not rewrite grandfathered plans
  or explicitly excluded files;
- inspect Lead/Worker permission ordering and confirm `todowrite`, `pbcopy`, MCP,
  plan-edit, plan-Bash, Git, destructive, and Task rules match this plan;
- inspect prompt-contract evidence for every TODO transition and verify no test
  claims native enforcement of repository-only limits;
- confirm the implementation's changed-file evidence shows no write to
  `docs/implementation-plans/plans/opencode/01-agent-definitions-improvement-program.md`,
  live config, credentials, dependencies, skills, unrelated specialist prompts,
  audit/regression commands, or the cleanup checklist; and
- report any target-machine OpenCode restart or runtime sidebar check as skipped
  unless it was actually observed.

## Open Decisions

None. The human fixed the lean section set, direct Lead authority, role and
command removals, optional review model, retained Tapestry conversion, legacy
successor behavior, and native TODO window contract.

## ERB Review History

None.

## Approval History

None.

## Amendments

None.

## Execution Record

None.
