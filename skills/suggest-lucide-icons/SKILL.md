---
name: suggest-lucide-icons
description: Pick real Lucide icons for a concept, UI placement, button, section header, or note frontmatter. Use when the user asks what Lucide icon to use, requests icon candidates, or needs an icon name verified.
---

# Suggest Lucide Icons

Use this skill to choose existing Lucide icon names, not to invent symbolic
artwork. Optimize for recognizable meaning in the user's context.

## Workflow

1. Identify the concept, action, object, state, and UI placement.
2. Generate 4-6 plausible Lucide icon names in kebab-case.
3. Verify candidates against an authoritative source:
   - `https://lucide.dev/icons/<icon-name>` when browsing is available;
   - `https://unpkg.com/lucide-static@latest/icons/<icon-name>.svg` when direct
     asset checks are easier;
   - an installed `lucide-static` or `lucide-react` package when the repo already
     vendors Lucide.
4. Discard names that cannot be verified.
5. Present up to 3 confirmed candidates and recommend one.

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
