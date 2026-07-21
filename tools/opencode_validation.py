"""Pure validation primitives shared by OpenCode definition checks.

The helpers in this module deliberately have no filesystem access.  Keeping the
contract evaluator pure lets callers validate an already-loaded definition and
lets tests exercise every contract token without rebuilding a repository.
"""

from __future__ import annotations

from dataclasses import dataclass


def normalize_prompt(text: str) -> str:
    """Collapse whitespace using the same rules as checked-in prompt contracts."""
    return " ".join(text.split())


def single_markdown_section(prompt: str, heading: str) -> str | None:
    """Return one normalized level-two section, rejecting duplicate headings."""
    lines = prompt.splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip() == heading]
    if len(matches) != 1:
        return None
    start = matches[0] + 1
    end = next(
        (
            index
            for index in range(start, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    return normalize_prompt("\n".join(lines[start:end]))


@dataclass(frozen=True)
class PromptContract:
    """Declarative requirements for a complete prompt or one of its sections."""

    required: tuple[str, ...] = ()
    forbidden: tuple[str, ...] = ()
    exact_counts: tuple[tuple[str, int], ...] = ()
    heading: str | None = None
    normalize_whitespace: bool = True


def prompt_satisfies_contract(prompt: str, contract: PromptContract) -> bool:
    """Return whether *prompt* satisfies all requirements in *contract*."""
    selected = (
        single_markdown_section(prompt, contract.heading)
        if contract.heading is not None
        else prompt
    )
    if selected is None:
        return False
    candidate = normalize_prompt(selected) if contract.normalize_whitespace else selected
    return (
        all(token in candidate for token in contract.required)
        and not any(token in candidate for token in contract.forbidden)
        and all(candidate.count(token) == count for token, count in contract.exact_counts)
    )
