# Asyncio Concurrency Reference

Load this reference only when concurrency behavior is a primary source of risk.
Sequential async I/O and routine `await` usage belong in the core
[`python-engineering`](../SKILL.md) workflow. Inspect the project's supported
Python version, runtime conventions, and test support before choosing APIs.

## Define The Contract First

Before implementation, state:

- which scope owns each task, queue, and resource;
- the maximum in-flight work and queued work;
- what producers do at capacity: wait, reject, drop, coalesce, or persist;
- whether one failure cancels siblings or produces a partial result;
- how cancellation, deadlines, retries, and shutdown affect an accepted item;
- whether pending work must survive process termination.

If these decisions are implicit, scheduling determines behavior by accident.

## Structured Ownership

- Give every task a parent that awaits it and observes its failure. Prefer
  `asyncio.TaskGroup` when the supported Python version provides it and sibling
  tasks share a lifetime. A non-cancellation failure cancels the remaining
  siblings and the group waits for them before raising grouped failures, except
  that `KeyboardInterrupt` and `SystemExit` are re-raised directly.
- Use fail-fast task-group behavior for coupled work. For independent items,
  catch expected item failures inside the worker and record an explicit outcome
  so one item does not unintentionally cancel unrelated work.
- Keep strong references to tasks created with `asyncio.create_task`. If work
  must outlive the creating call, place it in a longer-lived supervisor that
  tracks, reports, cancels, and awaits every task during shutdown.
- Ensure each resource's owning scope outlives every task that uses it. Create
  concurrency-safe shared resources in the parent scope, but let tasks acquire
  and clean up task-local connections, transactions, sessions, locks, or other
  resources that must not be shared. Await tasks before closing shared resources,
  and release task-local resources in `finally` blocks or async context managers.

## Bounded Concurrency And Backpressure

- Prefer a fixed worker set consuming `asyncio.Queue(maxsize=N)` when work
  naturally queues. Use a semaphore when calls arrive directly and only the
  in-flight operation needs a cap. A queue with `maxsize=0` is unbounded.
- Choose worker and queue limits from downstream capacity, memory cost, and the
  latency budget. Queue capacity controls burst absorption; worker count
  controls active pressure. They are separate limits.
- Do not create an unbounded task per item and rely on a semaphore only after
  task creation. This bounds execution but not task allocation or retained
  inputs.
- Make overload behavior observable and part of the caller contract. Never
  silently turn a full queue into data loss or unlimited waiting.
- Pair each accepted `queue.get()` with a completion decision. Call
  `task_done()` only after success or after failure/requeue state is recorded,
  so `queue.join()` neither hangs nor implies work was safely completed.

## Cancellation And Shutdown

- Treat `asyncio.CancelledError` as control flow. Put cleanup in `finally`; if
  cancellation is caught for cleanup, re-raise it after cleanup. Broad handlers
  must not convert cancellation into an ordinary item failure.
- Define shutdown order explicitly: stop intake, unblock or notify producers,
  drain accepted work or mark it abandoned according to policy, stop workers,
  await their termination, then close shared resources.
- Decide the cancellation-safe boundary for each item. If cancellation can land
  after an external side effect, use an idempotency key, durable status, or
  reconciliation rather than assuming the operation did not happen.
- Keep cleanup bounded. Shield only a narrowly identified cleanup action that
  must finish independently, and still await and time-bound it.

## Timeouts, Retries, Rate Limits, And Partial Success

- Prefer an end-to-end deadline over unrelated per-call timeouts. Decide whether
  queue wait counts against it, pass the remaining budget inward, and ensure
  retries cannot exceed the caller's total budget.
- Retry only classified transient failures. Bound attempts and elapsed time,
  use backoff with jitter, keep sleeps cancellable, and honor server-directed
  delay when the protocol provides one. Do not retry cancellation or permanent
  validation, authorization, or contract errors.
- Treat concurrency limits and rate limits as different controls. Enforce rate
  policy at the outbound boundary that consumes the quota; a semaphore alone
  does not limit requests per time interval.
- Retry side effects only when they are idempotent or protected by a stable
  idempotency/deduplication key.
- Choose fail-fast or best-effort behavior deliberately. For partial success,
  return or persist a terminal outcome for every accepted item, keyed by a
  stable input identifier, rather than exposing completion order as identity.

## Ordering And Shared State

- Assume concurrent completion is out of order. Preserve global order with one
  worker, per-key order with stable partitioning, or output order with sequence
  numbers and a bounded reorder buffer. State which order, if any, callers can
  rely on.
- Prefer single-owner state and message passing. When shared mutation is
  necessary, protect the smallest invariant with an asyncio synchronization
  primitive and avoid slow or external I/O while holding a lock.
- Asyncio synchronization primitives coordinate event-loop tasks; they are not
  thread-safe. Use a thread- or process-safe boundary when work crosses runtimes.
- Re-check predicates after waking from a condition. Scheduling and spurious
  wakeups make a notification alone insufficient proof that state is ready.

## Durable Intent And Restart Recovery

Add durability only when accepted work must survive the process that owns the
event loop. In-memory tasks, queues, and locks do not provide restart recovery.

- Persist intent before acknowledging acceptance. Store a stable work ID,
  payload or reference, state, attempt count, and next eligible time.
- Claim work with an atomic transition or expiring lease. On restart, recover
  pending work and safely reclaim expired attempts.
- Assume at-least-once execution unless the actual storage and side-effect
  protocol proves stronger semantics. Make handlers idempotent and record
  completion or deduplication state durably.
- Keep process-scoped work in memory when losing it at process exit is an
  explicit and acceptable contract; do not add durable infrastructure by
  default.

## Deterministic Async Tests

- Inject the application clock and async sleeper for deadline, backoff, and
  rate-limit tests. Advance a fake clock instead of waiting in real time.
- Coordinate exact states with `asyncio.Event`, queues, or a barrier supported
  by the project's Python version. Do not use short sleeps to guess when a task
  reached a scheduling point.
- Use scripted fakes to produce success, transient failure, permanent failure,
  timeout, and cancellation in a known order.
- Assert the concurrency maximum, capacity behavior, retry/deadline budget,
  ordering guarantee, partial outcomes, and shutdown cleanup. Use a test timeout
  only as a deadlock guard, not as the synchronization mechanism.
- At test teardown, assert that supervised tasks finished or were awaited and
  that queues, locks, and resources are left in the documented state.

Primary standard-library references: [tasks and task groups], [queues], and
[synchronization primitives].

[tasks and task groups]: https://docs.python.org/3/library/asyncio-task.html
[queues]: https://docs.python.org/3/library/asyncio-queue.html
[synchronization primitives]: https://docs.python.org/3/library/asyncio-sync.html
