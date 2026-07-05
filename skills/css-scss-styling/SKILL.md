---
name: css-scss-styling
description: CSS and SCSS/Sass styling guidance. Use when adding, changing, reviewing, refactoring, or migrating .css, .scss, .sass, CSS modules, design tokens, cascade layers, container/media queries, responsive layout, stylesheet build pipelines, CSS-in-JS, utility-class conventions, or styling integration in HTML, JavaScript/TypeScript, Python templates, or Rust Leptos/Axum apps. Use language/framework skills for non-styling implementation mechanics and do not use for behavior changes with no styling surface.
---

# CSS And SCSS Styling

Use this skill for project-neutral stylesheet work. Inspect the repository before
assuming plain CSS, SCSS/Sass, CSS modules, CSS-in-JS, utility CSS, or a
framework convention. Keep the guidance operational: preserve local conventions,
choose the simplest styling system that satisfies the requirement, and verify the
compiled/browser-visible result.

## Use When

- Editing `.css`, `.scss`, `.sass`, `*.module.css`, `*.module.scss`, design-token
  files, global stylesheets, component styles, theme files, or stylesheet build
  config.
- Changing cascade behavior, layout, responsive behavior, accessibility-related
  visual states, browser compatibility, or style performance.
- Deciding whether to use plain CSS or SCSS, converting CSS to SCSS, or avoiding
  an unnecessary conversion.
- Integrating styles with static HTML, JS/TS apps, Python web templates, Rust
  Leptos/Axum apps, CSS-in-JS, CSS modules, utility CSS, or framework-specific
  styling conventions.

Do not use this skill for UI behavior with no stylesheet or browser-visible
styling change. Use [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md),
[`python-engineering`](../python-engineering/SKILL.md), or
[`rust-async-web`](../rust-async-web/SKILL.md) for language/framework mechanics;
add this skill only when styling choices or style build behavior matter.

## Workflow

1. Detect the existing styling system before editing. Look at file patterns,
   imports, build scripts, framework config, README, design docs, Storybook or
   component examples, screenshots, and browser/E2E tests.
2. Identify the ownership boundary: global reset/theme, design tokens, component
   module, utility classes, template-level styles, generated CSS, or framework
   asset pipeline.
3. Choose plain CSS unless SCSS provides clear value in this repository. Do not
   introduce a preprocessor for one nested rule, one variable, or habit.
4. Make the smallest style change that preserves existing naming, cascade,
   token, breakpoint, and build conventions.
5. Verify both the source and output: formatter/linter, SCSS compilation when
   applicable, app build, targeted UI/browser tests, and a manual or screenshot
   check when layout/visual behavior is the product.

## Detect The Styling System

Use multiple clues; one dependency or file name is not enough.

| Surface | Clues |
| --- | --- |
| Plain CSS | `.css`, `styles.css`, `app.css`, `globals.css`, `assets/css/`, `<link rel="stylesheet">`, JS/TS imports of `.css`, no Sass dependency or loader. |
| SCSS/Sass | `.scss`, `.sass`, `_partial.scss`, `@use`, `@forward`, `$variables`, `@mixin`, `@include`, `sass` or `sass-embedded` dependencies, `sass-loader`, `vite`/`webpack`/`esbuild` Sass config, `sass` CLI scripts. |
| CSS modules | `*.module.css`, `*.module.scss`, imports such as `import styles from "./Button.module.css"`, generated scoped class names. |
| CSS-in-JS | `styled-components`, `@emotion/*`, `vanilla-extract`, `stitches`, `linaria`, `stylex`, `css\`...\``, `styled.div`, extracted CSS build plugins. |
| Utility CSS | `tailwind.config.*`, `@tailwind`, `@theme`, `postcss.config.*`, UnoCSS/Windi config, dense utility class strings in templates/components. |
| Framework conventions | Next/Vite/Astro/Svelte/Vue/Angular style entrypoints, Django/Flask static folders and templates, Rails-style asset folders, Leptos/Trunk/cargo-leptos static assets, Axum static-file routes. |

When conventions conflict, follow the closest local owner. For example, a React
app may use global CSS for tokens, CSS modules for components, and utility
classes for layout; do not collapse those into one system unless the task is an
explicit migration.

## CSS Versus SCSS Decision Rules

CSS is the browser's stylesheet language. Use it directly when the project can
express the style with the platform: custom properties, cascade layers, media
queries, container queries, logical properties, Grid/Flexbox, modern selectors,
and native nesting where the target browsers or build pipeline support it.

