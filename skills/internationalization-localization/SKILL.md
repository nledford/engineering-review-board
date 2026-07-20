---
name: internationalization-localization
description: Internationalization and localization guidance, including Project Fluent and Fluent Translation List (.ftl) files. Use when adding, changing, reviewing, or testing localized, multilingual, or localization-ready user-facing text, locale negotiation, translation catalogs, plural/select behavior, localized date/number formatting, or Fluent integrations in JavaScript, TypeScript, Python, Rust, or web UI. Do not use for fixed-language copyediting with no localization surface. Consult current official documentation for Fluent binding APIs and use security-review plus security-review-evidence when localized content crosses trust boundaries.
---

# Internationalization and Localization

Use this skill when software needs to present text, formatting, or UI behavior for
more than one locale. Internationalization (i18n) makes the product localizable;
localization (l10n) provides locale-specific messages, formats, and conventions.

Project Fluent is a localization system and message syntax designed to let
localizers express natural-language complexity such as plurals, gender, case,
conjugation, and word order in translation files instead of application code.
Fluent resources are usually written as Fluent Translation List (`.ftl`) files.

## Use When

- Adding or reviewing user-facing strings, message catalogs, locale folders,
  translation IDs, fallback chains, or locale negotiation.
- Writing or editing `.ftl` files, Fluent selectors, variables, terms,
  attributes, translator comments, or localized number/date formatting.
- Integrating Project Fluent through `fluent.js`, `python-fluent`, `fluent-rs`,
  or framework wrappers built on those packages.
- Testing locale-specific output, fallback behavior, missing translations,
  pseudolocalization, right-to-left/bidirectional layout, or accessibility text.

Do not use this skill for copyediting a single fixed-language message with no
localization surface. Use language engineering skills for implementation
mechanics, [`css-scss-styling`](../css-scss-styling/SKILL.md) for layout and
writing-direction styling, [`api-design`](../api-design/SKILL.md) for public
locale contract design, [`playwright-e2e`](../playwright-e2e/SKILL.md) for
browser-visible localization tests, and [`documentation-engineering`](../documentation-engineering/SKILL.md)
for docs-only localization guidance.

## Workflow

1. Inspect local conventions first: existing locale directories, source locale,
   message ID style, extraction/build scripts, package versions, fallback order,
   tests, and translation review workflow.
2. Treat American English (`en-US`) as the default/source locale unless the
   repository explicitly defines another source locale. Keep source messages clear
   and complete; do not use sentence fragments that force other languages to copy
   English grammar.
3. Decide whether the project needs full i18n or a smaller scoped change. Use
   Project Fluent when localizers need control over pluralization, grammatical
   variants, markup overlays, attributes, or cross-language word order; a simpler
   key/value library may be enough for a prototype or fixed internal tool.
4. Put language decisions in the catalog, not in application string assembly.
   Pass structured variables such as counts, dates, names, and states into Fluent;
   let the locale choose wording and order.
5. Design fallback before implementation. Typical order is requested locale,
   language fallback when supported, then `en-US`. Test missing-message and
   missing-variable behavior instead of assuming silent success.
6. Apply the negotiated BCP 47 language and script-aware direction with `lang`
   and `dir` on the document or localized subtree. Use logical CSS properties;
   do not infer direction from arbitrary user strings.
7. Consult current official upstream documentation before changing
   version-sensitive binding APIs, framework adapters, CLI tools, or
   parser/validator behavior.
8. Verify with the repository's parser, linter, typecheck, unit tests, snapshot
   tests, E2E tests, or build-time catalog validation.

## Fluent `.ftl` Authoring Rules

- Use stable, semantic message IDs: `checkout-submit`, `profile-greeting`,
  `error-network-timeout`. Avoid IDs that encode English text or UI position.
- Prefer complete sentences or complete UI labels. Do not concatenate localized
  fragments in code.
- Use variables/placeables for runtime data: `welcome = Welcome, { $user }!`.
  Keep variable names meaningful and pass typed values where the runtime supports
  locale-aware number/date formatting.
- Use selectors for plurals, gender, grammatical case, or state. Always include a
  default variant marked with `*`.

  ```ftl
  inbox-count =
      { $count ->
          [one] One message
         *[other] { $count } messages
      }
  ```

- Use CLDR plural categories such as `one`, `few`, `many`, and `other` instead
  of hard-coding English assumptions. Some languages do not use English-style
  plural forms; Japanese commonly uses one form where English uses singular and
  plural; Spanish needs gender and agreement in many messages.
- Use terms for reusable product vocabulary and brand names:

  ```ftl
  -brand-name = ExampleApp
  about-title = About { -brand-name }
  ```

- Use parameterized terms only when localizers need grammatical variants, such as
  case or gender. Do not expose terms directly as user-facing messages.
- Use attributes to group text for one UI element, including accessible labels:

  ```ftl
  email-input = Email
      .placeholder = name@example.com
      .aria-label = Email address
  ```

