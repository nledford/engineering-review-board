#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

try:
    from .opencode_contracts import (
        ALL_FIRST_PARTY_SKILL_IDS,
        CANONICAL_AGENT_SKILL_IDS,
        CANONICAL_AGENT_TOPOLOGY,
    )
except ImportError:
    from opencode_contracts import (
        ALL_FIRST_PARTY_SKILL_IDS,
        CANONICAL_AGENT_SKILL_IDS,
        CANONICAL_AGENT_TOPOLOGY,
    )


CORPUS_VERSION = 1
ROUTING_FIELDS = ("agent", "command", "skills", "handoffs")
LIST_ROUTING_FIELDS = ("skills", "handoffs")
MAX_PROMPT_CHARS = 4000
MAX_ROUTING_ITEMS = 64
MAX_RUN_LABEL_CHARS = 200
ROUTING_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,127}$")
CANONICAL_AGENTS_BY_ID = {
    policy.agent_id: policy for policy in CANONICAL_AGENT_TOPOLOGY.agents
}
CANONICAL_PRIMARY_AGENT_IDS = frozenset(
    policy.agent_id
    for policy in CANONICAL_AGENT_TOPOLOGY.agents
    if policy.mode == "primary"
)
CANONICAL_COMMAND_OWNERS = {
    policy.filename.removesuffix(".md"): policy.owner
    for policy in CANONICAL_AGENT_TOPOLOGY.commands
}
CANONICAL_FIRST_PARTY_SKILL_IDS = frozenset(ALL_FIRST_PARTY_SKILL_IDS)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    matched: int
    assertions: int
    failures: tuple[str, ...]
    actual: dict[str, object]

    @property
    def score(self) -> float:
        return self.matched / self.assertions if self.assertions else 0.0

    @property
    def passed(self) -> bool:
        return not self.failures


@dataclass(frozen=True)
class RunSummary:
    cases: tuple[CaseResult, ...]
    minimum_score: float

    @property
    def matched(self) -> int:
        return sum(case.matched for case in self.cases)

    @property
    def assertions(self) -> int:
        return sum(case.assertions for case in self.cases)

    @property
    def score(self) -> float:
        return self.matched / self.assertions if self.assertions else 0.0

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(
            f"{case.case_id}: {failure}"
            for case in self.cases
            for failure in case.failures
        )

    @property
    def passed(self) -> bool:
        return self.assertions > 0 and self.score >= self.minimum_score


