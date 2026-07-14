---
description: Normalize a legacy implementation plan into the canonical series and sequence format
agent: engineering-lead
subtask: false
---

Normalize the existing implementation plan at:

`$1`

into the plan series:

`$2`

## Arguments

- `$1`: Existing plan path
- `$2`: Destination series key

Example:

`/normalize-plan docs/implementation-plans/add-schema-cache.md db`

Expected destination shape:

`docs/implementation-plans/plans/db/04-add-schema-cache.md`

## Objective

Move and normalize an existing implementation plan into the canonical plan
structure without changing its underlying engineering intent.

The canonical location is:

`docs/implementation-plans/plans/<series>/<NN>-<slug>.md`

The canonical plan ID is:

`<series>-<NN>`

This command reorganizes and normalizes a plan. It does not implement the plan,
approve it, or perform a complete Engineering Review Board review.

## Required Preflight

Before changing files:

1. Read the complete source plan.
2. Read all applicable `AGENTS.md` files.
3. Read:
   - `docs/implementation-plans/README.md`
   - `docs/implementation-plans/TEMPLATE.md`
4. Confirm that `$1`:
   - exists
   - is a Markdown file
   - is inside the current repository
   - appears to be an implementation plan
5. Validate `$2` as a series key.

The series key must:

- contain one lowercase token
- begin with a letter
- contain only lowercase letters and digits
- contain between 2 and 12 characters
- represent one coherent, ordered initiative

Valid examples:

- `db`
- `forms`
- `auth`
- `shell`
- `search`

Invalid examples:

- `Database`
- `db-schema`
- `db_schema`
- `1db`
- `all`

If the series is invalid, ambiguous, or appears unrelated to the plan, stop and
ask the user to choose a valid series.

## Existing Status Safeguards

Determine the plan's current status.

### Draft

Normalization may proceed.

### Under Review

Normalization may proceed, but:

- reset `status` to `draft`
- reset `review_decision` to `pending`
- preserve the previous review history
- record that the path changed during review
- recommend a fresh `/review-plan`

### Approved

Do not move or rename the plan without explicit human confirmation.

Explain that changing the stable path may invalidate links from reviews, issues,
commands, or implementation records.

After confirmation:

- preserve `status: approved`
- preserve the approval history
- record the normalization as an amendment
- recommend confirming the plan again before execution

### In Progress

Do not move or rename the plan without explicit human confirmation.

Before proceeding, inspect:

- current implementation commits
- references to the existing path
- execution records
- active branches or worktrees
- commands or automation using the old path

Preserve execution evidence and record the move.

### Completed, Superseded, or Abandoned

Leave the plan at its historical path unless the user explicitly requests
historical normalization.

Do not reorganize historical records merely for cosmetic consistency.

## Detect Existing Canonical Identity

Inspect the plan for existing metadata such as:

- `plan_id`
- `series`
- `sequence`
- `depends_on`
- `renamed_from`
- `source_plan`

If the plan is already stored at:

`docs/implementation-plans/plans/<series>/<NN>-<slug>.md`

and its metadata agrees with its path, stop and report that it is already
normalized.

If its path and metadata disagree, treat that as a consistency problem. Do not
silently choose one as authoritative.

## Allocate the Sequence Number

Use this destination directory:

`docs/implementation-plans/plans/$2/`

Create it when it does not exist.

Scan existing Markdown filenames matching:

`^[0-9]{2}-.*\.md$`

Determine the highest existing two-digit sequence number and allocate the next
number.

Examples:

- No existing plans → `01`
- Highest existing plan is `03` → `04`
- Existing plans are `01`, `02`, and `04` → `05`

Do not:

- fill numbering gaps
- reuse abandoned numbers
- renumber existing plans
- reorder approved or completed plans
- allocate more than one plan in this series concurrently

If the next number would exceed `99`, stop and ask the user how to reorganize
the series.

## Derive the Plan Slug

Derive a concise kebab-case slug from, in priority order:

1. The plan's explicit title
2. Its first level-one heading
3. Its existing filename

The slug must:

- describe the plan's implementation outcome
- omit dates and sequence numbers
- avoid vague words such as `changes`, `updates`, or `misc`
- remain reasonably short
- contain lowercase letters, numbers, and hyphens only

Do not change the plan's product or engineering intent merely to produce a
cleaner filename.

## Confirm the Destination

Construct:

- `plan_id`: `$2-<NN>`
- destination path:
  `docs/implementation-plans/plans/$2/<NN>-<slug>.md`

Before moving the file:

1. Confirm that the destination does not exist.
2. Confirm that no other plan uses the resulting `plan_id`.
3. Search for exact references to the source path.
4. Identify references that will need updating.
5. Show the proposed old path, new path, and plan ID.

If there is a collision, stop. Do not choose another name silently.

## Move the Plan

Honor the active OpenCode runtime permission policy.

For a tracked source file, prefer a version-control-aware move such as
`git mv`.

For an untracked source file, use an appropriate filesystem move.

Do not:

- copy the plan and leave two active copies
- delete the original before confirming the destination is valid
- overwrite an existing plan
- modify unrelated files
- commit the move unless the user separately requested a commit

## Planning Coordinator Assignment

After the file has moved, delegate the normalized plan-content update to
`planning-coordinator`.

Provide the Planning Coordinator with:

- old path
- new path
- exact `plan_id`
- series
- sequence
- source plan content
- current status
- applicable project guidance
- existing dependency metadata
- references that may require updating
- an instruction to edit only the normalized plan file

The Planning Coordinator must not delegate to other agents.

## Required Metadata

Ensure the normalized plan contains YAML frontmatter with at least:

```yaml
---
plan_id: <series>-<NN>
series: <series>
sequence: <integer>
title: <human-readable title>
status: <existing or adjusted status>
review_decision: <existing or adjusted decision>
depends_on: []
renamed_from:
  - <old path>
created: <preserve original value when known>
updated: <current date>
---