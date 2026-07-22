## Durable Plan Workflow

Project-local plans use the canonical contract in
[`docs/implementation-plans/README.md`](docs/implementation-plans/README.md).
Prefer direct implementation when scope, safety, and validation are adequate;
complexity may justify a recommendation, never automatic plan creation.

The Lead or ERB may recommend top-level `/consult-plan` for bounded read-only
Plan Orchestrator advice, stating the reason, trade-off, and proposed scope. The
human controls the route. Only an explicit human `/create-plan` request creates
and persists a plan, and it is plan-only. Use `.erb/plans/<slug>.md` for one plan
and `.erb/plans/<subject>/<NN>-<slug>.md` only for separately managed series.

An explicit `/update-plan <exact-plan-path>` request may update one active plan
in place and is plan-only. It requires one canonical path, never infers its
target from `.erb/plan-state.json`, does not change state, and does not execute
TODOs. Completed plans remain immutable. New checklist entries remain unchecked,
and checked entries reset to unchecked when changed, invalidated, or no longer
supported by fresh evidence.

Every TODO and Verification entry has one finite atomic purpose and focused
evidence, follows all prerequisites in document order, discloses known ask-gated
or destructive operations and their contained targets, and has no self- or
future-step dependency, cycle, mutually waiting step, or unbounded progress
loop. Planning-time permission disclosure is not approval; execution reclassifies
the operation against current runtime policy. `/update-plan` may re-sequence the
smallest affected set when dependency correctness requires it.

Execution-only `/start-plan` accepts an existing valid canonical plan path or,
without a path, the selection in `.erb/plan-state.json`. The state file stores
only the repository-relative plan path. Derive active status and current work
from the plan: a plan remains active while a TODO or Verification checkbox is
unchecked, and the first unchecked checkbox is current. A fully checked plan
reports that it has already been implemented and stops.

An explicit valid plan path repairs missing, invalid, or stale state. The latest
explicit selection wins. The pointer is not concurrency control and does not
prevent the user from starting another plan.

Active plan bodies are immutable by default and during execution except for
evidenced checkbox advancement. Only a current explicit `/update-plan` request
authorizes an in-place prose or structure update. Separately, a current explicit
split-or-replace request may create at least two successors and retire one
unambiguous source after the source and all successors are re-read. No registry
or retained contract history is required.

The Plan Orchestrator is the exclusive durable-plan and state writer. The
Engineering Review Board remains separate, optional, and read-only advisory. The
Worker cannot edit plans or `.erb/plan-state.json`, stage, or commit. Every Worker
assignment fixes one mode: `implementation` or non-editing `verification`.
Implementation receives a self-contained bounded slice with numbered criteria;
the Orchestrator derives the TODO obligation partition, preserves completed
evidence, and reconciles Worker results before any checkbox change. Verification
may use packet-authorized repository-local setup, one diagnostic pass, finite
known lock or process waiting, exact owned disposable cleanup, and no more than
three parent-authorized starts. It never changes itself into implementation or
decides retries.

In implementation mode, each new Worker Task receives a self-contained packet
with one bounded active slice at a time. Strict criterion-level progress creates
a smaller residual slice; a second unsupported no-progress return is an
execution-channel failure. The Orchestrator stops when prior result or replay
safety is uncertain. Plan and Task scope never satisfy an `ask` permission.
A pending approval retains one waiting child.

The Plan Orchestrator prompt alone classifies planned effects and owns retry,
correction, uncertain-result, and checkbox transitions. Its descriptive
projection here is not a second state machine: deterministic verification failure
returns `NEEDS_CORRECTION` for a fresh bounded implementation unit followed by
fresh verification. Unknown consequential execution, denied or rejected
permission, unexpected effects, material scope change, prohibited operations, or
an exhausted budget stop with the checkbox unchecked. Worker results are evidence,
not checkbox authority.

In a human-owned repository, allowed checked-in project runners execute as
trusted arbitrary local code with the host authority of the OpenCode process.
Static permissions classify direct forms and do not sandbox transitive runner
effects or task-scoped filesystem or network access. Unknown direct command forms
and consequential directly invoked operations remain ask/deny-gated.
External-repository runners remain untrusted and require separate gating; use an
outer container, VM, or OS control for genuinely untrusted execution. Native
checked-in definitions and the
Plan Orchestrator remain authoritative: no plugin or secondary runtime may own or
replace agents or commands, mutate plans or state, classify permissions, effects,
or retries, or autonomously continue work. Reconsider only observational status
or UX assistance after full-restart measurements show residual friction; it never
grants workflow authority.

After the required full restart, the Lead and Worker trusted-local profiles allow
routine scoped in-repository edits and their canonical local quality, build, and
test command families without runtime approval. Plan and state paths retain their
existing boundaries.

After the Plan Orchestrator creates and validates a plan, an explicit current
human commit request may authorize the Engineering Lead to stage and commit only
the canonical plan Markdown. This exception grants no plan edit, state, or
execution authority and excludes `.erb/plan-state.json`. Use one freshly derived
literal canonical path per approval-gated `git add --` command; never use
expansion syntax, shell composition, or redirection.

OpenCode agent-definition changes take effect only after a full restart.
