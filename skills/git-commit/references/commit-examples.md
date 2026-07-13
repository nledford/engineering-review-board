# Commit Examples

Load this reference when the core workflow in
[`../SKILL.md`](../SKILL.md) needs detailed message or grouping examples. Follow
the repository's established convention when it conflicts with these examples.

## Conventional Commit Types

- `feat`: add user-facing or externally visible functionality.
- `fix`: correct broken behavior.
- `docs`: documentation-only changes.
- `test`: add or update tests without production behavior changes.
- `refactor`: restructure code without changing behavior.
- `chore`: routine maintenance that does not fit a more specific type.
- `build`: build system, dependency, or packaging changes.
- `ci`: continuous integration configuration or scripts.
- `style`: formatting or style-only changes with no behavior change.
- `perf`: improve performance.

## Subject Comparisons

| Poor | Better |
| --- | --- |
| `updates` | `Update image cache expiration rules` |
| `fix stuff` | `Fix retry loop for transient upload errors` |
| `misc changes` | Split into focused commits with specific subjects |
| `WIP` | `Add draft import queue behind feature flag` if WIP commits are allowed |
| `changed auth` | `Fix session renewal after password reset` |

## Message Shapes

Subject only:

```text
docs: fix typo in installation guide
```

Subject and body:

```text
fix(cache): prevent stale entries after rename

Renaming an item updated the primary record but left the old cache key in
place. Invalidate both the old and new keys so subsequent reads cannot return
stale metadata.
```

Subject, body, and footer:

```text
refactor(import): stream large CSV files

The previous importer loaded entire files into memory before validation.
Streaming keeps memory usage bounded and lets validation report the first
failing row earlier.

Refs: DATA-214
```

Breaking change:

```text
feat(api)!: require explicit pagination limits

BREAKING CHANGE: list endpoints now reject requests without a `limit`
parameter. Set `limit` explicitly to preserve previous behavior.
```

Non-Conventional style can be equally valid when local history uses it:

```text
Stream large CSV imports

Keep memory usage bounded by validating records as they are read instead of
loading the full file before processing.
```

## Mixed Working Tree

Suppose a working tree contains:

```text
src/importer.rs              # new streaming behavior plus whitespace cleanup
tests/importer_large.rs      # coverage for large files
README.md                    # documents importer limits
Cargo.toml                   # parser dependency update
Cargo.lock                   # dependency resolution
```

Potential commit groups:

1. `style(import): normalize importer formatting`
2. `build(parser): update CSV parser dependency`
3. `feat(import): stream large CSV files`
4. `docs(import): document CSV size limits`

Keep implementation and tests together when they explain one behavior change.
Separate tests when they document an independent regression or review unit.
Never use destructive worktree commands merely to manufacture these groups;
stage intended hunks and preserve unrelated changes.
