---
description: Safely normalize a legacy plan into the canonical series layout without changing intent
agent: engineering-lead
subtask: false
---

Normalize `$1` into series `$2` without implementing or approving it.

`$2` must match `[a-z][a-z0-9-]{1,19}`. Read the entire source, applicable
guidance, and the implementation-plan README/template. Stop if the source is
already canonical and consistent, identity is ambiguous, the destination would
collide, the sequence is exhausted, or historical normalization lacks the
required explicit human confirmation. Approved, in-progress, completed,
superseded, and abandoned sources require explicit human confirmation before a
path change. Do not silently renumber any plan.

Reject symlinked plan roots, sources, destination parents, or destinations, and
block when the series maximum is `99`.

This is structural migration, not redesign. Preserve original objective, context,
evidence, valid deliverables, guardrails, non-goals, implementation sequence,
acceptance criteria, test strategy, review history, amendments, execution
records, provenance, known `created`, and valid dependencies. Update `updated`;
never fabricate a creation date, implementation commit, or validation result.
Add YAML frontmatter when absent, append rather than replace `renamed_from`, and
normalize the first heading to `# <SERIES>-<NN> — <Title>` using an uppercase
visible series key. Only change metadata, heading, path, path references, status
safeguards, and a normalization amendment. Do not mark the plan approved.

When the path or identity changes, a draft, under-review, approved, in-progress,
or blocked source becomes `draft`/`pending` at an incremented or initialized
revision; clear `reviewed_at`, `approved_at`, and `approved_revision`, while
preserving prior review, approval, amendment, and execution records as history.
Completed, superseded, and abandoned plans retain their terminal status and
history but must not expose an old-path approval as currently executable.

Use a two-phase, rollback-safe process:

1. Inspect source status, metadata, dependencies, exact references, and series
   maximum. Preserve known `created`, provenance, review/execution history,
   objectives, guardrails, valid `depends_on`, and prior amendments.
2. Delegate destination creation and structural normalization to
   `planning-coordinator`. It allocates max+1, writes
   `docs/implementation-plans/plans/<series>/<NN>-<slug>.md`, adds canonical
   metadata, appends `renamed_from` and a normalization amendment, and leaves
   the source intact.
3. Re-read and verify destination path, ID, sequence, heading, frontmatter,
   content preservation, duplicate-ID absence, lifecycle reset, and exact
   references. Update eligible non-plan references only after verification;
   report uncertain, historical, generated, vendored, or archived references.
4. Invoke `planning-coordinator` a second time to finalize plan-contained
   references and remove the source only after successful verification and any
   required explicit human confirmation. If the source is outside the
   Coordinator's edit boundary, leave it intact and report the exact
   human-authorized removal action. Do not delete first.

Return source/destination, identity, status before/after, metadata corrections,
references updated/deferred, dependency decisions, intentional non-changes,
skipped validation, residual risk, and `/review-plan <destination>`.
