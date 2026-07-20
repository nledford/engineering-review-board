---
name: powershell-engineering
description: Cross-platform PowerShell engineering guidance. Use when creating, changing, reviewing, or testing `.ps1`, `.psm1`, or `.psd1` files, PowerShell functions/modules, Pester tests, PSScriptAnalyzer configuration, native-command orchestration, or Windows/macOS/Linux PowerShell automation. Do not use merely to run an existing PowerShell command or for generic script-language selection with no PowerShell implementation.
---

# PowerShell Engineering

Use this skill for idiomatic, testable PowerShell that behaves deliberately on
its supported platforms. Use [`script-engineering`](../script-engineering/SKILL.md)
when deciding whether the behavior belongs in a script or whether PowerShell is
preferable to shell, Python, Ruby, or JavaScript.

## Workflow

1. Inspect repository instructions, `.ps1`, `.psm1`, `.psd1`, module manifests,
   required modules, Pester/PSScriptAnalyzer configuration, task runners, CI,
   documentation, and supported host matrix.
2. Establish the minimum PowerShell edition and version. Distinguish PowerShell
   7+ (`pwsh`) from Windows PowerShell (`powershell.exe`); support both only when
   repository evidence requires both.
3. Identify platform-specific commands, providers, paths, encodings, native
   executables, permissions, and modules before claiming cross-platform support.
4. Define parameters, pipeline behavior, output objects and streams, errors,
   native exit codes, side effects, idempotence, and `-WhatIf` behavior.
5. Implement small advanced functions or modules with explicit boundaries and
   direct command invocation.
6. Run parser/static checks and focused Pester tests, then validate on every
   claimed operating-system and PowerShell-version target where practical.
7. Report the tested matrix, skipped targets, dependencies, commands, and
   remaining platform risk.

## Edition And Platform Contract

- Prefer current PowerShell 7 for new cross-platform scripts. Do not claim that
  a script is cross-platform merely because `pwsh` runs on Windows, macOS, and
  Linux; every cmdlet, module, provider, native executable, path, and data format
  must also exist or have an intentional adapter.
- Treat Windows PowerShell 5.1 compatibility as a separate target with older
  language, .NET, module, encoding, and native-command behavior. Avoid dual
  support unless consumers require it and the repository tests it.
- Use `$PSVersionTable` and the repository's declared matrix as evidence. Keep
  platform branches small and test each branch; prefer capability detection when
  it expresses the real requirement better than an operating-system name.
- Consult current official PowerShell, Pester, PSScriptAnalyzer, or module
  documentation after determining pinned versions.

## Idiomatic PowerShell

- Write reusable commands as advanced functions with approved `Verb-Noun`
  names, `[CmdletBinding()]`, explicit parameters, validation attributes, help,
  and pipeline semantics where pipeline input is a real part of the contract.
- Emit objects from reusable functions. Leave formatting to callers or dedicated
  format views; do not replace structured output with preformatted strings.
- Use full cmdlet and parameter names in durable scripts. Interactive aliases,
  positional ambiguity, and implicit command discovery reduce readability and
  portability.
- Use splatting and argument arrays for readable calls. Invoke native programs
  with `&` and separate arguments; never construct executable command text for
  `Invoke-Expression`.
- Keep success output distinct from error, warning, verbose, debug, information,
  and progress streams. Do not use `Write-Host` as a machine-readable result.
- Use `Join-Path`, `Split-Path`, `Resolve-Path`, `Test-Path`, literal-path
  parameters, and .NET path APIs deliberately. Do not hard-code path separators,
  drive letters, case-insensitive matching, or a caller working directory.
- Choose file encodings and newline expectations explicitly at boundaries.
  Account for different defaults across PowerShell editions and external tools.
- Keep module import and script load behavior cheap and deterministic. Avoid
  profile dependencies and mutation of caller-global preference variables.

## Errors And Native Commands

- Distinguish non-terminating PowerShell errors, terminating errors, and native
  process failures. Use `-ErrorAction Stop` at boundaries that must enter
  `try`/`catch`; do not assume every cmdlet failure terminates automatically.
- Catch only errors the current boundary can handle. Preserve useful error
  records and context, use `finally` for cleanup, and fail with a nonzero process
  result when the script contract fails.
- Inspect `$LASTEXITCODE` after native commands when their success matters. A
  native nonzero exit is not universally equivalent to a catchable PowerShell
  exception across supported versions.