SCSS is the CSS-like syntax for Sass, a preprocessor that compiles to CSS. Sass
also has the indented `.sass` syntax; do not introduce `.sass` unless the
repository already uses it. Prefer `.scss` for new Sass work because it is close
to CSS and easier to migrate incrementally.

Prefer **plain CSS** when:

- The project already uses CSS and modern CSS features solve the problem.
- The only desired SCSS feature is shallow nesting, variables, or simple file
  organization that CSS custom properties, native nesting, `@layer`, and imports
  or bundler entrypoints already cover.
- Runtime theming, user preferences, dark mode, container-size changes, or
  JavaScript-adjusted tokens need CSS custom properties in the browser.
- The project has no Sass build path and adding one would expand dependencies,
  CI time, editor setup, or deployment risk.

Prefer **SCSS** when:

- The repository already uses Sass and the change fits its module/token/mixin
  structure.
- Compile-time composition materially reduces duplication: shared maps, generated
  variants, math, functions, mixins, partials, or a package-style stylesheet API.
- A design system has many related tokens that need compile-time validation or
  exports through `@use`/`@forward`.
- A legacy SCSS codebase needs cleanup, migration from `@import`, or safer
  modularization without changing the browser-facing CSS contract.

If the decision is not obvious, state the tradeoff and choose the option that
adds less toolchain and migration burden.

## Modern CSS Guidance

- Use custom properties (`--token`) for runtime theme values, component-local
  tokens, dark/light modes, user preferences, and values JavaScript or media
  queries may change. Keep fallback values deliberate.
- Use cascade layers (`@layer reset, base, components, utilities;`) to make
  precedence explicit for resets, tokens, components, and overrides. Do not use
  specificity wars as a layer substitute.
- Use container queries for components that respond to their container, not the
  viewport. Keep media queries for viewport, device, and user-preference concerns
  such as `prefers-reduced-motion`, `prefers-color-scheme`, or coarse pointers.
- Use logical properties (`margin-inline`, `padding-block`, `inset-inline`,
  `border-start-start-radius`) when layout should survive writing-mode or
  direction changes.
- Use Flexbox for one-dimensional alignment and Grid for two-dimensional layout.
  Avoid float/table layout except for true legacy constraints.
- Use native CSS nesting only when local browser support or the build pipeline
  supports it; keep nesting shallow and avoid hiding selector specificity.
- Represent design tokens close to their consumption: global primitives on
  `:root`, semantic tokens in theme scopes, and component tokens on component
  roots. Avoid magic numbers unless the value is truly one-off.
- Prefer semantic class names and component boundaries over selectors coupled to
  deep DOM structure.

## Modern SCSS Guidance

- Use the Sass module system. Prefer `@use` for consuming variables, mixins, and
  functions, and `@forward` for exposing a curated module API. Avoid adding new
  `@import`; current Sass treats it as deprecated and it will be removed in a
  future major Dart Sass release.
- Keep module members namespaced (`theme.$space-2`, `@include buttons.reset`) so
  origins stay clear. Use `as *` only for a small, intentional compatibility
  layer.
- Use `$variables` for compile-time constants and CSS custom properties for
  runtime theming. Do not replace runtime `var(--token)` values with Sass
  variables unless the value never changes in the browser.
- Use mixins for repeated declaration groups that need parameters or feature
  gates. Avoid mixins that hide large, unrelated blocks of CSS.
- Use functions for pure value calculations. Keep side effects and emitted CSS in
  mixins, not functions.
- Use maps for related token sets and generated variants; validate expected keys
  where the project has patterns for doing so.
- Use partials (`_tokens.scss`) for files loaded by modules. Keep entrypoints
  explicit (`app.scss`, `index.scss`) and avoid accidental emitted CSS from helper
  files unless the module is meant to emit it.
- Use interpolation (`#{$name}`) sparingly for generated selectors, custom
  property names, or asset paths. Avoid interpolation that makes selector search
  and refactoring unreliable.
- Treat Sass as a build dependency. Update scripts, bundler config, Docker/CI, and
  generated output policy when introducing it.

## Integration Patterns

- **HTML pages:** link compiled CSS through `<link rel="stylesheet">` in the
  intended order. Keep critical inline styles minimal and avoid duplicating large
  rules across pages.
- **JavaScript/TypeScript apps:** use existing bundler conventions for CSS
  imports, CSS modules, extracted CSS, PostCSS, or CSS-in-JS. Load
  [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md)
  when package scripts, lockfiles, Vite/Webpack/Next/etc. config, or TypeScript
  component code changes.
