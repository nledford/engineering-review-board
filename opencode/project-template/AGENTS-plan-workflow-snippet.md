## Durable implementation-plan workflow

Use canonical plans at
`docs/implementation-plans/plans/<series>/<NN>-<slug>.md`. The series matches
`[a-z][a-z0-9-]{1,19}`; allocate the next zero-padded number as max+1 without
reusing gaps. The path supplies plan identity. New and updated plans use exactly
the closed lean shape in `docs/implementation-plans/TEMPLATE.md`: no frontmatter,
lifecycle fields, review records, history, or additional sections. Resolve a
central choice conversationally rather than adding an open-decision section.
Existing lifecycle-style plans are immutable legacy evidence; create a new
max-plus-one lean successor instead of modifying them.

The Engineering Lead owns classification, integration, validation, and handoffs.
It may complete narrow work directly or delegate bounded, non-overlapping
implementation units only to `implementation-worker`. The worker cannot edit
durable plans, delegate, commit, push, deploy, or broaden its assigned scope.

Route durable plan creation, updates, trusted state, planned execution, plan
checkboxes, and planned-work TODOs through top-level `/start-work`. Its Plan
Orchestrator is the only durable plan and trusted-state writer. The Engineering
Review Board is a separate, optional read-only primary agent, never a Task child;
invoke it directly for advisory review. Its critics and researchers do not
implement changes or control plan or state work.

Before first planned use, bootstrap must not overwrite the target repository's
`.gitignore`. After provisional state acquisition, add these missing exact lines
only when the existing policy is safe and non-conflicting:

```text
/.start-work/resume.json
/.start-work/lock/
```

Stop on broad, duplicate, ambiguous, or conflicting `.start-work` rules. Do not
copy the trusted helper into the target repository; it runs only from the linked
OpenCode checkout. The Plan Orchestrator acquires trusted provisional ownership
before mutating plan or state, validates the contained non-symlinked plan path,
and records only observed plan and state evidence. While retaining that lock, it
may construct a commit only for an explicit current human request or bounded plan
TODO: derive exact repository-relative paths from fresh trusted worktree evidence,
use `git add --`, recheck the staged diff and resulting worktree, and retain lock
and staged state on failure or uncertainty. A validated active canonical plan may
be staged, but Bash remains forbidden from mutating or redirecting plan bytes.
Approval is an additional human check, not proof a path is safe: separately
enumerate each dirty repository-relative path, quote it as one literal shell
word, and stop on `*`, `?`, bracket expressions, braces, pathspec magic, `.`,
traversal, substitution, or any other expansion syntax that cannot be represented
literally under the command policy.
The worker cannot stage or commit; amend, hook/signing bypass, implicit staging,
fetch, push, and branch/ref/history/worktree/remote mutation remain forbidden.
Load `git-commit`, plus `security-review` and `security-review-evidence` when
Git trust boundaries apply. Keep live OpenCode configuration machine-local; quit
and fully restart OpenCode before definition changes grant authority, because the
running session remains unchanged.
