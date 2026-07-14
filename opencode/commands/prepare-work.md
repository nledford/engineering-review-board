---
description: Classify work and choose the lightest safe execution or durable-plan workflow
agent: engineering-lead
subtask: false
---

Assess this work request:

$ARGUMENTS

Read applicable guidance and inspect enough evidence to classify it as Trivial,
Bounded, Complex, or Ambiguous / High-Risk. Do not implement in this command.

For Complex work, choose a series matching `[a-z][a-z0-9-]{1,19}`, gather only
decision-relevant evidence, and invoke `planning-coordinator` to create a
canonical plan at `docs/implementation-plans/plans/<series>/<NN>-<slug>.md`.
The Coordinator—not the Lead—allocates `max(existing)+1` from `01` through `99`,
never reuses gaps, and persists draft/pending revision `1` metadata. Return the classification,
evidence, unresolved decisions, plan path when created, and next command
(`/review-plan <path>`).
