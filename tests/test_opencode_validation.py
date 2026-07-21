import json
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from tools.opencode_install import OpenCodeInstallService
from tools.opencode_validation import (
    PromptContract,
    prompt_satisfies_contract,
    single_markdown_section,
)


class PromptContractTests(unittest.TestCase):
    def test_contract_supports_sections_normalization_and_forbidden_tokens(self) -> None:
        prompt = """# Agent

## Contract

Required   wording is present.
No retired route appears here.
"""
        contract = PromptContract(
            heading="## Contract",
            required=("Required wording is present.",),
            forbidden=("automatic route",),
        )

        self.assertTrue(prompt_satisfies_contract(prompt, contract))
        self.assertFalse(
            prompt_satisfies_contract(
                prompt.replace("No retired route", "An automatic route"),
                contract,
            )
        )

    def test_contract_rejects_missing_or_duplicate_sections(self) -> None:
        contract = PromptContract(
            heading="## Contract",
            required=("Required wording",),
        )
        missing = "# Agent\n\nRequired wording\n"
        duplicate = (
            "## Contract\n\nRequired wording\n\n"
            "## Contract\n\nRequired wording\n"
        )

        self.assertFalse(prompt_satisfies_contract(missing, contract))
        self.assertFalse(prompt_satisfies_contract(duplicate, contract))
        self.assertIsNone(single_markdown_section(duplicate, "## Contract"))

    def test_contract_can_require_exact_token_counts(self) -> None:
        contract = PromptContract(exact_counts=(("safety invariant", 1),))

        self.assertTrue(prompt_satisfies_contract("safety invariant", contract))
        self.assertFalse(
            prompt_satisfies_contract(
                "safety invariant and safety invariant",
                contract,
            )
        )


class DefinitionSnapshotIntegrationTests(unittest.TestCase):
    def test_validate_reads_each_manifested_definition_once(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        manifest = json.loads(
            (project_root / "opencode" / "manifest.json").read_text(encoding="utf-8")
        )
        definition_paths = {
            (project_root / "opencode" / kind / name).resolve()
            for kind in ("agents", "commands")
            for name in manifest[kind]
        }
        reads: Counter[Path] = Counter()
        original_read_text = Path.read_text

        def counting_read_text(path: Path, *args, **kwargs) -> str:
            resolved = path.resolve()
            if resolved in definition_paths:
                reads[resolved] += 1
            return original_read_text(path, *args, **kwargs)

        with patch.object(Path, "read_text", counting_read_text):
            result = OpenCodeInstallService(
                project_root,
                project_root / "test-config",
            ).validate()

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(definition_paths, set(reads))
        self.assertEqual(
            {},
            {str(path): count for path, count in reads.items() if count != 1},
        )


if __name__ == "__main__":
    unittest.main()
