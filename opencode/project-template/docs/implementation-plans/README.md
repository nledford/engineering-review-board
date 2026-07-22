# Implementation Plans

Use this contract for project-local implementation plans that must survive a
pause, context reset, or OpenCode restart. Prefer direct implementation when
scope, safety, and validation are already adequate. Complexity may justify a
planning recommendation, never automatic plan creation.

## Canonical Paths

Use one plan at:

```text
.erb/plans/<slug>.md
```

Use a series only when work needs separately managed plan documents:

```text
.erb/plans/<subject>/<NN>-<slug>.md
```

A single plan has no subject directory or numeric prefix. A series uses one
contained subject and zero-padded numbers from `01` through `99`. Allocate the
maximum number among live files plus one. Multiple TODOs in one bounded plan do
not justify a series.

## Canonical Format

Plans contain no frontmatter or lifecycle metadata. Use the exact ordered
headings and fixed Context labels in [`TEMPLATE.md`](TEMPLATE.md). TODO and
Verification entries are numbered Markdown checkboxes. Create every checkbox
unchecked.

Active plan prose and structure are immutable by default. During execution, only
an evidenced `[ ]` to `[x]` checkbox change is allowed. Do not add, remove,
rewrite, reorder, or renumber plan content during `/start-plan`.

A current explicit `/update-plan <exact-plan-path>` request may update one active
plan in place without executing it. Completed plans remain immutable. New
checklist entries stay unchecked, unchecked entries never become checked during
an update, and checked entries remain checked only when their obligation and the
surrounding acceptance contract are materially unchanged and fresh evidence
still supports them.

## Checklist Entry Contract

This contract applies whenever a plan is created, reviewed, updated, or
executed.

- Every TODO or Verification entry has one atomic purpose: one finite,
  observable outcome with focused completion evidence. Tightly coupled actions
  may share an entry only when they are inseparable from that outcome; split
  unrelated, multi-phase, or independently verifiable work.
- Every entry must be executable from satisfied external dependencies,
  repository state, and completed earlier entries. Put prerequisites before
  dependents. An entry must not depend on itself or a later checklist entry, and
  the plan must contain no dependency cycle or mutually waiting steps.
- Disclose any known ask-gated or destructive operation and its exact contained
  target in the entry text when repository evidence supports it. If none is
  disclosed, no special permission is expected. This planning disclosure is not
  approval; execution reclassifies the actual operation against current runtime
  policy.
- Give every entry a finite completion or stop condition. Do not encode an
  unbounded retry, polling, or correction loop. Blocked, denied, pending, failed,
  or replay-uncertain work remains unchecked and follows the execution rules
  below.

## Human-Controlled Lifecycle

The workflow has four routes:

1. The Engineering Lead implements directly when normal scope, safety, and
   validation are adequate.
2. An explicit human `/create-plan` request creates and persists a plan only.
   It does not execute TODOs.
3. An explicit human `/update-plan <exact-plan-path>` request updates one active
   plan in place without changing state or executing TODOs.
4. A separate human `/start-plan <existing-plan-path>` request executes an
   existing canonical plan. With no path, `/start-plan` resumes the plan
   selected in `.erb/plan-state.json`.

The Lead or ERB may recommend top-level `/consult-plan` for read-only advice,
stating the reason, trade-off, and proposed scope. The human decides whether to
create, update, or execute a plan.

## Plan State

The only durable workflow state is `.erb/plan-state.json`:

```json
{"plan_path":".erb/plans/<path>.md"}
```

It stores exactly one repository-relative canonical plan path. It does not store
status, current step, history, hashes, ownership, or concurrency data.

Derive state from the selected plan:

- Active means at least one TODO or Verification checkbox is unchecked.
- The current step is the first unchecked checkbox in document order.
- Complete means every TODO and Verification checkbox is checked.

If the plan is complete, `/start-plan` reports: `This plan has already been
implemented.` It then stops without implementation, delegation, validation, or
state mutation.

An explicit valid plan path replaces missing, invalid, or stale state. Without
an explicit path, unusable state requires the user to provide a plan path. The
latest valid explicit selection wins. This pointer is not an exclusivity or
concurrency mechanism; attempts to run multiple plans are not coordinated or
blocked.

