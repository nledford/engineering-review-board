---
name: git-workflows
description: Safe Git branch, remote, history-inspection, integration, rewrite, conflict, recovery, tag, and worktree workflows. Use when switching or restoring, fetching/pulling/pushing, managing upstreams or remotes, inspecting history with log/blame/bisect, merging/rebasing/squashing/cherry-picking/reverting/resetting, resolving conflicts, recovering with reflog, or managing tags and worktrees. Do not use for commit grouping or message drafting, checked-in CI/release automation, code review, GitHub pull-request operations, or release-readiness decisions.
---

# Git Workflows

Use this skill for repository-state operations beyond constructing a new commit.
Preserve unrelated work, inspect local policy before acting, and make the exact
side effect explicit before running a mutating command.

Use [`git-commit`](../git-commit/SKILL.md) to group, stage, validate, and describe
new commits. Load [`security-review`](../security-review/SKILL.md) and
[`security-review-evidence`](../security-review-evidence/SKILL.md) when secrets,
credentialed remotes, signing trust, untrusted hooks or configuration, or other
security boundaries are involved. Use
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
for submodule, downloaded hook tooling, vendored-source, or provenance questions.

## Core Rules

- Follow repository instructions, contributing docs, branch protections, hooks,
  signing rules, and established integration policy over generic advice.
- Distinguish `HEAD`, the index, the working tree, local refs, remote-tracking
  refs, and remote refs. Do not describe `reset`, `restore`, and `checkout` as
  interchangeable.
- Distinguish uncommitted work, local-only commits, shared commits, and published
  refs before rewriting or discarding anything.
- Never infer authorization to push, force-push, delete refs, rewrite history, or
  discard files from a request to commit, update, merge, or fix code.
- Preserve unrelated user changes. Do not hide them with an unrequested stash,
  temporary commit, branch switch, worktree removal, or cleanup command.
- Prefer reversible operations, but do not promise recovery. Reflogs are local,
  expire, and do not restore arbitrary untracked files removed from disk.
- Treat command output and remote URLs as potentially sensitive. Report
  sanitized refs and outcomes instead of credentials or private host details.

## Workflow

1. Inspect policy and repository state.
   - Read relevant repository instructions and contributing or release docs.
   - Check `git --version` before relying on version-sensitive commands.
   - Inspect status, current branch or detached `HEAD`, staged and unstaged
     changes, recent history, upstream configuration, and relevant worktrees.
   - Inspect remotes only when needed and do not print credential-bearing URLs.
   - In unfamiliar repositories, inspect effective hook and configuration
     sources before an operation that can execute hooks.

2. Define the intended outcome.
   - Separate branch or path switching from content restoration.
   - Separate downloading remote state from integrating it: `fetch` updates
     remote-tracking information; `pull` fetches and then integrates.
   - Choose whether history should preserve topology, replay commits, produce a
     squashed result, create an inverse commit, or move a ref.
   - For diagnosis, decide whether the task needs history inspection, line
     provenance, or a reproducible good/bad search before choosing log, blame, or
     bisect. Do not use blame to assign personal fault.
   - Determine whether affected commits or refs are already shared or published.

3. Protect current work.
   - Start from a clean state when the chosen operation requires it.
   - If work is present, stop and decide whether it belongs in a commit or an
     explicitly authorized stash. A separate worktree can isolate a different
     branch task, but it does not transfer staged, unstaged, or untracked changes
     from the current tree. Do not choose silently.
   - Check untracked and ignored files before restore, reset, clean, checkout,
     worktree removal, or submodule recursion. Reflog cannot recover all of them.
   - Check for submodules before adding, moving, or removing worktrees. Git's
     multiple-worktree support for submodules is incomplete; do not create
     multiple superproject checkouts when submodules are present.
   - When leaving detached `HEAD`, preserve wanted commits with an intentional
     branch or tag first.

4. Choose the narrowest operation.
   - Prefer `switch` for branch changes and `restore` for path or index content on
     Git 2.23 or newer. Retain `checkout` awareness for older repositories and
     ambiguous branch/path syntax; use `--` to disambiguate paths.
   - Follow repository policy when selecting merge, rebase, squash, or
     fast-forward-only integration. Do not impose a universal pull strategy.
   - Prefer `revert` for undoing published changes. Use reset or rebasing only
     when moving or rewriting refs is the intended and authorized result.
   - Use cherry-pick for selected commits, not as a default substitute for a
     repository's normal integration workflow.
   - Treat tags as published release identifiers when repository policy does.
     Do not silently replace a published tag.
   - Use bisect only with a reproducible test or observation, mark untestable
     commits as skipped, record the first bad commit as evidence rather than the
     root cause, and reset the bisect session when finished.