- **Python web apps:** keep templates responsible for markup and class hooks;
  serve styles through the framework's static asset path such as Django static
  files or Flask `url_for("static", ...)`. Load
  [`python-engineering`](../python-engineering/SKILL.md) when routes, templates,
  packaging, or framework config changes.
- **Rust Leptos/Axum apps:** keep Leptos components deterministic for SSR and
  hydration, use class/style bindings only where they produce stable markup, and
  serve compiled assets through the app's Trunk/cargo-leptos/Axum static route.
  Load [`rust-async-web`](../rust-async-web/SKILL.md) when server functions,
  hydration, routing, WASM targets, or Axum static-file behavior changes.
- **Utility CSS:** follow the local utility framework and token config. Do not
  replace established utility conventions with handcrafted CSS, or vice versa,
  without an explicit migration goal.
- **CSS-in-JS:** follow the existing extraction/runtime model. Keep dynamic values
  bounded, avoid per-render stylesheet churn, and verify SSR/hydration behavior
  when styles are generated server-side.

## Accessibility, Responsive Design, And Performance

- Preserve visible focus states, hover/focus/active/disabled distinctions,
  contrast, text resizing, zoom, reduced-motion preferences, and hit-target sizes.
- Responsive behavior should come from fluid layout, intrinsic sizing, container
  queries, and minimal breakpoints before adding many viewport-specific overrides.
- Use `rem`, `em`, percentages, viewport/container units, and logical properties
  where they preserve user settings and layout direction.
- Keep animations cheap and optional: prefer transform/opacity, avoid layout
  thrash, and respect `prefers-reduced-motion`.
- Avoid loading unused CSS. Check code splitting, extraction, purging/content
  scanning, and critical CSS only within the project's existing build model.
- Check browser compatibility against the project's stated support matrix,
  Browserslist, framework baseline, or test browsers. Load
  [`context7-docs`](../context7-docs/SKILL.md) for version-sensitive framework,
  Sass, or build-tool behavior.

## Safe CSS-To-SCSS Migration

1. Confirm a migration is justified. If modern CSS solves the need, keep CSS and
   document why no preprocessor was added.
2. Inventory entrypoints, imports, static references, test snapshots, generated
   assets, cache keys, and deployment paths.
3. Add Sass through the repository's package/build workflow; do not hand-edit
   lockfiles or generated bundles.
4. Rename incrementally (`.css` to `.scss`) and keep CSS-compatible syntax first.
   Update imports, HTML links, template references, and build scripts together.
5. Introduce SCSS features only after compilation matches the old output closely
   enough to review. Prefer `@use`/`@forward` modules over `@import`.
6. Validate compiled CSS, app build, visual or browser tests, accessibility states,
   and cache/deploy behavior. Compare output size and selector changes when risk
   is high.

Migration risks include broken asset URLs, changed cascade order, duplicated or
missing emitted CSS, CSS module class-name changes, source-map drift, framework
watcher failures, CI image missing Sass, and visual regressions hidden by broad
snapshots.

## Anti-Patterns

- Converting to SCSS by default when CSS custom properties, `@layer`, native
  nesting, or container queries are enough.
- Adding `@import` to new Sass code instead of `@use`/`@forward`.
- Using Sass variables for values that must change at runtime in the browser.
- Deep nesting that hides specificity and makes overrides brittle.
- Global selectors, resets, or utility overrides that leak outside their intended
  layer or component boundary.
- Copying class strings, breakpoints, colors, or z-index values instead of using
  existing tokens and conventions.
- Hiding behavior-critical state only in color or motion without accessible text,
  focus, or reduced-motion alternatives.
- Treating formatter/linter success as proof that layout, cascade, accessibility,
  or browser compatibility is correct.

## Security And Evidence

Load [`security-review`](../security-review/SKILL.md) when styling work touches
CSP, external fonts/assets, user-generated HTML/CSS, template rendering, Markdown
or rich-text styling, inline styles with untrusted values, URL-valued CSS,
uploaded assets, or SSR injection paths. Use
[`security-review-evidence`](../security-review-evidence/SKILL.md) when reports
include screenshots, DOM excerpts, network traces, tokens, private URLs, or other
sensitive evidence.

## Successful Use

The final handoff states the styling system detected, CSS-vs-SCSS decision,
files changed, build/tooling impact, validation commands run, visual or browser
checks performed, and remaining browser/accessibility/performance risk.