- Avoid broad `SilentlyContinue`, empty catches, output suppression that hides
  failure, and global `$ErrorActionPreference` changes that leak to callers.

## Safe Side Effects

- For functions that change state, use
  `[CmdletBinding(SupportsShouldProcess)]` and call
  `$PSCmdlet.ShouldProcess()` close to each mutation so `-WhatIf` and `-Confirm`
  participate in the normal PowerShell contract.
- Do not implement a separate `-WhatIf` switch or rely on `Read-Host` as the
  only safety gate. Validate the exact target even in preview mode.
- Keep destructive, privileged, credentialed, and remote operations explicit,
  idempotent where possible, and bounded by repository and agent authority.
- Never embed credentials or print secure values. Use established secret stores
  and credential types without converting secrets to ordinary strings merely for
  convenience.

## Cross-Platform Checklist

Verify, rather than assume:

- command and module availability on Windows, macOS, and Linux targets;
- filesystem roots, separators, case behavior, permissions, symlinks, and
  executable discovery;
- environment-variable names and platform-provided values;
- text encoding, BOM, newline, locale, culture, and date/number formatting;
- native argument passing, stdout/stderr treatment, signal and exit behavior;
- registry, services, event logs, COM, WMI/CIM, and other Windows-only providers;
  and
- container, CI, remoting, authentication, and module-install assumptions.

Isolate unavoidable platform behavior behind small functions or adapters instead
of spreading `$IsWindows`, `$IsMacOS`, or `$IsLinux` branches throughout the
script.

## Test PowerShell

Use the repository's Pester version and conventions. Do not mix Pester major
syntax or configuration without checking the installed version.

- **Unit:** test pure functions, parameter validation, object shapes,
  transformations, error contracts, and `ShouldProcess` decisions.
- **Integration:** exercise real modules, filesystems, native processes,
  environment boundaries, and platform adapters with isolated temporary state.
- **End to end:** invoke the script or module entry point when parameters,
  streams, host interaction, side effects, or process exit status are the
  behavior under test.
- Use Pester's isolated filesystem facilities or repository-owned temporary
  directories. Mock external boundaries selectively; do not mock the function or
  behavior being specified.
- Run tests on every claimed OS and PowerShell edition/version. Static
  compatibility analysis helps find gaps but does not replace target execution.

Use the repository's parser or import smoke check and configured
PSScriptAnalyzer settings. PSScriptAnalyzer can check scripts, modules, manifests,
style, defects, and configured compatibility profiles; review intentional
suppressions rather than disabling broad rule sets.

Typical commands to derive from repository evidence include:

```powershell
Invoke-ScriptAnalyzer -Path ./scripts -Recurse
Invoke-Pester -Path ./tests
pwsh -NoProfile -File ./scripts/example.ps1
```

Use [`test-driven-development`](../test-driven-development/SKILL.md) for behavior
changes and regressions, and [`systematic-debugging`](../systematic-debugging/SKILL.md)
for active unexplained PowerShell failures.

## Anti-Patterns

Avoid:

- aliases and unexplained positional parameters in checked-in scripts;
- text parsing when cmdlets or APIs already return objects;
- `Invoke-Expression`, interpolated command strings, and unvalidated paths;
- `Write-Host` as data output or output formatting inside reusable functions;
- broad preference-variable changes, global state, profile dependence, and
  import-time side effects;
- Windows-only commands, backslash paths, CRLF, case-insensitivity, or drive
  assumptions in code labeled cross-platform;
- treating native stderr as automatic failure or forgetting `$LASTEXITCODE`;
- ad hoc confirmations instead of `SupportsShouldProcess`; and
- claiming cross-platform support after testing only one host.

## Security And Completion

Load [`security-review`](../security-review/SKILL.md) for untrusted parameters,
paths, command execution, remoting, credentials, privileged operations, or
destructive targets. Use
[`security-review-evidence`](../security-review-evidence/SKILL.md) when command
output, transcripts, test artifacts, or reports may contain sensitive values.
Load [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
for modules, galleries, installers, signatures, checksums, or provenance.

Before handoff, report supported and actually tested hosts, PowerShell versions,
Pester and analyzer evidence, side-effect and `-WhatIf` coverage, skipped matrix
entries, and residual compatibility or security risk.