- Add translator comments for placeholders, ambiguous terms, character limits,
  tone, variables, and UI context. Use group or file comments for broader context.
- Keep `.ftl` indentation space-based. Preserve Unicode text. Escape literal
  braces or leading special characters according to Fluent syntax rules.

## Locale and Language Guidance

- Use BCP 47 locale tags such as `en-US`, `es`, `es-MX`, `ja`, or `ja-JP`.
  Store locale-specific files in predictable paths, for example
  `locales/en-US/app.ftl`, `locales/es/app.ftl`, and `locales/ja/app.ftl`, unless
  the repository already has a convention.
- Keep `en-US` complete. Other locales may be partial only if fallback behavior is
  intentional, visible in tests, and acceptable for the product.
- For Spanish, avoid baking gender, number, or formality choices into code. Let
  translators choose variants and agreement in `.ftl`.
- For Japanese, avoid assumptions about spaces, capitalization, or English plural
  categories. Let the message own sentence order and politeness level.
- Test long strings, short strings, missing translations, bidirectional content,
  pseudolocalized text, and accessible names. Test a real RTL locale and
  mixed-direction content, not only a flipped layout. Include screen-reader text
  and ARIA attributes in localization review when they are user-visible.

## Binding Guidance

Use local dependency versions and current upstream docs before changing APIs.

- JavaScript/TypeScript: `fluent.js` packages include `@fluent/bundle` for core
  `FluentBundle`/`FluentResource` formatting, `@fluent/syntax` for parsing and
  tooling, `@fluent/langneg` for locale negotiation, `@fluent/dom` for DOM
  localization, and `@fluent/react` for React integration. Use
  [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md)
  for package-manager, build, and type/test mechanics.
- Python: `python-fluent` provides `fluent.syntax` for parsing, serialization,
  AST tooling, and analysis; `fluent.runtime` for `FluentLocalization`,
  `FluentResourceLoader`, `format_value`, and `format_message`; and
  `fluent.pygments` for syntax highlighting. Use
  [`python-engineering`](../python-engineering/SKILL.md) for packaging, typing,
  tests, and Python implementation structure.
- Rust: `fluent-rs` includes crates such as `fluent`, `fluent-bundle`,
  `fluent-fallback`, `fluent-resmgr`, `fluent-syntax`, `fluent-pseudo`,
  `fluent-testing`, and `fluent-cli`. Low-level bundles format messages for a
  locale or locale chain; higher-level fallback/resource-manager crates can own
  resource loading and fallback. Use [`rust-engineering`](../rust-engineering/SKILL.md)
  and [`rust-testing-quality`](../rust-testing-quality/SKILL.md) for Rust code and
  quality gates.

## Testing and Validation

- Keep catalog and runtime validation separate. In the catalog lane, parse and
  add each resource with the repository's pinned binding or parser, checking parse
  and add-resource errors such as syntax failures, duplicate IDs, or missing
  default variants.
- In the runtime call-site lane, format through the pinned binding with
  representative arguments; cover selector branches, fallback, locale-specific
  number/date output, missing translations, unknown message, term, attribute, or
  function references, and missing-argument/error handling. Format every relevant
  message and attribute, or use a binding-specific semantic analyzer that proves
  equivalent reference coverage. Test message IDs and accessible labels at the
  call sites that render them.
- Add regression tests near the code that formats messages; add E2E coverage when
  locale affects layout, navigation, ARIA names, forms, direction, or user-visible
  flows.
- Use pseudolocalization or long-string fixtures to catch clipped text,
  concatenation assumptions, and layout coupling.

## Security and Accessibility

- Load [`security-review`](../security-review/SKILL.md) and
  [`security-review-evidence`](../security-review-evidence/SKILL.md) when
  localized content, locale tags, translation files, templates, Markdown/HTML,
  user-generated text, remote catalogs, or interpolation cross a trust boundary.
- Do not assume Fluent sanitizes output for every sink. Escape or sanitize for
  the target context, and do not insert translated strings into `innerHTML` unless
  an official, reviewed overlay mechanism is used safely.
- Treat translator-controlled markup and attributes as security-sensitive. In
  DOM/React integrations, prefer official Fluent overlay/component APIs and allow
  translated attributes only when the sink is safe and intentional.
- Validate and normalize locale inputs before using them in file paths, URLs,
  cache keys, or database queries.
- Localize visible labels, placeholders, titles, errors, and ARIA attributes
  together so screen-reader and keyboard users receive the same meaning as visual
  users.

## References

- Project Fluent syntax guide: <https://projectfluent.org/fluent/guide/>
- Fluent specification: <https://github.com/projectfluent/fluent>
- `fluent.js`: <https://github.com/projectfluent/fluent.js>
- `python-fluent`: <https://projectfluent.org/python-fluent/>
- `fluent-rs`: <https://github.com/projectfluent/fluent-rs>
