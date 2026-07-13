# Git Operation Matrix

Load this reference only when selecting or verifying a specific Git operation.
Repository policy and the core workflow in
[`../SKILL.md`](../SKILL.md) remain authoritative.

## Branches and Paths

| Goal | Prefer | Check First | Important Caveat | Verify |
| --- | --- | --- | --- | --- |
| Create or change branches | `git switch` | Status, detached state, target branch, other worktrees | Available in Git 2.23 and newer; a branch is normally checked out in only one worktree | Current branch, status, upstream |
| Restore tracked worktree content | `git restore` | Diff, source tree, affected paths, untracked obstructions | Defaults to the index unless `--staged` is used; tracked paths absent from the source may be removed | Diff and status |
| Restore index content | `git restore --staged` | Staged diff and source | Defaults to `HEAD`; does not mean the same thing as worktree restoration | Staged and unstaged diffs |
| Use legacy branch/path command | `git checkout` | Whether the token names a branch or path | Multiplexes branch switching and path replacement; use `--` for path disambiguation | Branch, diff, status |
| Temporarily set tracked and selected untracked work aside | `git stash` only when authorized | Staged, unstaged, untracked, and ignored state | Default behavior does not include every untracked or ignored file; a stash changes repository state and can conflict when reapplied | Stash list, status, reapplied diff |
| Remove untracked files | `git clean` only when explicitly authorized | Untracked and ignored files, nested repositories, dry-run output | Removal is not recovered by reflog; `-x` also selects ignored files | Status and expected filesystem state |

