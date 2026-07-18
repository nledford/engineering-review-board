---
description: "Audit, apply, or locally tag a Semantic Versioning release."
agent: engineering-lead
subtask: false
---

You are handling this current command turn as the Engineering Lead. Earlier
Engineering Review Board or Plan Orchestrator output, when present, came from a
different primary agent and remains context only; it does not transfer that
agent's identity or permissions to this turn.

Never claim that the Engineering Review Board or Plan Orchestrator is selected,
and do not ask the human to select the Engineering Lead while this command is
running. Before refusing on role-authority grounds, reconcile the request against
the active Engineering Lead contract.

This invocation authorizes only the work belonging to the one explicitly
selected mode below. It does not transfer authority between modes or authorize a
commit, remote mutation, publication, deployment, or final ship decision.

Use exactly one mode per invocation:

- `/semver audit [scope or instructions]`
- `/semver apply [recommended|<version>] [scope or instructions]`
- `/semver tag [recommended|<version>] [scope or instructions]`

Handle this request:

$ARGUMENTS

Treat the first argument as the mode. If it is missing, unsupported, ambiguous,
or combined with a side effect owned by another mode, show the valid syntax and
stop before mutation. Do not silently turn `apply` into `tag`, perform an
apply-and-tag release sequence, or infer `commit`, `push`, `publish`, or `deploy`
authority from release-oriented language.

Load `semantic-versioning` for every valid mode. Read applicable `AGENTS.md`
guidance and inspect repository release policy, package metadata, release
documentation, automation, and validation commands before making
repository-specific claims. Load matching language or package-workflow skills
when metadata mechanics require them. Load `api-design` when compatibility of a
public API, SDK, CLI, schema, webhook, or event contract needs focused analysis.
Checked-in release automation changes route to `ci-release-engineering`; final
ship-or-hold decisions route to `release-readiness` and are outside this command.

## Shared evidence rules

- Identify the release unit, version policy, declared public contract,
  supported consumers, canonical version source, synchronized mirrors, current
  released baseline, and intended release target from fresh repository evidence.
- Treat any earlier version recommendation as context only. Re-audit the current
  baseline-to-target delta before recommending, applying, or tagging a version;
  `recommended` never means blindly reuse a prior answer.
- Inspect the complete material delta, not only commit subjects or Conventional
  Commit labels. State whether uncommitted work is included in or excluded from
  the audit target.
- Let the highest compatibility impact determine the minimum honest bump. Keep
  `0.x`, prerelease, monorepo, dependency, de facto behavior, and non-SemVer
  policy uncertainty explicit.
- Preserve unrelated work. Stop before mutation when release-unit scope,
  authoritative metadata, target version, compatibility impact, dirty-file
  ownership, or repository policy is materially ambiguous.
- Never reuse a released version or claim that choosing a version makes the
  release ready to ship.

## Audit mode

Audit mode is read-only. Inspect the released baseline through the intended
target, classify every material public-contract change, and recommend the
smallest honest next version with confidence and assumptions. When audit scope
does not identify a target, inspect the released baseline through `HEAD` and
report release-relevant staged and unstaged changes separately. Do not edit,
create, delete, rename, format, stage, commit, tag, push, publish, deploy, or
create or mutate a durable plan or `.erb/plan-state.json`.

## Apply mode

Apply mode authorizes version-metadata edits and their repository-native
validation only. Recompute the recommendation from fresh evidence before
editing. When no exact version is supplied, apply only the freshly computed
recommendation. For an explicit version, validate SemVer syntax and compare it
with the fresh minimum recommendation: refuse an under-bump, and identify any
deliberate over-bump as a separate repository-policy choice rather than a SemVer
requirement.

Inspect the working tree, update only the selected release unit's canonical
version source and required synchronized mirrors, and run the strongest relevant
metadata, lockfile, package-build, stale-version, and focused test checks. Do not
stage, commit, tag, push, publish, or deploy in apply mode. Report that a later
tag operation is invalid until the applied metadata is intentionally committed.

## Tag mode

Load `git-workflows` before any tag operation. Tag mode authorizes creation of
one local release tag only. It does not authorize version edits, staging, a
release commit, remote updates, publication, deployment, or tag replacement.
With no version operand in tag mode, use only the single unambiguous canonical
version recorded at `HEAD`.

Before creating the tag, require `git status` to show no staged, unstaged, or
untracked paths, then use fresh evidence to verify all of the following:

- `HEAD` is the exact intended release commit;
- the canonical version metadata at `HEAD` equals the target Semantic Version;
- the target version is not lower than the fresh minimum recommendation from the
  complete released-baseline-to-`HEAD` audit;
- repository policy or established history unambiguously supplies the tag name,
  including any `v` prefix, tag type, message convention, and signing policy;
  and
- neither the release version nor any equivalent release tag already exists
  locally or in the inspected publication evidence.

If applied metadata is uncommitted, stop and explain that the human must
explicitly request and review a commit before invoking tag mode. Do not edit
version metadata, stage, commit, push, publish, or deploy in tag mode. Never
create, move, replace, delete, or force a pre-existing tag. Create no tag when
the naming, target, signing, publication, or compatibility evidence is
ambiguous.

Honor the Engineering Lead's runtime approval policy for `git tag`. After local
creation, verify that the new tag resolves to the exact intended `HEAD` and that
its embedded or associated version matches the canonical metadata. Never push
the tag; a remote tag update requires a separate explicit human request and is
not part of `/semver tag`.

## Report

Report the selected mode, release unit, baseline, target, policy, public contract
and consumers considered, dominant compatibility impact, confidence, assumptions,
and validation actually observed. For apply mode, list changed files and checks.
For tag mode, list the local tag and verified target commit without exposing
sensitive remote data. Explicitly identify every requested or customary release
side effect that was not performed and any residual risk.
