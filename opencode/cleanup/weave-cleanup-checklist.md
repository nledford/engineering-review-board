# Legacy Weave Cleanup Checklist

Use this after native OpenCode agents and commands are installed. Keep legacy
Tapestry references that preserve provenance, conversion, or cleanup history.

## Inventory

- Search for `.weave/`, Weave configuration/plugins, `call_weave_agent`, and
  Weave-only model or prompt fields.
- Classify Pattern, Tapestry, Loom, Shuttle, Warp, Weft, Thread, and Spindle
  references as active dependency, migration/provenance, historical record, or
  stale documentation.
- Check agent IDs, command owners, canonical plan paths, metadata fields, status
  values, and permission rule ordering.

## Remove Only Confirmed Stale Material

- Do not remove source Tapestry plans before `/convert-tapestry-plan` or
  `/normalize-plan` has preserved provenance and the destination is verified.
- Do not remove historical logs, snapshots, or records solely for terminology.
- Remove a reference only when it incorrectly states that Weave is installed or
  required by the current workflow.
- Keep live OpenCode configuration and credentials machine-local; do not copy
  them into a repository cleanup.

## Verify

- Confirm no command bypasses the Planning Coordinator for durable plan writes.
- Confirm no command asks the ERB to edit or executes an unapproved plan.
- Confirm native agents use valid IDs and no prompt claims delegation or
  persistence without an observed Task or artifact.
- Report remaining migration/provenance references, skipped checks, and residual
  risk rather than deleting uncertain material.
