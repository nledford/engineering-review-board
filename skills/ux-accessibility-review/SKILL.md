---
name: ux-accessibility-review
description: Review UI and UX quality, visual polish, responsive behavior, interaction states, and WCAG accessibility. Use for focused interface audits of existing products or changes; do not use as the primary styling, frontend implementation, or browser-test workflow.
---

# UX Accessibility Review Skill

Use this skill as a focused review lens for user interfaces and end-to-end
workflows. Always load
[`review-verification-protocol`](../review-verification-protocol/SKILL.md)
before reporting findings. For repository change reviews, also load
[`code-review`](../code-review/SKILL.md).

Use [`css-scss-styling`](../css-scss-styling/SKILL.md) for stylesheet
implementation and [`playwright-e2e`](../playwright-e2e/SKILL.md) for durable
browser-test changes. Do not infer product quality from source code alone when a
runnable interface is available.

## Workflow

1. Identify target users, critical tasks, supported devices, design-system
   conventions, and required accessibility level.
2. Exercise key workflows and states across relevant viewports, including
   loading, empty, error, success, hover, focus, active, and disabled behavior.
3. Review visual hierarchy, spacing, typography, density, alignment,
   responsiveness, cognitive load, and task completion.
4. Check WCAG 2.2 AA concerns including semantics, labels, keyboard navigation,
   focus order and visibility, contrast, ARIA use, reduced motion, zoom/reflow,
   screen-reader output, and touch targets.
5. Verify findings with the rendered interface, DOM/accessibility tree,
   computed styles, keyboard use, or automated checks. Record untested devices,
   assistive technologies, skipped checks, and residual risk.

## Output

Return prioritized findings with user impact, reproducible evidence, concrete
fixes, positive patterns worth preserving, skipped validation, and residual
risk.