5. Confirm risky side effects.
   - Require explicit authorization for worktree or index discard, destructive
     cleanup, history rewriting, branch or tag deletion, remote updates, and
     forced ref changes.
   - Preview the target ref, source commit, affected paths, and remote state
     before acting. Use dry-run behavior where the command supports it.
   - Never use plain `--force` as routine guidance. `--force-with-lease` is a
     guard, not coordination; forms that rely on remote-tracking refs can be
     undermined by background fetches. Prefer an explicit expected object ID for
     a separately authorized critical rewrite.
   - Do not bypass hooks with `--no-verify` merely to make an operation succeed.

6. Handle stopped operations deliberately.
   - Identify whether merge, rebase, cherry-pick, or revert owns the current
     conflict state before choosing continue, abort, skip, or quit.
   - Resolve content and semantic conflicts, then run focused validation for the
     integrated result. Compilation alone may not detect an incorrect merge.
   - Do not use `reset --hard` as generic conflict cleanup. An abort may also be
     unable to reconstruct pre-existing uncommitted work.

7. Verify and report.
   - Recheck status, diffs, recent history, branch/upstream state, tags, and
     worktrees relevant to the operation.
   - For remote changes, verify the intended remote ref instead of assuming a
     successful local command proves the server state.
   - Report the operation, affected refs or paths, validation, and remaining
     risks. Never expose secrets, credentialed URLs, private keys, or sensitive
     hook output.

## Worktree Decision And Lifecycle

- Use a linked worktree when genuine concurrent branch work or a separate clean
  checkout must proceed without disturbing a worktree that remains in use.
  Prefer the current worktree for ordinary edits on the current task and branch.
- Existing dirty work remains in its original worktree. Transfer it only through
  a separate, explicitly chosen commit, patch, or authorized stash workflow.
- Before adding a worktree, inspect `git worktree list`, relevant worktree statuses,
  submodules, the target path, the intended commit or branch, and whether that
  branch is already checked out. A branch is normally checked out in only one
  worktree.
- Specify branch intent. Without a commit-ish or explicit `-b`, `-B`, or
  `--detach`, `git worktree add <path>` may create a branch named after the final
  path component. Disclose the new directory, branch or detached state, and
  linked-worktree metadata before creation.
- Worktrees share repository objects and refs while keeping separate working
  files, `HEAD`, and indexes. A ref update in one worktree can affect what the
  others observe even though their uncommitted files remain separate.
- Remove a clean linked worktree with `git worktree remove`; do not delete its
  directory as the normal cleanup path. Forced removal of an unclean, locked, or
  submodule-bearing worktree can discard work and requires explicit authorization.
- Use `lock` for a worktree on storage that may be temporarily unavailable,
  `prune` for stale administrative records after a worktree is already missing,
  and `repair` for inconsistent metadata such as a manually moved worktree. Do
  not use them as interchangeable cleanup commands.

## Security and Supply-Chain Escalation

- If a secret may be staged, committed, reflog-reachable, or pushed, stop. Do not
  print it. Determine the exposure class, rotate or revoke first, and coordinate
  any history rewrite or remote cleanup through the security skills.
- Treat hooks and `core.hooksPath` as executable configuration. Do not trust or
  run unfamiliar hooks, hook managers, or downloaded helpers without review.
- Never solve repository ownership warnings by setting `safe.directory=*`.
  Scope any trust exception to a repository that policy intentionally trusts.
- Treat changed `.gitmodules`, submodule URLs, gitlinks, and pinned submodule
  commits as dependency provenance. Sanitize credential-bearing URLs.
- Follow established signing policy. Do not change key, trust, or signature
  configuration merely to complete a Git operation.

## Detailed Operation Guidance

Load [`references/operation-matrix.md`](references/operation-matrix.md) when the
task needs command-specific selection, abort/recovery behavior, or upstream
documentation links. Keep the core workflow above active for every operation.

## Do Not Use For

- Grouping a working tree into commits or writing commit messages; use
  `git-commit`.
- Reviewing code, deciding whether a pull request should merge, or deciding
  whether a release should ship.
- GitHub issue, pull-request, review, or repository-administration APIs.
- Editor workspaces or generic orchestration across unrelated repositories.
- Checked-in CI or automated release publication where Git is only one pipeline
  step; use [`ci-release-engineering`](../ci-release-engineering/SKILL.md).
- Docker/OCI or Compose configuration; use
  [`container-engineering`](../container-engineering/SKILL.md). Other deployment
  systems require their applicable platform or repository-specific guidance.

## Handoff Checklist

- Repository policy and Git version checked.
- Current work, detached state, upstreams, remotes, and publication state scoped.
- Exact side effect and authorization confirmed.
- Unrelated changes and sensitive output preserved.
- Conflict, abort, and recovery path understood before mutation.
- Resulting refs, status, diffs, and relevant validation verified.
- Commands, outcomes, limitations, and residual risk reported safely.