Official references: [`git-switch`](https://git-scm.com/docs/git-switch),
[`git-restore`](https://git-scm.com/docs/git-restore), and
[`git-checkout`](https://git-scm.com/docs/git-checkout),
[`git-stash`](https://git-scm.com/docs/git-stash), and
[`git-clean`](https://git-scm.com/docs/git-clean).

## History Inspection and Diagnosis

| Goal | Prefer | Caveat | Verify |
| --- | --- | --- | --- |
| Inspect commits and topology | `git log` and `git show` | Choose ranges, paths, and graph options that answer the question; do not assume chronological display proves ancestry | Relevant commits and changed paths |
| Find line provenance | `git blame` | Records the last associated commit for lines, not personal fault or root cause; moves and copies may need explicit options | Commit context and surrounding history |
| Find a regression boundary | `git bisect` | Requires a reliable good/bad observation; skipped commits can leave multiple possible first bad commits | Reproduce on the reported boundary and reset the session |

Official references: [`git-log`](https://git-scm.com/docs/git-log),
[`git-show`](https://git-scm.com/docs/git-show),
[`git-blame`](https://git-scm.com/docs/git-blame), and
[`git-bisect`](https://git-scm.com/docs/git-bisect).

## Remotes and Synchronization

| Goal | Prefer | Check First | Important Caveat | Verify |
| --- | --- | --- | --- | --- |
| Create, track, or rename a branch | `git switch -c` or focused `git branch` operations | Existing refs, target name, upstream, other worktrees | Tracking configuration and branch names are separate from remote refs; renaming a local branch does not rename a remote branch | `git branch -vv`, current branch, upstream |
| Delete a local branch | `git branch -d` when merged; `-D` only when explicitly authorized | Reachability, unmerged commits, branch reflog, other worktrees | Forced deletion ignores merge safety and deletes the branch reflog; it does not delete the remote branch | Local refs and preserved commits |
| Set or remove an upstream | Focused `git branch --set-upstream-to` or `--unset-upstream` | Intended local branch and remote-tracking ref | Upstreams affect argument-less pull and push behavior but do not create or delete the remote ref | `git branch -vv` and relevant configuration |
| Add, rename, remove, or change a remote | Focused `git remote` operation | Fetch and push URLs, refspecs, credentials, affected tracking refs | Removing a remote deletes its configuration and remote-tracking refs; fetch and push URLs may differ but must identify the same repository, so use separate remotes for upstream and publishing repositories; never expose credential-bearing URLs | Sanitized remote names, refspecs, and tracking refs |
| Update a remote or remote group | Explicit `git remote update <group-or-remote>` | `remotes.<group>`, `remotes.default`, each remote's `skipDefaultUpdate`, refspecs, and prune intent | Omitting the target can fetch every eligible remote; `--prune` prunes across every remote selected for the update | Updated and pruned refs for every affected remote |
| Preview and prune stale remote-tracking refs | `git remote prune --dry-run` before an authorized prune | Remote refspecs, local-only refs, tag mappings | Pruning affects remote-tracking refs and can affect locally stored tags under some refspecs; it does not delete branches on the remote | Remaining refs and expected tags |
| Inspect remote state without integrating | `git fetch` | Remote, refspec, credential exposure | Updates remote-tracking refs according to configured refspecs; does not update the working branch | Remote-tracking refs and fetched commits |
| Fetch and integrate | `git pull` only under repository policy | Dirty state, upstream, pull/rebase/ff configuration | Pull is fetch plus integration; do not assume `origin/main` or a universal merge/rebase policy | History topology, diff, tests |
| Publish refs | `git push` only when authorized | Destination remote/refspec, upstream, server protection | Argument-less behavior depends on configuration; a commit request does not authorize a push | Intended remote ref |
| Rewrite a remote ref | Explicit lease after coordination | Fresh remote state and expected object ID | Plain `--force` removes safeguards; tracking-ref leases can be undermined by background fetches | Server ref equals intended object ID |

Official references: [`git-branch`](https://git-scm.com/docs/git-branch),
[`git-remote`](https://git-scm.com/docs/git-remote),
[`git-fetch`](https://git-scm.com/docs/git-fetch),
[`git-pull`](https://git-scm.com/docs/git-pull), and
[`git-push`](https://git-scm.com/docs/git-push).

## Integration, Rewriting, and Undo

| Goal | Operation | History Effect | Safety Rule |
| --- | --- | --- | --- |
| Preserve branch topology | Merge | May create a merge commit | Inspect both tips and validate the integrated result |
| Produce combined content without merge topology | Squash merge | Does not record `MERGE_HEAD` or create the merge commit automatically | Do not describe it as preserving the branch relationship |
| Replay commits on another base | Rebase | Creates replacement commits | Require explicit authorization for shared or published commits |
| Fold fixup commits during rebase | `commit --fixup` plus rebase autosquash | Reorders and combines specially named commits | Confirm targets and final history; autosquash recognizes `fixup!`, `squash!`, and `amend!` forms |
| Apply selected commits | Cherry-pick | Creates new commits from selected changes | Start clean and review merge-commit mainline selection when applicable |
| Undo published changes | Revert | Creates inverse commits | Merge reverts require deliberate mainline selection and affect future merges |
| Move a ref or reset index/worktree | Reset | Mode determines which state is replaced | `--hard` overwrites tracked state and may remove obstructing untracked paths; require explicit authorization |

Official references: [`git-merge`](https://git-scm.com/docs/git-merge),
[`git-rebase`](https://git-scm.com/docs/git-rebase),
[`git-commit`](https://git-scm.com/docs/git-commit),
[`git-cherry-pick`](https://git-scm.com/docs/git-cherry-pick),
[`git-revert`](https://git-scm.com/docs/git-revert), and
[`git-reset`](https://git-scm.com/docs/git-reset).

## Conflicts and Recovery

| State | Available Decisions | Caveat |
| --- | --- | --- |
| Merge stopped | Continue after resolution, abort, or quit as supported | Abort may not reconstruct pre-existing uncommitted work |
| Rebase stopped | Continue, abort, skip, or quit | Skipping intentionally drops the current patch from the replay |
| Cherry-pick or revert stopped | Continue, abort, or quit; skip where supported | Confirm which sequencer operation owns the state |
| Ref moved or commit abandoned | Inspect reflog and relevant recovery refs | Reflogs are local and expire; they are not backups |
| Untracked file removed | Restore from an external backup if one exists | Reflog does not preserve arbitrary untracked file contents |

Official references: [`git-merge`](https://git-scm.com/docs/git-merge),
[`git-rebase`](https://git-scm.com/docs/git-rebase),
[`git-cherry-pick`](https://git-scm.com/docs/git-cherry-pick),
[`git-revert`](https://git-scm.com/docs/git-revert), and
[`git-reflog`](https://git-scm.com/docs/git-reflog).

## Tags, Worktrees, and Submodules

| Surface | Guidance |
| --- | --- |
| Release tags | Prefer annotated tags when release metadata matters; follow local signing policy; verify signatures when policy requires it; push tags explicitly and never silently replace a published release tag |
| Worktrees | Use for concurrent branch work without disturbing the current tree; inspect `git worktree list`; check for submodules first because Git recommends against multiple superproject checkouts when submodules are present; worktrees with submodules cannot be moved and require `--force` for removal, which needs explicit authorization |
| Submodules | Cover only when present; the superproject records a gitlink commit; inspect `.gitmodules`, source URLs, pinned commits, detached state, local changes, and recursive push requirements |

Official references: [`git-tag`](https://git-scm.com/docs/git-tag),
[`git-worktree`](https://git-scm.com/docs/git-worktree), and
[`gitsubmodules`](https://git-scm.com/docs/gitsubmodules).

## Trust Boundaries

- Hooks may execute during commit, merge, rebase, checkout, and push workflows.
  Inspect [`githooks`](https://git-scm.com/docs/githooks) and effective
  `core.hooksPath`; do not normalize bypassing hooks.
- Scope repository ownership exceptions narrowly. See
  [`safe.directory`](https://git-scm.com/docs/git-config#Documentation/git-config.txt-safedirectory).
- If history contains a secret, rotate or revoke it before coordinated rewrite
  and hosting cleanup. Do not recommend `git filter-branch`; its own
  [warning](https://git-scm.com/docs/git-filter-branch#_warning) recommends safer
  alternatives and explains rewrite hazards.
