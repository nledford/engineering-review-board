#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence


GLOBAL_CONFIG_ROOT = Path.home() / ".config" / "opencode"
DEFINITION_ROOT_NAME = "opencode"
MANIFEST_NAME = "manifest.json"
DEFINITION_KINDS = ("agents", "commands")
DEFINITION_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")
COMMAND_FIELD_RE = re.compile(r"^([a-z][a-z0-9_-]*):\s*(.*)$")
COMMAND_AGENT_VALUE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
COMMAND_FIELDS = frozenset({"description", "agent", "model", "variant", "subtask"})


@dataclass(frozen=True)
class DefinitionInventory:
    agents: tuple[str, ...]
    commands: tuple[str, ...]

    def for_kind(self, kind: str) -> tuple[str, ...]:
        return getattr(self, kind)


@dataclass
class OperationResult:
    messages: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class OpenCodeInstallService:
    def __init__(
        self,
        repo_root: Path | str,
        config_root: Path | str = GLOBAL_CONFIG_ROOT,
    ) -> None:
        self.repo_root = Path(repo_root).expanduser().resolve()
        self.definition_root = self.repo_root / DEFINITION_ROOT_NAME
        self.config_root = Path(config_root).expanduser()
        self.sources = {
            kind: self.definition_root / kind
            for kind in DEFINITION_KINDS
        }
        self.destinations = {
            kind: self.config_root / kind
            for kind in DEFINITION_KINDS
        }

    def validate(self) -> OperationResult:
        inventory, errors = self._load_inventory()
        if inventory is None:
            return OperationResult(errors=errors)

        for kind in DEFINITION_KINDS:
            errors.extend(self._validate_kind(kind, inventory.for_kind(kind)))

        if not errors:
            errors.extend(self._validate_command_agents(inventory))

        if errors:
            return OperationResult(errors=errors)

        return OperationResult(
            messages=[
                "OpenCode definitions are valid: "
                f"agents={len(inventory.agents)} commands={len(inventory.commands)}"
            ]
        )

    def setup(self, *, dry_run: bool = False) -> OperationResult:
        validation = self.validate()
        if not validation.ok:
            return validation

        if self.config_root.exists() and not self.config_root.is_dir():
            return OperationResult(
                errors=["OpenCode config root exists but is not a directory"]
            )

        states, errors = self._inspect_destinations(missing_is_error=False)
        if errors:
            return OperationResult(errors=errors)

        messages: list[str] = []
        for kind in DEFINITION_KINDS:
            if states[kind] == "expected":
                messages.append(f"{kind} symlink is already configured")
            else:
                prefix = "Would create" if dry_run else "Created"
                messages.append(f"{prefix} {kind} symlink")

        if dry_run or all(state == "expected" for state in states.values()):
            return OperationResult(messages=messages)

        try:
            self.config_root.mkdir(parents=True, exist_ok=True)
        except OSError:
            return OperationResult(errors=["Could not create OpenCode config root"])
        created: list[str] = []
        active_kind = "OpenCode"
        try:
            for kind in DEFINITION_KINDS:
                if states[kind] == "expected":
                    continue
                active_kind = kind
                os.symlink(
                    self.sources[kind],
                    self.destinations[kind],
                    target_is_directory=True,
                )
                created.append(kind)
        except OSError:
            warnings = self._rollback_created(created)
            return OperationResult(
                errors=[f"Failed to create {active_kind} symlink; setup was rolled back"],
                warnings=warnings,
            )

        _, verification_errors = self._inspect_destinations(missing_is_error=True)
        if verification_errors:
            warnings = self._rollback_created(created)
            return OperationResult(
                errors=["OpenCode symlink verification failed; setup was rolled back"],
                warnings=warnings,
            )

        return OperationResult(messages=messages)

    def verify(self) -> OperationResult:
        validation = self.validate()
        if not validation.ok:
            return validation

        inventory, inventory_errors = self._load_inventory()
        if inventory is None:
            return OperationResult(errors=inventory_errors)

        _, errors = self._inspect_destinations(missing_is_error=True)
        if errors:
            return OperationResult(errors=errors)

        for kind in DEFINITION_KINDS:
            for name in inventory.for_kind(kind):
                visible_path = self.destinations[kind] / name
                if not visible_path.is_file():
                    errors.append(f"{kind}: '{name}' is not visible through the symlink")

        if errors:
            return OperationResult(errors=errors)

        return OperationResult(
            messages=[
                "OpenCode agents and commands symlinks are configured",
                "Visible OpenCode definitions: "
                f"agents={len(inventory.agents)} commands={len(inventory.commands)}",
            ]
        )

    def uninstall(self, *, dry_run: bool = False) -> OperationResult:
        states, errors = self._inspect_destinations(missing_is_error=False)
        if errors:
            return OperationResult(errors=errors)

        if all(state == "missing" for state in states.values()):
            return OperationResult(messages=["No managed OpenCode symlinks are installed"])

        if any(state != "expected" for state in states.values()):
            return OperationResult(
                errors=[
                    "OpenCode install is incomplete; refusing to remove either destination"
                ]
            )

        if dry_run:
            return OperationResult(
                messages=[
                    "Would remove agents symlink",
                    "Would remove commands symlink",
                ]
            )

        removed: list[str] = []
        active_kind = "OpenCode"
        try:
            for kind in DEFINITION_KINDS:
                active_kind = kind
                if self._destination_state(kind) != "expected":
                    raise OSError("destination changed during uninstall")
                self.destinations[kind].unlink()
                removed.append(kind)
        except OSError:
            warnings = self._restore_removed(removed)
            return OperationResult(
                errors=[
                    f"Failed to remove {active_kind} symlink; uninstall was rolled back"
                ],
                warnings=warnings,
            )

        return OperationResult(
            messages=["Removed agents symlink", "Removed commands symlink"]
        )

    def _load_inventory(self) -> tuple[DefinitionInventory | None, list[str]]:
        if self.definition_root.is_symlink() or not self.definition_root.is_dir():
            return None, ["OpenCode source root is missing or is not a regular directory"]

        manifest = self.definition_root / MANIFEST_NAME
        if manifest.is_symlink() or not manifest.is_file():
            return None, ["OpenCode manifest is missing or is not a regular file"]

        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None, ["OpenCode manifest is not valid UTF-8 JSON"]

        if not isinstance(data, dict) or set(data) != set(DEFINITION_KINDS):
            return None, ["OpenCode manifest must contain only agents and commands lists"]

        values: dict[str, tuple[str, ...]] = {}
        errors: list[str] = []
        for kind in DEFINITION_KINDS:
            entries = data.get(kind)
            if not isinstance(entries, list) or not all(
                isinstance(entry, str) for entry in entries
            ):
                errors.append(f"OpenCode manifest {kind} value must be a list of filenames")
                continue
            if entries != sorted(set(entries)):
                errors.append(
                    f"OpenCode manifest {kind} filenames must be sorted and unique"
                )
            invalid = [entry for entry in entries if not DEFINITION_NAME_RE.fullmatch(entry)]
            if invalid:
                errors.append(f"OpenCode manifest {kind} contains an invalid filename")
            values[kind] = tuple(entries)

        if errors:
            return None, errors

        return DefinitionInventory(
            agents=values["agents"],
            commands=values["commands"],
        ), []

    def _validate_kind(self, kind: str, expected: tuple[str, ...]) -> list[str]:
        root = self.sources[kind]
        if root.is_symlink() or not root.is_dir():
            return [f"{kind} source is missing or is not a regular directory"]

        try:
            observed = {path.name for path in root.iterdir()}
        except OSError:
            return [f"{kind} source directory is not readable"]
        expected_names = set(expected)
        errors = [
            f"{kind}: unexpected asset '{name}'"
            for name in sorted(observed - expected_names)
        ]
        errors.extend(
            f"{kind}: manifest asset missing '{name}'"
            for name in sorted(expected_names - observed)
        )

        for name in expected:
            path = root / name
            if path.is_symlink() or not path.is_file():
                errors.append(f"{kind}: '{name}' must be a regular non-symlink file")
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                errors.append(f"{kind}: '{name}' is not readable UTF-8")
                continue
            errors.extend(self._validate_markdown(kind, name, text))

        return errors

    @staticmethod
    def _validate_markdown(kind: str, name: str, text: str) -> list[str]:
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            return [f"{kind}: '{name}' is missing YAML frontmatter"]
        try:
            closing_index = lines.index("---", 1)
        except ValueError:
            return [f"{kind}: '{name}' has unterminated YAML frontmatter"]
        if not "\n".join(lines[closing_index + 1 :]).strip():
            return [f"{kind}: '{name}' has an empty prompt body"]
        return []

    def _validate_command_agents(self, inventory: DefinitionInventory) -> list[str]:
        agent_names = {Path(name).stem for name in inventory.agents}
        errors: list[str] = []
        for name in inventory.commands:
            command_path = self.sources["commands"] / name
            try:
                lines = command_path.read_text(encoding="utf-8").splitlines()
                closing_index = lines.index("---", 1)
            except (OSError, UnicodeError, ValueError):
                errors.append(f"commands: '{name}' could not be revalidated")
                continue

            fields: dict[str, str] = {}
            command_errors: list[str] = []
            for line in lines[1:closing_index]:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                if line[0].isspace():
                    command_errors.append(
                        f"commands: '{name}' metadata must use scalar top-level fields"
                    )
                    continue
                match = COMMAND_FIELD_RE.fullmatch(line)
                if match is None:
                    command_errors.append(
                        f"commands: '{name}' metadata must use canonical key-value fields"
                    )
                    continue
                key, value = match.groups()
                if key not in COMMAND_FIELDS:
                    command_errors.append(
                        f"commands: '{name}' has unsupported '{key}' field"
                    )
                    continue
                if key in fields:
                    command_errors.append(
                        f"commands: '{name}' has duplicate '{key}' field"
                    )
                    continue
                fields[key] = value

            if command_errors:
                errors.extend(command_errors)
                continue

            if "agent" not in fields:
                errors.append(f"commands: '{name}' must define exactly one agent")
                continue

            agent_name = fields["agent"]
            if COMMAND_AGENT_VALUE_RE.fullmatch(agent_name) is None:
                errors.append(f"commands: '{name}' must use a canonical bare agent name")
                continue
            if agent_name not in agent_names:
                errors.append(
                    f"commands: '{name}' references unknown agent '{agent_name}'"
                )
        return errors

    def _inspect_destinations(
        self,
        *,
        missing_is_error: bool,
    ) -> tuple[dict[str, str], list[str]]:
        states: dict[str, str] = {}
        errors: list[str] = []
        for kind in DEFINITION_KINDS:
            state = self._destination_state(kind)
            states[kind] = state
            if state == "missing" and missing_is_error:
                errors.append(f"{kind} destination is missing")
            elif state == "broken":
                errors.append(f"{kind} destination is a broken symlink")
            elif state == "foreign":
                errors.append(f"{kind} destination points somewhere else")
            elif state == "occupied":
                errors.append(
                    f"{kind} destination exists and is not a symlink; "
                    "move it aside manually"
                )
        return states, errors

    def _destination_state(self, kind: str) -> str:
        destination = self.destinations[kind]
        if destination.is_symlink():
            try:
                resolved = destination.resolve(strict=True)
            except (FileNotFoundError, RuntimeError, OSError):
                return "broken"
            return "expected" if resolved == self.sources[kind].resolve() else "foreign"
        if destination.exists():
            return "occupied"
        return "missing"

    def _rollback_created(self, created: list[str]) -> list[str]:
        warnings: list[str] = []
        for kind in reversed(created):
            destination = self.destinations[kind]
            if self._destination_state(kind) != "expected":
                warnings.append(f"Could not safely roll back {kind} symlink")
                continue
            try:
                destination.unlink()
            except OSError:
                warnings.append(f"Could not safely roll back {kind} symlink")
        return warnings

    def _restore_removed(self, removed: list[str]) -> list[str]:
        warnings: list[str] = []
        for kind in removed:
            destination = self.destinations[kind]
            if destination.exists() or destination.is_symlink():
                warnings.append(f"Could not safely restore {kind} symlink")
                continue
            try:
                os.symlink(
                    self.sources[kind],
                    destination,
                    target_is_directory=True,
                )
            except OSError:
                warnings.append(f"Could not safely restore {kind} symlink")
        return warnings


