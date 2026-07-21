#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__:
    from .opencode_contracts import GLOBAL_CONFIG_ROOT
    from .opencode_install import OpenCodeInstallService, OperationResult
else:  # Direct script execution.
    from opencode_contracts import GLOBAL_CONFIG_ROOT
    from opencode_install import OpenCodeInstallService, OperationResult


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
