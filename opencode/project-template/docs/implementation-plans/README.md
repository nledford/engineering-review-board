# Implementation Plans

This directory holds durable, project-local plans. They are authored and updated
only by the Planning Coordinator through the Engineering Lead; the Engineering
Review Board is read-only.

## Canonical Location and Identity

Plans live at:

```text
docs/implementation-plans/plans/<series>/<NN>-<slug>.md
```

- `series` matches `[a-z][a-z0-9-]{1,19}`.
- `NN` ranges from `01` through `99` and is the series maximum plus one. Gaps and
  retired numbers are never reused; a series whose maximum is `99` is exhausted.
- `plan_id` is `<series>-<NN>` and must match the path and metadata.
- Filename order is descriptive. `depends_on` is the authoritative prerequisite.

## Required Metadata

Every plan includes `plan_id`, `series`, `sequence`, `title`, `status`,
`revision`, `review_decision`, `reviewed_at`, `approved_at`,
`approved_revision`, `depends_on`, `baseline_commit`, `execution_owner`,
`created`, `updated`, and `completed_at`. Converted or normalized plans also
preserve `source_format` and `source_plan` when relevant.

Allowed statuses are `draft`, `under-review`, `approved`, `in-progress`,
`blocked`, `completed`, `superseded`, and `abandoned`. Allowed review decisions
are `pending`, `ready`, `ready-with-revisions`, and `not-ready`.

## Lifecycle

1. `/prepare-work <request>` classifies work and creates a draft when durable
   planning is warranted.
2. `/review-plan <path>` produces a read-only ERB record for the exact path, ID,
   revision, and baseline. Multiple plans receive independent records.
3. `/record-plan-review <path> [review-evidence]` verifies and persists that
   structured record through the Coordinator. Revision and approval always
   consume this latest matching durable record, so the workflow survives session
   boundaries.
4. `/revise-plan <path>` makes material corrections, increments revision, clears
   approval metadata, and returns the plan to review.
5. `/approve-plan <path>` records explicit human authorization only after the
   latest persisted ERB record is `ready`. Approval metadata updates do not
   increment revision.
6. `/execute-plan <path>` requires ready review state, matching approval at the
   current revision, unchanged/re-reviewed baseline, and all dependencies
   completed. The Lead uses bounded implementation workers; the Coordinator
   persists lifecycle and execution records.
7. `/review-implementation <path>` provides independent completion review.

Material changes increment `revision`, reset review/approval fields, preserve
history, and require review plus explicit approval again. Metadata-only lifecycle
updates do not increment revision.

Path permissions are defense in depth, not a sandbox against hostile repository
content or runtime bugs. Before any durable write, reject symlinked plan roots or
destination components and verify that the resolved destination remains under
`docs/implementation-plans/`. Do not cross the boundary with an apply-patch move,
shell redirection, alternate path spelling, or symlink alias.

## Conversion and Normalization

Use `/convert-tapestry-plan <source> <series>` for legacy Tapestry plans. The
source is revalidated and provenance is preserved; the converted plan begins
draft/pending at revision 1.

Use `/normalize-plan <source> <series>` for structural migration. It is two
phase: the Coordinator writes the destination first, the Lead verifies it and
non-plan references, then a second Coordinator task finalizes plan references and
removes an in-boundary source only after success and any required human
confirmation. Path-changing normalization resets current approval for draft or
active plans; terminal history remains non-executable. Historical plans are never
silently renumbered.

Use [TEMPLATE.md](TEMPLATE.md) for new project-local plan files.