Repositories may ignore `/.erb/plan-state.json` or a broader local plan
directory according to project policy. Missing ignore rules never block plan
creation or execution.

## Creation

Validate the request against repository evidence and the checklist-entry
contract, choose the smallest layout, write the plan with all boxes unchecked,
and re-read it. Then write the selected canonical path to
`.erb/plan-state.json` and re-read both files. Stop without implementation.

A current explicit split-or-replace request may create at least two successors
and retire one unambiguous source. Create and re-read every successor, re-read
the exact source, and only then delete the source with an exact-content edit
patch. If successor creation or verification fails, keep the source. No registry,
retained contract history, or additional deletion confirmation is required.

## Active Plan Updates

`/update-plan <exact-plan-path>` requires one explicit canonical plan path. It
never infers the target from `.erb/plan-state.json`, and it does not select the
updated plan. Accept only a plan with at least one unchecked TODO or Verification
checkbox. A completed plan remains immutable; additional work requires a new
human-authorized `/create-plan` request.

Re-read the exact plan and fresh repository evidence immediately before
mutation, and validate the existing canonical format. During `/update-plan`,
checklist-entry violations in the existing active plan are repair inputs, not
triggers for the execution-only `/start-plan` material-plan-change stop rule.
Derive and validate the complete candidate plan before mutation, including
checkbox reconciliation and any re-sequencing. If the candidate fails the
canonical format or checklist-entry contract, stop with the original plan
unchanged. Otherwise apply the smallest exact-content edit patch that satisfies
the human's instructions, keep the same path, then re-read and validate the
persisted result. If the patch no longer matches fresh content, stop instead of
overwriting unexpected changes.

Reconcile checklist evidence conservatively:

- New TODO and Verification entries are unchecked.
- An unchecked entry never becomes checked during an update.
- A checked entry stays checked only when its obligation and the surrounding
  acceptance contract remain materially unchanged and fresh evidence still
  supports it.
- A changed, invalidated, or insufficiently evidenced checked entry resets to
  unchecked.
- When ordering violates the checklist-entry contract, re-sequence the smallest
  affected set. Dependency correctness outranks preserving existing order. Keep
  all TODOs before dedicated Verification steps and keep entries sequentially
  numbered within each checklist.
- Reordering alone does not justify retaining checked state. Apply the same
  evidence rules after every move, and report the old-to-new ordering plus the
  reason for each move.

Do not write `.erb/plan-state.json`, delegate, implement, run implementation
validation, stage, commit, execute TODOs, or update native planned-work TODOs in
this route. Report the applied changes and every retained or reset checked item.
A later explicit `/start-plan <existing-plan-path>` request is required to
execute or resume the updated plan.

## Plan Artifact Commits

After the Plan Orchestrator creates and validates a plan, an explicit current
human commit request may authorize the selected Engineering Lead to stage and
commit only the canonical plan Markdown. This exception does not authorize the
Lead to create, edit, advance, or execute a plan. It excludes
`.erb/plan-state.json`.

The Lead re-reads the exact contained regular non-symlink plan, derives its
repository-relative path from fresh trusted worktree evidence, and stages one
literal path with `git add -- <path>`. Runtime approval is an additional human
check, not proof that a path is safe. Wildcards, question marks, bracket
expressions, braces, pathspec magic, `.` shorthand, traversal, substitution,
shell composition, and redirection remain forbidden.

## Execution And Resume

Validate the selected path, canonical plan format, and the whole checklist-entry
contract before mutation. Resume the first unchecked checkbox. Finish TODOs in
document order before Verification steps.

Check a TODO only after observed implementation or individual-validation
evidence. Check a Verification step only after its own observed evidence. A
blocked, failed, or uncertain step remains unchecked and is still current.
Re-read the plan and fresh worktree evidence before each mutable phase.

If fresh evidence shows that the plan contract needs a material update, leave
the current checkbox unchecked, stop execution, and report the exact mismatch
plus the smallest proposed amendment. The human may then choose
`/update-plan <exact-plan-path>`. Never update the plan during `/start-plan`;
resume only after a later explicit `/start-plan` request.

