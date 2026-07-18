from __future__ import annotations

import re
from typing import Sequence


MACHINE_SPECIFIC_PATH_PATTERNS = (
    (
        "machine-specific POSIX home path",
        re.compile(
            r"(?<![A-Za-z0-9_.-])/(?:Users|home)/"
            r"(?![<$%{])[A-Za-z0-9._-]+(?:/|(?=[\s`'\"),.;:}\]]|$))"
        ),
    ),
    (
        "machine-specific Windows home path",
        re.compile(
            r"(?i)(?<![A-Za-z0-9])(?:[A-Z]:[\\/])Users[\\/]"
            r"(?![<$%{])[^\\/\s`'\"]+"
        ),
    ),
)


def project_neutrality_errors(
    text: str,
    *,
    location: str,
    forbidden_identifiers: Sequence[str] = (),
) -> list[str]:
    errors: list[str] = []
    identifier_patterns = tuple(
        (
            identifier,
            re.compile(
                rf"(?i)(?<![A-Za-z0-9_-]){re.escape(identifier)}"
                rf"(?![A-Za-z0-9_-])"
            ),
        )
        for identifier in forbidden_identifiers
    )

    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in MACHINE_SPECIFIC_PATH_PATTERNS:
            if pattern.search(line):
                errors.append(
                    f"{location}:{line_number}: contains a {label}; "
                    "use a placeholder or repository-relative path"
                )
        for identifier, pattern in identifier_patterns:
            if pattern.search(line):
                errors.append(
                    f"{location}:{line_number}: contains source-project identifier "
                    f"'{identifier}'; reusable skill guidance must be project-neutral"
                )
    return errors