def load_corpus(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read routing corpus {path}: {error}") from error
    errors = validate_corpus(data)
    if errors:
        raise ValueError("; ".join(errors))
    return data


def validate_corpus(corpus: object) -> list[str]:
    if not isinstance(corpus, dict):
        return ["corpus root must be an object"]
    errors = _validate_corpus_header(corpus)
    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        return [*errors, "cases must be a non-empty array"]
    errors.extend(_validate_cases(cases))
    return errors


def _validate_corpus_header(corpus: dict) -> list[str]:
    errors: list[str] = []
    if corpus.get("version") != CORPUS_VERSION:
        errors.append(f"version must be {CORPUS_VERSION}")
    errors.extend(
        _routing_id_errors(
            corpus.get("suite"),
            "suite",
        )
    )
    minimum_score = corpus.get("minimum_score")
    if not isinstance(minimum_score, (int, float)) or isinstance(
        minimum_score,
        bool,
    ):
        errors.append("minimum_score must be a number from 0 through 1")
    elif not 0 <= float(minimum_score) <= 1:
        errors.append("minimum_score must be a number from 0 through 1")
    return errors


def _validate_cases(cases: list[object]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(_validate_case(case, prefix, seen_ids))
    return errors


def _validate_case(
    case: dict,
    prefix: str,
    seen_ids: set[str],
) -> list[str]:
    errors = _validate_case_identity(case, prefix, seen_ids)
    if case.get("synthetic") is not True:
        errors.append(f"{prefix}.synthetic must be true")
    errors.extend(_validate_case_prompt(case.get("prompt"), prefix))

    expected = case.get("expected")
    forbidden = case.get("forbidden", {})
    if not isinstance(expected, dict) or not expected:
        return [*errors, f"{prefix}.expected must be a non-empty object"]
    if not isinstance(forbidden, dict):
        return [*errors, f"{prefix}.forbidden must be an object"]

    errors.extend(
        _unsupported_field_errors(
            expected,
            ROUTING_FIELDS,
            f"{prefix}.expected",
        )
    )
    errors.extend(
        _unsupported_field_errors(
            forbidden,
            LIST_ROUTING_FIELDS,
            f"{prefix}.forbidden",
        )
    )
    errors.extend(_validate_expected_route_ids(expected, prefix))
    errors.extend(_validate_route_item_fields(expected, f"{prefix}.expected"))
    errors.extend(_validate_route_item_fields(forbidden, f"{prefix}.forbidden"))
    return errors


def _validate_case_identity(
    case: dict,
    prefix: str,
    seen_ids: set[str],
) -> list[str]:
    case_id = case.get("id")
    errors = _routing_id_errors(case_id, f"{prefix}.id")
    if errors or not isinstance(case_id, str):
        return errors
    if case_id in seen_ids:
        return [f"{prefix}: duplicate case id: {case_id}"]
    seen_ids.add(case_id)
    return []


def _routing_id_errors(value: object, label: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [f"{label} must be a non-empty routing identifier"]
    if ROUTING_ID_RE.fullmatch(value) is None:
        return [
            f"{label} must be a lowercase routing identifier of at most 128 characters"
        ]
    return []


def _validate_case_prompt(prompt: object, prefix: str) -> list[str]:
    if not isinstance(prompt, str) or not prompt.strip():
        return [f"{prefix}.prompt must be a non-empty string"]
    if len(prompt) > MAX_PROMPT_CHARS:
        return [
            f"{prefix}.prompt must contain at most {MAX_PROMPT_CHARS} characters"
        ]
    return []


def _unsupported_field_errors(
    container: Mapping[str, object],
    supported_fields: Sequence[str],
    label: str,
) -> list[str]:
    unexpected = sorted(set(container) - set(supported_fields))
    if not unexpected:
        return []
    return [f"{label} has unsupported fields: {', '.join(unexpected)}"]


def _validate_expected_route_ids(expected: Mapping[str, object], prefix: str) -> list[str]:
    errors: list[str] = []
    for field in ("agent", "command"):
        if field in expected:
            errors.extend(
                _routing_id_errors(
                    expected[field],
                    f"{prefix}.expected.{field}",
                )
            )

    expected_agent = _canonical_expected_agent_id(expected)
    agent_value = expected.get("agent")
    if isinstance(agent_value, str) and not _routing_id_errors(
        agent_value,
        f"{prefix}.expected.agent",
    ):
        policy = CANONICAL_AGENTS_BY_ID.get(agent_value)
        if policy is None:
            errors.append(
                f"{prefix}.expected.agent must name a canonical registered primary agent: "
                f"{agent_value!r}"
            )
        elif policy.mode != "primary":
            errors.append(
                f"{prefix}.expected.agent must name a canonical primary agent; "
                f"{agent_value!r} is a registered subagent"
            )

    command = expected.get("command")
    if isinstance(command, str) and not _routing_id_errors(
        command,
        f"{prefix}.expected.command",
    ):
        command_owner = CANONICAL_COMMAND_OWNERS.get(command)
        if command_owner is None:
            errors.append(
                f"{prefix}.expected.command must name a canonical command: {command!r}"
            )
        elif expected_agent is None:
            errors.append(
                f"{prefix}.expected.command requires a canonical primary expected.agent"
            )
        elif command_owner != expected_agent:
            errors.append(
                f"{prefix}.expected.command {command!r} is owned by {command_owner!r}, "
                f"not expected.agent {expected_agent!r}"
            )

    skills = expected.get("skills")
    if isinstance(skills, list) and _valid_route_items(skills):
        if skills and expected_agent is None:
            errors.append(
                f"{prefix}.expected.skills requires a canonical primary expected.agent"
            )
        for skill in skills:
            if skill not in CANONICAL_FIRST_PARTY_SKILL_IDS:
                errors.append(
                    f"{prefix}.expected.skills contains unknown canonical skill {skill!r}"
                )
            elif expected_agent is not None and skill not in CANONICAL_AGENT_SKILL_IDS[
                expected_agent
            ]:
                errors.append(
                    f"{prefix}.expected.skills contains skill {skill!r} not allowed for "
                    f"expected.agent {expected_agent!r}"
                )

    handoffs = expected.get("handoffs")
    if isinstance(handoffs, list) and _valid_route_items(handoffs):
        for handoff in handoffs:
            if not isinstance(handoff, str):
                continue
            if handoff not in CANONICAL_AGENTS_BY_ID:
                errors.append(
                    f"{prefix}.expected.handoffs contains unknown registered agent {handoff!r}"
                )
            elif expected_agent is None:
                errors.append(
                    f"{prefix}.expected.handoffs requires a canonical primary expected.agent"
                )
            elif handoff not in CANONICAL_AGENTS_BY_ID[expected_agent].task_targets:
                errors.append(
                    f"{prefix}.expected.handoffs contains handoff {handoff!r} not permitted "
                    f"for expected.agent {expected_agent!r}"
                )
    return errors


def _canonical_expected_agent_id(expected: Mapping[str, object]) -> str | None:
    agent = expected.get("agent")
    if isinstance(agent, str) and agent in CANONICAL_PRIMARY_AGENT_IDS:
        return agent
    return None


def _validate_route_item_fields(
    container: Mapping[str, object],
    label: str,
) -> list[str]:
    errors: list[str] = []
    for field in LIST_ROUTING_FIELDS:
        if field in container and not _valid_route_items(container[field]):
            errors.append(
                f"{label}.{field} must be an array of at most "
                f"{MAX_ROUTING_ITEMS} unique lowercase routing identifiers"
            )
    return errors


def _valid_route_items(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) <= MAX_ROUTING_ITEMS
        and all(
            isinstance(item, str) and ROUTING_ID_RE.fullmatch(item) is not None
            for item in value
        )
        and len(value) == len(set(value))
    )


def _bounded_actual(actual: object) -> dict[str, object]:
    if not isinstance(actual, dict):
        return {}
    bounded: dict[str, object] = {}
    for field in ("agent", "command"):
        value = actual.get(field)
        if isinstance(value, str) and ROUTING_ID_RE.fullmatch(value) is not None:
            bounded[field] = value
    for field in LIST_ROUTING_FIELDS:
        value = actual.get(field)
        if isinstance(value, list):
            items: list[str] = []
            for item in value:
                if (
                    isinstance(item, str)
                    and ROUTING_ID_RE.fullmatch(item) is not None
                    and item not in items
                ):
                    items.append(item)
                if len(items) == MAX_ROUTING_ITEMS:
                    break
            bounded[field] = items
    return bounded


def evaluate_case(case: dict, actual: object) -> CaseResult:
    bounded = _bounded_actual(actual)
    expected = case["expected"]
    forbidden = case.get("forbidden", {})
    matched = 0
    assertions = 0
    failures: list[str] = []

    for field in ("agent", "command"):
        if field not in expected:
            continue
        assertions += 1
        if bounded.get(field) == expected[field]:
            matched += 1
        else:
            failures.append(
                f"expected {field} {expected[field]!r}, found {bounded.get(field)!r}"
            )

    for field in LIST_ROUTING_FIELDS:
        actual_values = bounded.get(field, [])
        if not isinstance(actual_values, list):
            actual_values = []
        for value in expected.get(field, []):
            assertions += 1
            if value in actual_values:
                matched += 1
            else:
                failures.append(f"expected {field} to contain {value!r}")
        for value in forbidden.get(field, []):
            assertions += 1
            if value not in actual_values:
                matched += 1
            else:
                failures.append(f"forbidden {field} contained {value!r}")

    return CaseResult(
        case_id=case["id"],
        matched=matched,
        assertions=assertions,
        failures=tuple(failures),
        actual=bounded,
    )


def run_suite(
    corpus: dict,
    *,
    runner: Sequence[str],
    model: str,
    configuration: str,
    trace_path: Path | None = None,
    timeout_seconds: int = 120,
) -> RunSummary:
    errors = validate_corpus(corpus)
    if errors:
        raise ValueError("; ".join(errors))
    if not runner:
        raise ValueError("runner command must not be empty")
    if not model.strip() or not configuration.strip():
        raise ValueError("model and configuration labels must be non-empty")
    if any(
        len(label) > MAX_RUN_LABEL_CHARS
        or any(ord(character) < 32 for character in label)
        for label in (model, configuration)
    ):
        raise ValueError(
            f"model and configuration labels must be printable and at most {MAX_RUN_LABEL_CHARS} characters"
        )

    results: list[CaseResult] = []
    trace_cases: list[dict[str, object]] = []
    for case in corpus["cases"]:
        payload = {
            "id": case["id"],
            "prompt": case["prompt"],
            "model": model,
            "configuration": configuration,
        }
        completed = subprocess.run(
            tuple(runner),
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"runner exited with {completed.returncode} for {case['id']}"
            )
        try:
            actual = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"runner returned invalid JSON for {case['id']}: {error}") from error
        result = evaluate_case(case, actual)
        results.append(result)
        trace_cases.append(
            {
                "id": case["id"],
                "prompt": case["prompt"],
                "actual": result.actual,
                "score": result.score,
                "failures": list(result.failures),
            }
        )

    summary = RunSummary(tuple(results), float(corpus["minimum_score"]))
    if trace_path is not None:
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_text(
            json.dumps(
                {
                    "suite": corpus["suite"],
                    "model": model,
                    "configuration": configuration,
                    "score": summary.score,
                    "minimum_score": summary.minimum_score,
                    "cases": trace_cases,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate or execute synthetic agent-routing evaluation corpora."
    )
    parser.add_argument("action", choices=("validate", "run"))
    parser.add_argument("corpus", type=Path)
    parser.add_argument(
        "--runner",
        help="Runner command string. Receives one JSON case on stdin and returns JSON on stdout.",
    )
    parser.add_argument("--model", help="Model identifier recorded with a live run.")
    parser.add_argument(
        "--configuration", help="Configuration or commit label recorded with a live run."
    )
    parser.add_argument(
        "--trace-out",
        type=Path,
        help="Explicit path for a bounded synthetic trace; no trace is written by default.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        corpus = load_corpus(args.corpus)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    if args.action == "validate":
        print(f"Routing corpus valid: {len(corpus['cases'])} synthetic cases.")
        return 0

    runner_text = args.runner or os.environ.get("ROUTING_EVAL_RUNNER", "")
    model = args.model or os.environ.get("ROUTING_EVAL_MODEL", "")
    configuration = args.configuration or os.environ.get(
        "ROUTING_EVAL_CONFIGURATION", ""
    )
    runner = tuple(shlex.split(runner_text))
    try:
        summary = run_suite(
            corpus,
            runner=runner,
            model=model,
            configuration=configuration,
            trace_path=args.trace_out,
        )
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    for failure in summary.failures:
        print(f"failure: {failure}", file=sys.stderr)
    print(
        f"Routing score: {summary.matched}/{summary.assertions} "
        f"({summary.score:.3f}); minimum={summary.minimum_score:.3f}"
    )
    return 0 if summary.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