def emit_operation(result: OperationResult) -> int:
    for message in result.messages:
        print(message)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    return 0 if result.ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and install repository-managed OpenCode definitions."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--config-root",
        type=Path,
        default=GLOBAL_CONFIG_ROOT,
        help="OpenCode config root. Defaults to ~/.config/opencode.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("validate", help="Validate repository definitions.")

    setup_parser = subcommands.add_parser(
        "setup",
        help="Create the managed agents and commands symlinks.",
    )
    setup_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without applying them.",
    )

    subcommands.add_parser("verify", help="Verify definitions and both symlinks.")
    subcommands.add_parser("doctor", help="Validate definitions and both symlinks.")

    uninstall_parser = subcommands.add_parser(
        "uninstall",
        help="Remove both symlinks when this repository owns them.",
    )
    uninstall_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without applying them.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        service = OpenCodeInstallService(args.repo_root, args.config_root)
        if args.command == "validate":
            return emit_operation(service.validate())
        if args.command == "setup":
            return emit_operation(service.setup(dry_run=args.dry_run))
        if args.command in {"verify", "doctor"}:
            return emit_operation(service.verify())
        if args.command == "uninstall":
            return emit_operation(service.uninstall(dry_run=args.dry_run))
    except (OSError, RuntimeError, UnicodeError, ValueError):
        print("error: OpenCode operation failed safely", file=sys.stderr)
        return 1

    print(f"error: unsupported command: {args.command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
