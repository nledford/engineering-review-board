---
name: suggest-lucide-icons
description: Pick real Lucide icons for a concept, UI placement, button, section header, or note frontmatter. Use when the user asks what Lucide icon to use, requests icon candidates, or needs an icon name verified.
---

# Suggest Lucide Icons

Use this skill to choose existing Lucide icon names, not to invent symbolic
artwork. Optimize for recognizable meaning in the user's context.

## Workflow

1. When the project uses Lucide, inspect its manifest and installed package version
   first. Verify candidates against that exact version; `@latest` is not proof of
   project compatibility.
2. Identify the concept, action, object, state, and UI placement.
3. Generate 4-6 plausible Lucide icon names in kebab-case.
4. Verify candidates against the installed package or versioned package assets. If
   no project version constrains compatibility, use `https://lucide.dev/icons/<icon-name>`
   or the current upstream package instead.
5. Discard names that cannot be verified.
6. Present up to 3 confirmed candidates and recommend one, stating the verification
   source and version.

If verification is blocked by network or tooling, say that candidates are
unverified and do not present them as confirmed.

## Naming Rules

- Use kebab-case: `arrow-up`, not `Arrow Up`.
- Use Lucide's American English names: `color`, not `colour`.
- For grouped variants, use the icon family first: `badge-plus`.
- For multiple elements, lead with the larger or containing element:
  `circle-user`, `square-arrow-out-up-right`.
- For modifiers, put the base object first: `circle-dashed`, not
  `dashed-circle`.

## Selection Rules

- Prefer icons whose visual metaphor works without explanation.
- Match the placement: toolbar actions need simpler shapes than navigation or
  section icons.
- Prefer action icons for commands (`save`, `download`, `trash-2`) and object or
  state icons for labels (`database`, `shield-check`, `file-warning`).
- Avoid novelty when a conventional icon exists.
- For multiple requested icons, choose a visually coherent set with similar
  density and stroke complexity.

## Output

```text
Candidates
- icon-name: why it fits
- icon-name: why it fits
- icon-name: why it fits

Recommendation: icon-name
Reason: ...
Verification: ...
```
