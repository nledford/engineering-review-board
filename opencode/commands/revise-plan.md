---
description: Revise an implementation plan from ERB findings
agent: engineering-lead
subtask: false
---

Revise the implementation plan located at:

$ARGUMENTS

## Objective

Update the plan to address the most recent Engineering Review Board decision
and accepted findings.

This is a controlled plan revision. Do not implement source-code changes.

## Required Preflight

Before modifying the plan:

1. Read the entire plan.
2. Read all applicable `AGENTS.md` and project guidance.
3. Locate the most recent ERB review associated with the plan.
4. Confirm that the review decision is:
   - `Ready With Revisions`, or
   - `Not Ready`
5. Identify:
   - required revisions
   - advisory recommendations
   - rejected recommendations
   - unresolved human decisions
6. Inspect the current repository when a finding depends on repository state.
7. Confirm that the plan has not already entered implementation.

If no ERB review can be found, stop and request either:

- the review report path, or
- explicit revision instructions from the user.

Do not infer missing Board findings.

## Revision Classification

Classify each ERB finding as one of:

- Accepted — must be incorporated
- Accepted with modification — incorporate the intent using a better approach
- Rejected by human decision — preserve the decision and rationale
- Already addressed — cite the existing plan section
- Requires clarification — do not guess
- Obsolete due to repository drift

Do not silently omit a required finding.

## Specialist Clarification

The Engineering Lead may invoke a registered specialist only when:

- an ERB finding is ambiguous
- repository state has materially changed
- two accepted recommendations conflict
- a revision requires current technical evidence

Use the minimum sufficient specialists.

The Planning Coordinator must not delegate to other agents.

## Planning Coordinator Assignment

Delegate the plan rewrite to `planning-coordinator`.

Provide:

- exact plan path
- latest ERB review
- classification of every finding
- repository evidence
- applicable project guidance
- accepted constraints
- explicit non-goals
- unresolved decisions
- instruction to modify only the plan file

## Revision Rules

Preserve unless explicitly changed:

- original objective
- approved product intent
- valid guardrails
- valid non-goals
- provenance metadata
- prior review history
- existing amendments
- completed execution evidence

Update where required:

- scope
- proposed design
- implementation sequence
- dependencies
- acceptance criteria
- validation commands
- migration strategy
- rollback or roll-forward strategy
- test strategy
- documentation impact
- risks and trade-offs

Do not:

- broaden scope merely because a reviewer identified nearby work
- convert advisory findings into mandatory work without justification
- remove guardrails to simplify execution
- rewrite history
- delete earlier ERB reviews
- mark the plan approved
- begin implementation

## Amendment Record

Add an amendment entry:

### Amendment — <current date>

**Reason:** ERB review revision

**Source Review:** <review date or reference>

**Changes Made:**

- <finding and corresponding plan change>

**Recommendations Not Applied:**

- <recommendation and rationale>

**Open Decisions:**

- <unresolved decision>

## Status Update

After revision:

- set `status: draft` or `status: under-review`
- set `review_decision: pending`
- update `updated`
- preserve previous review decisions in the review-history section
- do not set `status: approved`

## Verification

After the Planning Coordinator completes the edit, the Engineering Lead must:

1. Re-read the revised plan.
2. Map each required ERB finding to a concrete plan change.
3. Confirm no unrelated scope was introduced.
4. Confirm guardrails and non-goals remain intact.
5. Confirm unresolved decisions are explicit.
6. Confirm the plan remains internally coherent.
7. Recommend running `/review-plan` again.

## Required Output

Return:

- revised plan path
- findings addressed
- findings accepted with modification
- findings rejected by explicit human decision
- findings requiring clarification
- sections changed
- scope changes
- unresolved decisions
- recommendation to rerun `/review-plan`

Do not implement the plan.
Do not mark the plan approved.