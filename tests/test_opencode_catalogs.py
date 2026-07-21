import json
import unittest
from pathlib import Path

from tools.opencode_contracts import (
    ALL_FIRST_PARTY_SKILL_IDS,
    CANONICAL_AGENT_SKILL_IDS,
    CANONICAL_AGENT_TOPOLOGY,
)
from tools.opencode_frontmatter import parse_frontmatter
from tools.skills_manager import SkillRegistry


from tests.opencode_test_support import (
    resolve_opencode_action,
)


class AuditRemediationContractTests(unittest.TestCase):
    def _checked_in_agent(self, name: str):
        project_root = Path(__file__).parents[1]
        parsed, errors = parse_frontmatter(
            "agents",
            f"{name}.md",
            (project_root / "opencode" / "agents" / f"{name}.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertEqual([], errors)
        assert parsed is not None
        return parsed

    def test_mutation_capable_mcp_prefixes_require_runtime_approval(self) -> None:
        for agent_name in ("engineering-lead", "implementation-worker"):
            parsed = self._checked_in_agent(agent_name)
            for pattern in (
                "playwright_*",
                "chrome-devtools_*",
                "serena_*",
                "hound_*",
                "github_*",
            ):
                with self.subTest(agent=agent_name, pattern=pattern):
                    self.assertEqual("ask", parsed.permissions[pattern])

    def test_agent_skill_catalogs_are_fail_closed_and_role_scoped(self) -> None:
        expected_allowed_skill = {
            "accessibility-critic": "ux-accessibility-review",
            "engineering-lead": "rust-engineering",
            "engineering-review-board": "code-review",
            "implementation-worker": "python-engineering",
            "plan-orchestrator": "git-commit",
            "technical-debt-auditor": "technical-debt-audit",
            "technical-researcher": "hound-web-research",
        }
        for agent_name, allowed_skill in expected_allowed_skill.items():
            parsed = self._checked_in_agent(agent_name)
            rules = parsed.permissions["skill"]
            self.assertIsInstance(rules, tuple)
            assert isinstance(rules, tuple)
            with self.subTest(agent=agent_name):
                self.assertEqual(
                    "deny",
                    resolve_opencode_action(rules, "find-skills", baseline="deny"),
                )
                self.assertEqual(
                    "allow",
                    resolve_opencode_action(rules, allowed_skill, baseline="deny"),
                )

    def test_agent_skill_catalog_registry_matches_first_party_inventory(self) -> None:
        project_root = Path(__file__).parents[1]
        first_party = {
            skill.name for skill in SkillRegistry.load(project_root).first_party()
        }

        self.assertEqual(first_party, set(ALL_FIRST_PARTY_SKILL_IDS))
        self.assertEqual(
            {policy.agent_id for policy in CANONICAL_AGENT_TOPOLOGY.agents},
            set(CANONICAL_AGENT_SKILL_IDS),
        )
        for agent_id, skill_ids in CANONICAL_AGENT_SKILL_IDS.items():
            with self.subTest(agent=agent_id):
                self.assertEqual(len(skill_ids), len(set(skill_ids)))
                self.assertLessEqual(set(skill_ids), first_party)

    def test_browser_evidence_collector_is_registered_and_ask_gated(self) -> None:
        project_root = Path(__file__).parents[1]
        manifest = json.loads(
            (project_root / "opencode/manifest.json").read_text(encoding="utf-8")
        )
        self.assertIn("browser-evidence-collector.md", manifest["agents"])
        parsed = self._checked_in_agent("browser-evidence-collector")
        self.assertEqual("ask", parsed.permissions["playwright_*"])
        self.assertEqual("ask", parsed.permissions["chrome-devtools_*"])
        self.assertEqual("deny", parsed.permissions["edit"])
        self.assertEqual("deny", parsed.permissions["task"])

    def test_audit_and_regression_commands_load_required_companions(self) -> None:
        project_root = Path(__file__).parents[1]
        audit = (
            project_root / "opencode/commands/audit-technical-debt.md"
        ).read_text(encoding="utf-8")
        regression = (
            project_root / "opencode/commands/investigate-regression.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "`dependency-supply-chain-review`, `security-review`, and "
            "`security-review-evidence`",
            audit,
        )
        self.assertIn(
            "Load `systematic-debugging` and `review-verification-protocol`.",
            regression,
        )
        self.assertIn(
            "hand off to `root-cause-analysis` only after the direct cause is understood",
            regression,
        )

    def test_technical_debt_auditor_supports_exact_non_rust_evidence_lanes(self) -> None:
        parsed = self._checked_in_agent("technical-debt-auditor")
        bash = parsed.permissions["bash"]
        self.assertIsInstance(bash, tuple)
        assert isinstance(bash, tuple)
        cases = (
            ("python3 -m pytest -q", "ask"),
            ("ruff check .", "ask"),
            ("npm run lint", "ask"),
            ("npm audit", "ask"),
            ("bundle exec rspec", "ask"),
            ("just check", "ask"),
            ("npm audit fix", "deny"),
            ("npm test -- --updateSnapshot", "deny"),
            ("bun test --update-snapshots", "deny"),
            ("pytest --snapshot-update", "deny"),
            ("bundle exec rubocop -A", "deny"),
            ("bundle exec rubocop --autocorrect", "deny"),
            ("bundle exec rubocop --auto-correct", "deny"),
            ("bundle exec rubocop --auto-gen-config", "deny"),
            ("bundle install", "deny"),
            ("npx eslint .", "deny"),
        )
        for command, expected in cases:
            with self.subTest(command=command):
                self.assertEqual(
                    expected,
                    resolve_opencode_action(bash, command, baseline="deny"),
                )
