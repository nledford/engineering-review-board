# Complete the OpenCode Plan Workflow Migration

## TL;DR

Finish the active governance and validation migration so the repository consistently uses the lean Plan Orchestrator workflow and rejects stale lifecycle guidance.

## Context

**Original request:**

Complete and execute the remaining OpenCode planned-work workflow migration.

**Key repository findings:**

- The lean plan contract, Plan Orchestrator runtime, trusted helper, three-link installer, and six-command route are present.
- Active repository guidance still names the retired Planning Coordinator and deleted lifecycle commands.
- The validator does not yet scan the closed active-workflow inventory for the retired token set while excluding immutable plans, tests, and historical records.
- The current Plan Orchestrator can coordinate implementation but hard-denies Git inspection, staging, and commits, while the Worker is intentionally forbidden to commit.
- OpenCode 1.18.1 permission patterns cannot escape literal `*` or `?`, so exact-path staging relies on a runtime approval gate plus the validated prompt contract rather than an unrepresentable static glob deny.

**Dependencies:**

- Reconcile the current worktree before edits and retain the available trusted-helper installation throughout execution.
- After validating a checked-in permission change, restart OpenCode and explicitly recover the retained lock only after confirming that no planned mutator remains.

## Objectives

- Make all active governance agree on the lean Plan Orchestrator workflow and optional advisory review model.
- Add deterministic validation for stale lifecycle tokens over only the closed active-workflow inventory.
- Prove the completed migration with focused and repository-wide validation.
- Grant the Plan Orchestrator narrow commit-only Git authority for explicitly authorized planned work.
- Package all resulting dirty files into atomic logical commits.

## Guardrails

- Preserve existing legacy plans byte-for-byte and exclude plan history, tests, fixtures, and archived material from stale-token scanning.
- Preserve the 23-agent, six-command, one-helper inventory; exact Task boundaries; Worker restrictions; and the Lead's existing MCP, clipboard, Git, and unplanned-TODO permissions.
- Do not add compatibility aliases, lifecycle metadata, approval gates, dependencies, skills, providers, credentials, or live machine-local configuration changes.
- Keep root and project-template plan guidance synchronized and limit edits to the Plan Orchestrator definition, active governance, validator, and validator-test surfaces.
- Allow only safe Git inspection, approval-gated explicit-path staging, and bare staged-index commits; require fresh exact quoted paths in the prompt contract and keep representable unsafe forms, fetch, push, amend, hook bypass, history/ref/worktree mutation, and shell composition denied.
- Do not amend, rewrite history, bypass hooks, or stage files outside the verified migration scope.

## Deliverables

- Updated active repository and project-template governance for the lean workflow.
- A closed active-workflow inventory and exact retired-token diagnostics in the OpenCode validator.
- Focused mutation and exclusion tests for every retired token and inventory boundary.
- Checked-in Plan Orchestrator permission, prompt, validator, and test coverage for narrow commit-only Git authority.
- Atomic logical commits containing every verified dirty file.

## Definition of Done

- Active guidance consistently routes planned work through top-level `/start-work`, reserves plan/state/TODO execution for the Plan Orchestrator, and treats ERB review as optional read-only advice.
- Validation reports the exact active file and retired token, while immutable plans, tests, fixtures, and historical records remain valid exclusions.
- Effective permission and prompt tests prove the Plan Orchestrator can inspect, approval-gate exact staging, and create a bare commit while non-exact staging is prohibited by contract and risky Git plus all remote/history/worktree mutation remain gated or denied.
- Required focused, repository-only, and configured-workstation checks pass without changing either existing legacy plan.
- Every intended dirty file is committed in a logical group and the worktree is clean.

## TODOs

1. [x] Reconcile remaining active governance with the lean Plan Orchestrator workflow.
2. [x] Add closed-inventory stale-token validation and focused mutation/exclusion tests.
3. [x] Run final focused, repository-wide, and configured-install verification and resolve scoped failures.
4. [x] Add narrow Plan Orchestrator commit-only Git authority with validator and test coverage.
5. [x] Restart OpenCode and recover the retained lock after explicit no-mutator confirmation.
6. [ ] Create atomic logical commits for every verified dirty file.

## Verification

- `python3 -m unittest discover -s tests -p 'test_opencode_manager.py' -v`
- `python3 -m unittest discover -s tests -p 'test_start_work_state.py' -v`
- `just lint`
- `just test`
- `just validate`
- `just validate-opencode`
- `just verify-opencode`
- `just check`
- `git diff --check`
- `git status --short`
- `git diff --cached`
- `git log --oneline -10`
