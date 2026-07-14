---
plan_id: <series>-<NN>
series: <series>
sequence: <integer>
title: <human-readable title>
status: draft
revision: 1
review_decision: pending
reviewed_at:
approved_at:
approved_revision:
depends_on: []
baseline_commit: <commit or null>
execution_owner: engineering-lead
source_format: native
source_plan:
created: YYYY-MM-DD
updated: YYYY-MM-DD
completed_at:
---

# <SERIES>-<NN> — <Title>

## Executive Summary

## Problem and Context

## Objectives

## Non-Goals

## Applicable Project Guidance

## Current-State Evidence

## Proposed Design

## Alternatives and Trade-offs

## Dependencies

`depends_on` in frontmatter is authoritative. Explain only validated dependency
relationships here; leave uncertain ones in Open Decisions.

## Specialist Contributions

List only exact agent IDs actually consulted and their material contributions.

## Risks and Guardrails

## Implementation Sequence

### 1. <Bounded work unit>

**Objective:**

**Scope and stable interfaces:**

**Dependencies:**

**Acceptance criteria:**

**Validation:**

## Test Strategy

## Migration, Compatibility, and Recovery

## Documentation Impact

## Final Verification

## Open Decisions

## ERB Review History

Every actionable entry is persisted through `/record-plan-review` and binds the
exact plan path, ID, revision, and baseline.

### Review — <ISO-8601 date/time>

- Plan path:
- Plan ID:
- Revision:
- Baseline commit:
- Decision: `ready` | `ready-with-revisions` | `not-ready`
- Findings:
- Next command:

## Approval History

### Approval — <ISO-8601 date/time>

- Authorized by: explicit human `/approve-plan`
- Plan ID / revision / baseline:
- ERB review record:

## Amendments

## Execution Record
