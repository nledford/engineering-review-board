"""Fail-closed parser for the repository's constrained OpenCode frontmatter."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field


TOP_LEVEL_FIELD_RE = re.compile(r"^([a-z][A-Za-z0-9_]*):(?:\s(.*))?$")
PERMISSION_LEVEL_RE = re.compile(
    r'^  (?:(?:"([^"\\]+)")|([a-z][a-z0-9_]*)):(?:\s(.*))?$'
)
PERMISSION_RULE_RE = re.compile(
    r'^    (?:"(.+)"|([a-z0-9][a-z0-9-]*)):\s*(allow|ask|deny)$'
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
COMMAND_FIELDS = frozenset({"description", "agent", "model", "variant", "subtask"})
AGENT_FIELDS = frozenset(
    {"description", "mode", "model", "reasoningEffort", "color", "permission"}
)
PERMISSION_ACTIONS = frozenset({"allow", "ask", "deny"})


@dataclass(frozen=True)
class ParsedFrontmatter:
    fields: dict[str, str | None]
    permissions: dict[str, str | tuple[tuple[str, str], ...]]
    closing_index: int


@dataclass
class _MetadataParser:
    kind: str
    name: str
    fields: dict[str, str | None] = field(default_factory=dict)
    permissions: dict[str, str | tuple[tuple[str, str], ...]] = field(
        default_factory=dict
    )
    errors: list[str] = field(default_factory=list)
    active_permission: str | None = None
    permission_rules: list[tuple[str, str]] = field(default_factory=list)

    def parse(self, lines: list[str]) -> None:
        for line in lines:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("    "):
                self._parse_rule(line)
            elif line.startswith("  "):
                self._finish_permission_rules()
                self._parse_permission(line)
            else:
                self._finish_permission_rules()
                self._parse_field(line)
        self._finish_permission_rules()

    def _finish_permission_rules(self) -> None:
        if self.active_permission is not None:
            self.permissions[self.active_permission] = tuple(self.permission_rules)
        self.active_permission = None
        self.permission_rules = []

    def _parse_rule(self, line: str) -> None:
        if self.active_permission is None:
            self.errors.append(
                f"{self.kind}: '{self.name}' metadata must use supported top-level fields"
            )
            return
        match = PERMISSION_RULE_RE.fullmatch(line)
        if match is None:
            self.errors.append(
                f"{self.kind}: '{self.name}' permission rules must use canonical key-value fields"
            )
            return
        quoted_key, named_key, action = match.groups()
        rule_key = self._decode_rule_key(quoted_key, named_key)
        if rule_key is None:
            return
        if any(existing == rule_key for existing, _ in self.permission_rules):
            self.errors.append(
                f"{self.kind}: '{self.name}' has duplicate permission rule '{rule_key}'"
            )
            return
        self.permission_rules.append((rule_key, action))

    def _decode_rule_key(
        self,
        quoted_key: str | None,
        named_key: str | None,
    ) -> str | None:
        if quoted_key is None:
            assert named_key is not None
            return named_key
        try:
            return json.loads(f'"{quoted_key}"')
        except json.JSONDecodeError:
            self.errors.append(
                f"{self.kind}: '{self.name}' permission rules must use "
                "supported double-quoted escapes"
            )
            return None

    def _parse_permission(self, line: str) -> None:
        if "permission" not in self.fields:
            self.errors.append(
                f"{self.kind}: '{self.name}' metadata must use scalar top-level fields"
            )
            return
        match = PERMISSION_LEVEL_RE.fullmatch(line)
        if match is None:
            self.errors.append(
                f"{self.kind}: '{self.name}' permission fields must use canonical key-value fields"
            )
            return
        quoted_key, named_key, value = match.groups()
        permission_key = quoted_key or named_key
        assert permission_key is not None
        if permission_key in self.permissions:
            self.errors.append(
                f"{self.kind}: '{self.name}' has duplicate permission '{permission_key}'"
            )
        elif value is None:
            self.active_permission = permission_key
        elif value not in PERMISSION_ACTIONS:
            self.errors.append(
                f"{self.kind}: '{self.name}' permission values must be allow, ask, or deny"
            )
        else:
            self.permissions[permission_key] = value

    def _parse_field(self, line: str) -> None:
        match = TOP_LEVEL_FIELD_RE.fullmatch(line)
        if match is None:
            self.errors.append(
                f"{self.kind}: '{self.name}' metadata must use canonical key-value fields"
            )
            return
        key, value = match.groups()
        allowed_fields = AGENT_FIELDS if self.kind == "agents" else COMMAND_FIELDS
        if key not in allowed_fields:
            self.errors.append(f"{self.kind}: '{self.name}' has unsupported '{key}' field")
        elif key in self.fields:
            self.errors.append(f"{self.kind}: '{self.name}' has duplicate '{key}' field")
        elif key == "permission":
            self._parse_permission_field(value)
        elif value is None or not value.strip():
            self.errors.append(
                f"{self.kind}: '{self.name}' field '{key}' must be a non-empty scalar"
            )
        else:
            self.fields[key] = value

    def _parse_permission_field(self, value: str | None) -> None:
        if value is not None:
            self.errors.append(f"{self.kind}: '{self.name}' permission must be a block")
        else:
            self.fields["permission"] = None


def _frontmatter_bounds(
    kind: str,
    name: str,
    lines: list[str],
) -> tuple[int | None, list[str]]:
    if not lines or lines[0] != "---":
        return None, [f"{kind}: '{name}' is missing YAML frontmatter"]
    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        return None, [f"{kind}: '{name}' has unterminated YAML frontmatter"]
    if not "\n".join(lines[closing_index + 1 :]).strip():
        return None, [f"{kind}: '{name}' has an empty prompt body"]
    return closing_index, []


def _markdown_fence_errors(
    kind: str,
    name: str,
    lines: list[str],
) -> list[str]:
    fence: tuple[str, int] | None = None
    for line in lines:
        match = FENCE_RE.fullmatch(line)
        if match is None:
            continue
        marker, suffix = match.groups()
        if fence is None:
            fence = (marker[0], len(marker))
        elif marker[0] == fence[0] and len(marker) >= fence[1] and not suffix.strip():
            fence = None
    return [f"{kind}: '{name}' has an unclosed Markdown code fence"] if fence else []


def parse_frontmatter(
    kind: str,
    name: str,
    text: str,
) -> tuple[ParsedFrontmatter | None, list[str]]:
    """Parse the supported scalar fields and permission-map subset.

    This deliberately does not implement YAML. Unsupported YAML forms fail
    closed so that the validator and OpenCode cannot interpret policy metadata
    differently without an explicit repository change.
    """
    lines = text.splitlines()
    closing_index, errors = _frontmatter_bounds(kind, name, lines)
    if closing_index is None:
        return None, errors
    parser = _MetadataParser(kind, name)
    parser.parse(lines[1:closing_index])
    parser.errors.extend(
        _markdown_fence_errors(kind, name, lines[closing_index + 1 :])
    )
    if parser.errors:
        return None, parser.errors
    return ParsedFrontmatter(parser.fields, parser.permissions, closing_index), []