Every Worker assignment has exactly one mode: `implementation` or non-editing
`verification`, and only one Worker may be active at a time. In implementation
mode, the Plan Orchestrator delegates one bounded TODO slice, derives the current
obligation partition, preserves evidenced-complete work, and reconciles Worker
evidence before any checkbox change. Worker results close only their assigned
slice; no Worker result authorizes a checkbox change.

Each new implementation Task receives a self-contained packet. The Plan
Orchestrator derives the full canonical TODO obligation set and partitions it into
three disjoint and collectively exhaustive sets: active slice, evidenced complete,
and unresolved or deferred. It selects one bounded active slice; unresolved or
deferred work is context only, while satisfied dependencies are preserved and not
repeated. A Worker `COMPLETED` report closes only the active slice, and the
Orchestrator reconciles source, diff, and validation evidence before a TODO-level
integration decision.

Strict progress means fresh evidence moves at least one unresolved active-slice
criterion to evidenced complete. The Orchestrator preserves that evidence and
forms a strictly smaller residual active slice. With no criterion classification
change, it may resume the same implementation child for one complete,
delta-focused correction; a second consecutive unsupported no-progress return is
an execution-channel failure and leaves the checkbox unchecked. Permission-state
and replay-safety gates run before no-progress handling. While approval is
pending, retain one waiting child; approval alone does not prove execution; and
unknown or interrupted execution stops without replay. Before every continuation,
the Orchestrator stops rather than repeating an action whose prior result or
replay safety cannot be established from fresh evidence. If an interrupted runtime
cannot resume the prior Task child, it re-derives the obligation partition and
creates one fresh self-contained Task for only the unresolved slice without
inferring completion.

Verification is non-editing. Its packet may authorize repository-local bounded
setup needed for the objective, one diagnostic pass, waiting for a known live
lock or process to a finite deadline, exact owned disposable cleanup, and at most
three parent-authorized starts. It never becomes implementation or decides retry,
correction, effect, uncertain-result, or checkbox transitions. Plan and Task
scope never satisfy an `ask` permission.

This guide describes the protocol; the Plan Orchestrator prompt alone owns its
transition policy. That prompt classifies each operation as `repeatable_local`,
`consequential`, or `prohibited`, reconciles liveness and observed effects, and
selects the next transition. Known lock or process contention waits within the
packet deadline. A deterministic verification failure requires a fresh bounded
`implementation` assignment under the same obligation followed by fresh
verification. An uncertain repeatable-local execution first requires liveness and
effect reconciliation. Unknown consequential execution, denied or rejected
permission, unexpected effects, material scope change, prohibited operations, or
an exhausted budget stop with the checkbox unchecked.

The Worker reports status, mode, effect class, approval and execution state,
attempt budget, liveness and effect evidence, cleanup state, replay safety,
requirement mapping, validation, and residual risk. The Plan Orchestrator alone
reconciles this evidence and advances a checkbox. Worker results are evidence,
never checkbox authority. Documentation and `/start-plan` are descriptive
projections, not competing transition state machines.

## Security And Validation

Treat state paths and plan content as untrusted. Reject absolute paths, traversal,
symlinks, alternate repositories, non-regular files, invalid UTF-8, and content
larger than 1 MiB. Use edit tools instead of shell redirection for plan and state
writes.

In a human-owned repository, allowed checked-in Just recipes, package scripts,
build scripts, tests, hooks, and binaries execute as trusted arbitrary local code
with the host authority of the OpenCode process. Static permission rules classify
direct command forms; they do not sandbox transitive runner effects or provide
task-scoped filesystem or network containment. External-repository runners are
not trusted by this posture and remain separately gated. Genuinely untrusted
execution requires an outer container, VM, or OS control not added here.

Native checked-in agent and command definitions plus the Plan Orchestrator remain
authoritative. No plugin or secondary runtime may own, inject, or replace agents
or commands; mutate plans or state; classify permissions, effects, or retries; or
autonomously continue work. Reconsider only observational status or UX assistance
after full-restart measurements show residual friction; observation never grants
workflow authority.

Optional ERB review is independent read-only advice, not approval, readiness,
persistence, or execution authority. Report selected plan, current or completed
state, checkbox evidence, validation, skipped checks, unresolved decisions, and
residual risk.
