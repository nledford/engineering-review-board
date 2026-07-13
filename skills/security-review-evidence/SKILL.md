---
name: security-review-evidence
description: Companion evidence checklist for security-sensitive changes and reviews. Use only with security-review, threat-modeling, or dependency-supply-chain-review to keep evidence sanitized, scoped, and tied to repository policy. Do not use as standalone security analysis.
user-invocable: false
---

# Security Review Evidence

Use this skill when a change touches authentication, authorization, crypto,
certificates, tokens, signatures, sessions, secrets, passwords, CORS, CSP, CSRF,
`.env` handling, credential handling, trust boundaries, security-sensitive input
validation, file import/export paths, plugin or extension trust roots, browser
artifacts, or related commands/docs.

Use this skill only as evidence support for the owning security workflow:
[`security-review`](../security-review/SKILL.md) for implemented controls,
[`threat-modeling`](../threat-modeling/SKILL.md) for design-time risks, or
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
for dependency and provenance risk. This skill owns collection, redaction, and
reporting guardrails, not the security analysis itself.

## Source of Truth

- First inspect the repository for security guidance such as `SECURITY.md`,
  `AGENTS.md`, `docs/security*`, threat models, runbooks, CI security jobs, or
  review templates.
- Prefer existing validation commands and evidence templates over inventing a new
  checklist.
- If no repository policy exists, use this skill as the minimum evidence
  checklist and state that no project-specific policy was found.

## Evidence to Collect

- Record **pre-change** and **post-change** security evidence for each
  security-sensitive change; if a checkpoint is impossible, say why.
- Name the affected route classes, commands, docs, helper scripts, deployment
  surfaces, browser artifacts, storage paths, or trust boundaries.
- Cover authentication, authorization, sessions, CORS, CSP, CSRF, MFA,
  throttling, and secret handling where applicable.
- For secrets and credentials, record lifecycle checkpoints for generation,
  storage, scope, rotation, revocation, destruction, backup/log exposure,
  fixture or test handling, and post-test cleanup. Use sanitized control names
  and locations, never raw values.
- For import/export or filesystem work, confirm raw host paths, canonical paths,
  cache payloads, task payloads, and command output are redacted where needed.
- For plugin, extension, or script execution work, identify trust roots, managed
  roots, path boundaries, and untrusted inputs without exposing private
  filesystem details.
- For dependency or supply-chain work, capture sanitized evidence for the
  package, binary, script, generated code, lockfile, provenance, checksum or
  signature, install hooks, advisory state, and dependency-audit result.
  Redact private registry hosts, tokens, credentials, local cache paths, and
  customer or organization names when they are sensitive.
- For browser/frontend evidence, treat screenshots, traces, videos, storage
  state, HAR/network dumps, downloads, reports, credentialed URLs, and live data
  as local ignored artifacts by default. Record sanitized artifact classes,
  redactions, policy or explicit approval, access boundary, and cleanup evidence
  before anything is retained or shared.

## Secrets and Credential Lifecycle Checkpoints

- **Generation:** identify the approved generator or secret source, required
  entropy, uniqueness, TTL, and whether test fixtures use deterministic or fake
  values instead of live credentials.
- **Storage:** identify the storage class only, such as secret manager, CI
  variable, keychain, encrypted database column, or local test fixture. Do not
  name or print the secret value, `.env` contents, raw DSN, or private file path.
- **Scope:** record the intended audience, permissions, tenant/project boundary,
  environment, expiration, and least-privilege constraints.
- **Rotation and revocation:** confirm the rotation path, revocation trigger,
  rollback behavior, and how old credentials become unusable.
- **Destruction and cleanup:** confirm generated test credentials, temporary
  tokens, fixture accounts, temporary keys, and local secret files are deleted,
  expired, revoked, or replaced with non-live placeholders after verification.
- **Backup and log exposure:** check whether backups, audit logs, telemetry,
  traces, crash reports, dependency audit output, or command output could retain
  credential material. Record only sanitized results.

## Forbidden Outputs

Never print, commit, paste, publish, or attach `.env` contents, secret files,
private keys, cookies, tokens, CSRF values, password hashes, credential material,
credentialed database URLs, browser storage state, raw import paths, raw browser
artifacts, or private host paths. Use placeholders such as `<redacted>`,
`<local-secret-file>`, `<credentialed-url>`, `<private-registry>`, or
`<private-path>`.

## Artifact Cleanup Expectations

- Treat security traces, screenshots, videos, storage state, HAR/network dumps,
  downloads, reports, logs, credentialed URLs, live data, dependency audit
  output, temporary databases, export files, reproduced exploit payloads,
  fuzzing/minimized payloads, and generated fixtures as sensitive until reviewed
  and cleaned.
- Prefer writing raw artifacts to documented local temporary or ignored artifact
  locations that can be deleted after review. Do not move raw artifacts into the
  repository, issue trackers, PR comments, shared chat, or persistent reports.
- The safe override path for sharing or retention is: sanitized artifact,
  documented repository policy or explicit approval, and security evidence that
  records redactions, retained class/location, access boundary, and cleanup.
- Before reporting, inspect artifact names and sanitized summaries for secrets,
  credentialed URLs, cookies, tokens, private paths, customer data, exploit
  payloads, and private dependency or registry details.
- Delete or securely dispose of raw security artifacts after extracting sanitized
  evidence. If retention is required by project policy or explicit approval,
  record the retention class, access boundary, and cleanup/expiry expectation
  without exposing private paths or contents.
- Clean temporary databases, local export files, fixture credentials, generated
  payload files, and dependency audit logs after tests. Prefer automated cleanup
  in tests or teardown scripts over manual deletion.

## Reporting Cleanup Gaps

When cleanup cannot be verified, report all of the following:

- Artifact or credential class, not the raw path or value.
- What cleanup was attempted or expected.
- Why cleanup could not be confirmed, such as missing permissions, external CI
  retention, policy-managed retention, test crash before teardown, or unavailable
  audit access.
- Residual exposure risk and who must follow up.
- Any safe remediation command, ticket, or repository-owned cleanup process,
  with placeholders for private paths and identifiers.

## Verification Expectations

- Prefer repository-owned validation recipes when they exist; cite exact commands
  run and sanitized pass/fail results.
- Do not treat search output, screenshots containing secrets, or raw logs as
  shareable security evidence.
- If verification is skipped or partial, report the missing control, why it was
  not checked, and the residual risk.
