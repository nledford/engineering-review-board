---
name: serena
description: Semantic code navigation and refactoring with the Serena MCP toolkit. Use when exploring code structure, finding symbols, declarations, references, implementations, call relationships, diagnostics, or making symbol-level edits and renames in supported languages. Do not use for non-code text search, docs/config/logs/assets, tiny single-file text edits, or as a replacement for repository instructions, direct reads, and validation commands.
---

# Serena

Use Serena when an agent needs IDE-like understanding of a codebase instead of
plain text matching. Serena is an MCP-based coding toolkit that exposes semantic
code retrieval, editing, refactoring, and diagnostics through language-server and
IDE-style capabilities.

## What Serena Solves

- Reduces context waste from broad file reads in large or unfamiliar codebases.
- Finds code by symbols, declarations, references, implementations, and call
  relationships instead of only by matching text.
- Supports safer cross-file refactors and renames when language tooling can prove
  where a symbol is used.
- Surfaces diagnostics and symbol structure that plain `grep` output cannot.
- Helps agents move from "where is this?" to "what owns this behavior and who
  calls it?" before editing.

## When to Use Serena

Use Serena for code-centric tasks such as:

- exploring unfamiliar modules, packages, crates, or service boundaries;
- finding a symbol, declaration, implementation, method, class, trait, function,
  or interface;
- checking references or callers before changing an API, type, function, method,
  field, or module boundary;
- understanding inheritance, implementation, or adapter relationships;
- reading a symbol body after a semantic search has narrowed the target;
- renaming or moving code where symbol-aware refactoring is available;
- checking file diagnostics before or after changes;
- reviewing or debugging behavior when call paths matter more than exact text.

Serena is most valuable when the repository is large, the relevant files are not
obvious, or symbol relationships matter to correctness.

## Workflow Fit

1. Read local task instructions, repository docs, and AGENTS-style guidance first;
   Serena does not override project rules.
2. If not already read this session, call `serena_initial_instructions` before
   using Serena's other tools.
3. Use ordinary `glob`, direct reads, and exact-text search to locate files,
   docs, configs, generated assets, and literal strings.
4. Switch to Serena when the question becomes semantic: "which symbol is this?",
   "who references it?", "what implements it?", or "can this be renamed safely?"
5. Start with overviews or symbol searches. Retrieve only the symbol bodies needed
   for the decision instead of reading whole files by default.
6. Before changing a public or shared symbol, inspect references, implementations,
   callers, and diagnostics that could be affected.
7. Use symbol-level edits or semantic rename only when they match the intended
   change; otherwise use precise file edits.
8. Verify with the repository's tests, formatters, linters, type checks, builds,
   or focused manual checks. Serena is navigation and editing assistance, not
   validation evidence by itself.

## Why Prefer Serena Over Plain Search Sometimes

Plain search is ideal for exact strings, comments, docs, configuration, fixtures,
and unknown textual clues. Prefer Serena when names, imports, overloads,
implementations, or cross-file references can make text search noisy or
incomplete. Semantic tools usually produce less context, preserve intent better,
and reduce missed call sites during refactors.

## Use Serena Effectively

- Narrow first: search for symbols or get a file overview before requesting full
  bodies.
- Follow relationships: declaration -> references -> implementations/callers ->
  diagnostics.
- Keep edits small and behavior-focused. Use semantic rename for real symbol
  renames; avoid it for unrelated text or comments unless the tool explicitly
  handles them correctly.
- Cross-check surprising results with a direct file read or exact search.
- Treat diagnostics as evidence to investigate, not proof that all behavior is
  correct.
- If indexes appear stale, language support is missing, or generated/macro-heavy
  code hides relationships, fall back to direct reads, search, build output, and
  tests.

## When Not to Use Serena

Prefer direct file tools or shell commands for:

- Markdown, README files, comments-only searches, docs, changelogs, and prose;
- config files, manifests, lockfiles, logs, fixtures, snapshots, templates, and
  non-code assets;
- exact string search, counting matches, or verifying literal text;
- generated, vendored, minified, or unsupported-language code where semantic
  indexes may be incomplete;
- tiny single-file edits where a direct read and patch is clearer;
- external library/API documentation lookup;
- running tests, builds, formatters, linters, package managers, or git commands.

## Anti-Patterns

- Reading every file or every symbol through Serena when a targeted query would
  answer the question.
- Trusting semantic results without checking stale indexes, unsupported languages,
  conditional compilation, macros, metaprogramming, generated code, or vendored
  dependencies.
- Using broad textual search results as proof of references when a symbol-aware
  reference query is available.
- Using symbol-level replacement for small textual edits that do not align with a
  whole symbol.
- Renaming public or shared symbols without inspecting references and running the
  relevant validation commands.
- Letting Serena output replace requirements analysis, repository docs, local
  instructions, direct reads of decisive files, or tests.

## Complements, Not Replacements

Serena complements direct file reads, search tools, local documentation, and test
commands. Use it to focus code exploration and make semantic edits; use direct
reads for exact content and non-code context; use repository docs and AGENTS-style
files for rules; use tests, type checks, lint, format, build, and diagnostics to
verify the final state.
