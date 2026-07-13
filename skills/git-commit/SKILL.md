---
name: git-commit
description: Write high-quality git commits and commit messages. Use when the user asks to commit changes, split a working tree into logical commits, improve commit messages, prepare reviewer-friendly history, or apply Conventional Commits guidance in any plain git repository.
---

# Git Commit Quality

Use this skill to produce clean, maintainable, reviewer-friendly `git`
history. Prefer several well-scoped commits over one large mixed-purpose commit
when the working tree contains separable changes.

## Core Principles

- Make each commit atomic: one coherent change, one reason, one review unit.
- Make commits logical: related files and tests belong together; unrelated work
  does not.
- Make commits reviewable: a reviewer should understand the intent from the
  commit message and confirm it from the diff.
- Make history useful later: future readers should understand what changed and
  why without reverse-engineering every line.
- Follow local repository conventions over generic advice when they are clear.
- Do not create commits unless the user or active workflow authorizes commits;
  otherwise propose grouping and draft messages.

## Scope and Routing

Use this skill to construct new commits: inspect changes, choose logical groups,
stage intentionally, validate, write messages, commit when authorized, and report
the result.

Use [`git-workflows`](../git-workflows/SKILL.md) for amend/fixup and autosquash,
branch switching, merge or rebase, cherry-pick, revert or reset, conflict and
reflog recovery, fetch/pull/push, remotes, tags, and worktrees. Authorization to
commit never authorizes those operations or a push.

Load [`security-review`](../security-review/SKILL.md) and
[`security-review-evidence`](../security-review-evidence/SKILL.md) when a commit
surface includes secrets, credentialed URLs, signing trust, untrusted hooks or
configuration, or other security boundaries. Use
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
for submodule, hook-tool, dependency, vendored-source, or provenance review.

## Workflow

1. Detect repository conventions.
   - Inspect recent history, for example `git log --oneline -10`.
   - Check project docs such as contributing guides, commit templates, hook
     configuration, or release notes when present.
   - Check established commit-signing and signoff policy. Follow it without
     changing key or trust configuration merely to complete the commit.
   - In an unfamiliar repository, inspect the effective hook source before the
     first commit. Treat hooks and `core.hooksPath` as executable configuration;
     stop when provenance is unclear and do not bypass trusted hooks merely to
     make a commit succeed.
   - Prefer existing style, casing, type names, scopes, ticket references, and
     body/footer conventions.
   - Do not introduce a new convention into an established repository without a
     clear reason.

2. Inspect the working tree.
   - Review `git status --short` before staging.
   - Review unstaged changes with `git diff` and staged changes with
     `git diff --staged`.
   - Identify generated files, lockfiles, snapshots, vendored files,
     dependency updates, `.gitmodules`, submodule gitlinks, local machine files,
     editor state, and other artifacts that need extra care.
   - Never stage secrets, credentials, private keys, environment files with real
     values, generated junk, or unrelated artifacts.
   - If a secret may already be staged, committed, reflog-reachable, or pushed,
     stop without printing it. Determine the exposure class, rotate or revoke
     first, and coordinate any history rewrite or remote cleanup through the
     security skills.

3. Choose commit groups.
   - Commit after a coherent unit of work is complete.
   - Avoid committing unrelated changes together.
   - Avoid committing broken code unless the repository explicitly uses
     checkpoint or WIP commits.
   - Separate formatting-only changes from behavior changes when practical.
   - Separate refactors from feature or bug-fix changes when practical.
   - Separate dependency updates from code changes when practical.
   - Separate tests from implementation when that improves reviewability; keep
     them together when the tests are the best evidence for the same behavior
     change.
   - Use partial staging, such as `git add -p`, when a file contains unrelated
     edits that belong in different commits.
   - Do not use reset, restore, checkout, clean, stash, amend, or rebase to make
     grouping easier unless that exact operation is separately requested and
     handled through `git-workflows`.

4. Validate before committing.
   - Run the most relevant available formatter, linter, typecheck, build, or
     test command when practical.
   - If full validation is too expensive, run focused checks for the changed
     area and remember the limitation for the final summary.
   - Before every commit, check `git diff --staged` and confirm only intended
     files are staged.

5. Write the commit message.
   - Use a concise subject line; aim for about 50 characters when practical and
     avoid exceeding 72 without a good reason.
   - Use imperative mood where appropriate: `Add`, `Fix`, `Refactor`, `Remove`,
     `Document`, `Update`.
   - Explain what changed and why. The diff shows how.
   - Add a body when context, rationale, tradeoffs, side effects, migration
     notes, or notable implementation details matter.
   - Separate subject, body, and footers with blank lines.
   - Wrap body text around 72 characters when practical.
   - Avoid vague subjects such as `updates`, `misc`, `fix stuff`, `changes`,
     `wip`, or `temp` in durable history.

6. Report the result.
   - Summarize what was committed and why the grouping was chosen.
   - Include commit hashes when available.
   - State validation performed and any validation limitations.
   - Redact credentialed URLs, secrets, private keys, and sensitive hook output.

## Conventional Commits

Conventional Commits is a recommended structured format when a repository uses
it or when no local convention conflicts with it. It is not an unconditional
requirement.

Format:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

Use scopes to name the affected area when helpful and consistent with the
project, for example `fix(parser): handle empty input`.

Breaking changes:

- Add `!` after the type or scope, such as `feat(api)!: require signed tokens`.
- Add a `BREAKING CHANGE:` footer explaining what changed and how users should
  adapt.
- Use either form when local convention allows it; use both when extra clarity
  helps.

Example:

```text
fix(cache): prevent stale entries after rename

Renaming an item updated the primary record but left the old cache key in
place. Invalidate both keys so subsequent reads cannot return stale metadata.
```

Load [`references/commit-examples.md`](references/commit-examples.md) when the
task needs type selection, breaking-change examples, message comparisons, or a
worked mixed-tree grouping example.

## Pre-Commit Checklist

- Local convention checked.
- Working tree inspected.
- Signing/signoff policy and effective hooks checked when applicable.
- Commit grouping chosen and unrelated edits kept out.
- Secrets, local files, generated junk, and unintended artifacts excluded.
- Lockfiles, generated files, snapshots, vendored files, and dependencies are
  included only when intentional and explained by the commit.
- Submodule gitlinks and `.gitmodules` reviewed when present.
- Relevant validation run, or limitation recorded.
- Staged diff reviewed.
- Commit message explains what changed and why.
- Final response will summarize commits, hashes, validation, and limitations.

## When to Ask the User

Ask for clarification only when the desired grouping is genuinely ambiguous or
risky, for example:

- The working tree contains unrelated user changes and it is unclear what may be
  committed.
- A generated file, lockfile, snapshot, vendored file, or dependency update looks
  accidental.
- The repository convention conflicts with the user's requested message style.
- The user requested a single commit, but the changes are clearly separable and
  mixing them would make review or revert materially worse.
- Hook provenance is unclear, signing policy cannot be satisfied safely, or a
  secret may already exist in Git history or a remote.

Otherwise, proceed with the safest coherent non-destructive grouping and explain
the choice. Do not push or rewrite history as part of a commit request.
