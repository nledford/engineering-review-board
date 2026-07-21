import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.opencode_install import OpenCodeInstallService
from tools.opencode_manager import main


from tests.opencode_test_support import (
    create_expected_links,
    create_opencode_repo,
    snapshot_tree,
)


class OpenCodeInstallServiceTests(unittest.TestCase):
    def test_setup_creates_both_directory_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"

            result = OpenCodeInstallService(repo, config_root).setup()

            self.assertTrue(result.ok)
            for kind in ("agents", "commands"):
                target = config_root / kind
                self.assertTrue(target.is_symlink())
                self.assertEqual((repo / "opencode" / kind).resolve(), target.resolve())

    def test_setup_is_idempotent_for_correct_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root)

            result = OpenCodeInstallService(repo, config_root).setup()

            self.assertTrue(result.ok)
            self.assertEqual(2, sum("already configured" in message for message in result.messages))

    def test_setup_accepts_relative_links_to_expected_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root, relative=True)

            result = OpenCodeInstallService(repo, config_root).setup()

            self.assertTrue(result.ok)

    def test_setup_dry_run_does_not_create_parent_or_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "missing"

            result = OpenCodeInstallService(repo, config_root).setup(dry_run=True)

            self.assertTrue(result.ok)
            self.assertFalse(config_root.exists())
            self.assertEqual(2, sum("Would create" in message for message in result.messages))

    def test_setup_preflights_both_destinations_before_mutating(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            (config_root / "commands").mkdir(parents=True)

            result = OpenCodeInstallService(repo, config_root).setup()

            self.assertFalse(result.ok)
            self.assertFalse((config_root / "agents").exists())
            self.assertTrue((config_root / "commands").is_dir())

    def test_setup_refuses_foreign_symlink_without_mutating_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            foreign = root / "foreign"
            foreign.mkdir()
            config_root.mkdir()
            os.symlink(foreign, config_root / "commands")

            result = OpenCodeInstallService(repo, config_root).setup()

            self.assertFalse(result.ok)
            self.assertFalse((config_root / "agents").exists())
            self.assertEqual(foreign.resolve(), (config_root / "commands").resolve())

    def test_setup_refuses_broken_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            config_root.mkdir()
            os.symlink(root / "missing", config_root / "commands")

            result = OpenCodeInstallService(repo, config_root).setup()

            self.assertFalse(result.ok)
            self.assertIn("broken symlink", result.errors[0])
            self.assertFalse((config_root / "agents").exists())

    def test_setup_rolls_back_first_link_if_second_creation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            real_symlink = os.symlink
            call_count = 0

            def fail_second_link(source: str, target: str, *, target_is_directory: bool, dir_fd: int) -> None:
                nonlocal call_count
                call_count += 1
                if call_count == 2:
                    raise OSError("injected failure")
                real_symlink(source, target, target_is_directory=target_is_directory, dir_fd=dir_fd)

            with patch("tools.opencode_install.os.symlink", side_effect=fail_second_link):
                result = OpenCodeInstallService(repo, config_root).setup()

            self.assertFalse(result.ok)
            self.assertFalse((config_root / "agents").exists())
            self.assertFalse((config_root / "commands").exists())

    def test_verify_confirms_both_links_and_visible_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root)

            result = OpenCodeInstallService(repo, config_root).verify()

            self.assertTrue(result.ok)
            self.assertIn("agents=1", result.messages[-1])
            self.assertIn("commands=1", result.messages[-1])

    def test_verify_rejects_one_sided_installation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            config_root.mkdir()
            os.symlink(repo / "opencode" / "agents", config_root / "agents")

            result = OpenCodeInstallService(repo, config_root).verify()

            self.assertFalse(result.ok)
            self.assertTrue(any("commands destination is missing" in error for error in result.errors))

    def test_uninstall_removes_only_the_expected_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root)

            result = OpenCodeInstallService(repo, config_root).uninstall()

            self.assertTrue(result.ok)
            self.assertFalse((config_root / "agents").exists())
            self.assertFalse((config_root / "commands").exists())
            self.assertTrue((repo / "opencode" / "agents" / "reviewer.md").is_file())

    def test_uninstall_dry_run_preserves_expected_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root)

            result = OpenCodeInstallService(repo, config_root).uninstall(dry_run=True)

            self.assertTrue(result.ok)
            self.assertTrue((config_root / "agents").is_symlink())
            self.assertTrue((config_root / "commands").is_symlink())

    def test_uninstall_is_idempotent_when_both_links_are_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)

            result = OpenCodeInstallService(repo, root / "config").uninstall()

            self.assertTrue(result.ok)
            self.assertIn("No managed OpenCode symlinks", result.messages[0])

    def test_uninstall_refuses_mixed_ownership_without_removing_expected_link(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            config_root.mkdir()
            os.symlink(repo / "opencode" / "agents", config_root / "agents")
            (config_root / "commands").mkdir()

            result = OpenCodeInstallService(repo, config_root).uninstall()

            self.assertFalse(result.ok)
            self.assertTrue((config_root / "agents").is_symlink())
            self.assertTrue((config_root / "commands").is_dir())

    def test_operation_messages_do_not_expose_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            (config_root / "commands").mkdir(parents=True)

            result = OpenCodeInstallService(repo, config_root).setup()

            output = "\n".join([*result.messages, *result.warnings, *result.errors])
            self.assertNotIn(str(root), output)

    def test_cli_sanitizes_config_parent_creation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_parent = root / "not-a-directory"
            config_parent.write_text("occupied\n", encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(
                    [
                        "--repo-root",
                        str(repo),
                        "--config-root",
                        str(config_parent / "opencode"),
                        "setup",
                    ]
                )

            self.assertEqual(1, exit_code)
            output = stdout.getvalue() + stderr.getvalue()
            self.assertNotIn("Traceback", output)
            self.assertNotIn(str(root), output)

    def test_cli_sanitizes_command_read_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            stdout = io.StringIO()
            stderr = io.StringIO()
            original_read_text = Path.read_text

            def fail_command_read(
                path: Path,
                encoding: str | None = None,
                errors: str | None = None,
            ) -> str:
                if path.parent.name == "commands":
                    raise PermissionError("injected private path")
                return original_read_text(path, encoding=encoding, errors=errors)

            with (
                patch.object(Path, "read_text", new=fail_command_read),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
            ):
                exit_code = main(
                    [
                        "--repo-root",
                        str(repo),
                        "--config-root",
                        str(root / "config"),
                        "validate",
                    ]
                )

            self.assertEqual(1, exit_code)
            output = stdout.getvalue() + stderr.getvalue()
            self.assertNotIn("Traceback", output)
            self.assertNotIn(str(root), output)

    def test_cli_sanitizes_service_construction_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(
                    Path,
                    "resolve",
                    side_effect=RuntimeError("injected private path"),
                ),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
            ):
                exit_code = main(
                    [
                        "--repo-root",
                        str(repo),
                        "--config-root",
                        str(root / "config"),
                        "validate",
                    ]
                )

            self.assertEqual(1, exit_code)
            output = stdout.getvalue() + stderr.getvalue()
            self.assertNotIn("Traceback", output)
            self.assertNotIn(str(root), output)

    def test_setup_creates_two_links_and_verify_requires_visible_definitions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            service = OpenCodeInstallService(repo, config_root)
            self.assertTrue(service.setup().ok)
            self.assertEqual(
                {"agents", "commands"},
                {path.name for path in config_root.iterdir()},
            )
            self.assertTrue(service.verify().ok)
            (repo / "opencode" / "commands" / "review.md").unlink()
            self.assertFalse(service.verify().ok)

    def test_setup_refuses_unsafe_missing_parent_and_safe_final_root_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            unsafe = OpenCodeInstallService(repo, root / "missing" / "opencode")
            self.assertFalse(unsafe.setup().ok)
            self.assertFalse((root / "missing").exists())
            safe_root = root / "safe" / "opencode"
            safe_root.parent.mkdir()
            service = OpenCodeInstallService(repo, safe_root)
            self.assertTrue(service.setup().ok)
            self.assertTrue(safe_root.is_dir())

    def test_root_swap_before_create_is_fail_closed_and_leaves_sentinel_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            config_root.mkdir()
            replacement = root / "replacement"
            replacement.mkdir()
            sentinel = replacement / "sentinel"
            sentinel.write_text("keep", encoding="utf-8")
            swapped = False

            def swap(position: str, _kind: str) -> None:
                nonlocal swapped
                if position == "create" and not swapped:
                    config_root.rename(root / "former-config")
                    replacement.rename(config_root)
                    swapped = True

            result = OpenCodeInstallService(repo, config_root, mutation_hook=swap).setup()
            self.assertFalse(result.ok)
            self.assertEqual("keep", (config_root / "sentinel").read_text(encoding="utf-8"))
            self.assertFalse((config_root / "agents").exists())

    def test_uninstall_refuses_destination_swap_without_touching_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root)
            sentinel = root / "sentinel"
            sentinel.write_text("keep", encoding="utf-8")
            swapped = False

            def swap(position: str, kind: str) -> None:
                nonlocal swapped
                if position == "remove" and kind == "agents" and not swapped:
                    (config_root / "agents").unlink()
                    os.symlink(sentinel, config_root / "agents")
                    swapped = True

            result = OpenCodeInstallService(repo, config_root, mutation_hook=swap).uninstall()
            self.assertFalse(result.ok)
            self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))
            self.assertTrue((config_root / "commands").is_symlink())

    def test_root_substitution_is_fail_closed_at_each_create_and_setup_success_position(self) -> None:
        positions = (("create", kind) for kind in ("agents", "commands"))
        for position in (*positions, ("success", "setup")):
            with self.subTest(position=position), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                config_root.mkdir()
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                swapped = False

                def hook(actual_position: str, kind: str) -> None:
                    nonlocal swapped
                    if (actual_position, kind) == position and not swapped:
                        config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                        swapped = True

                result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).setup()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_destination_substitution_is_fail_closed_at_each_create_and_setup_success_position(self) -> None:
        positions = (("create", kind) for kind in ("agents", "commands"))
        for position in (*positions, ("success", "setup")):
            with self.subTest(position=position), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                config_root.mkdir()
                sentinel = root / "unrelated-target"
                sentinel.write_bytes(b"sentinel")
                before_repo = snapshot_tree(repo)
                swapped = False

                def hook(actual_position: str, kind: str) -> None:
                    nonlocal swapped
                    if (actual_position, kind) == position and not swapped:
                        target = config_root / (kind if actual_position == "create" else "agents")
                        if target.exists() or target.is_symlink():
                            target.unlink()
                        os.symlink(sentinel, target)
                        swapped = True

                result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).setup()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(b"sentinel", sentinel.read_bytes())
                self.assertEqual(before_repo, snapshot_tree(repo))

    def test_rollback_refuses_root_and_destination_substitution_and_reports_partial_cleanup(self) -> None:
        for substitution in ("root", "destination"):
            with self.subTest(substitution=substitution), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                config_root.mkdir()
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                sentinel = root / "unrelated-target"
                sentinel.write_bytes(b"sentinel")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                real_symlink = os.symlink
                calls = 0
                swapped = False

                def hook(position: str, kind: str) -> None:
                    nonlocal swapped
                    if position != "rollback" or swapped:
                        return
                    if substitution == "root":
                        config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                    else:
                        target = config_root / kind
                        target.unlink()
                        real_symlink(sentinel, target)
                    swapped = True

                def fail_second_link(source: str, target: str, *, target_is_directory: bool, dir_fd: int) -> None:
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        raise OSError("injected create failure")
                    real_symlink(source, target, target_is_directory=target_is_directory, dir_fd=dir_fd)

                with patch("tools.opencode_install.os.symlink", side_effect=fail_second_link):
                    result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).setup()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertTrue(any("roll back" in warning for warning in result.warnings))
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(b"sentinel", sentinel.read_bytes())
                if substitution == "root":
                    self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_root_substitution_is_fail_closed_at_each_remove_and_uninstall_success_position(self) -> None:
        positions = (("remove", kind) for kind in ("agents", "commands"))
        for position in (*positions, ("success", "uninstall")):
            with self.subTest(position=position), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                create_expected_links(repo, config_root)
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                swapped = False

                def hook(actual_position: str, kind: str) -> None:
                    nonlocal swapped
                    if (actual_position, kind) == position and not swapped:
                        config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                        swapped = True

                result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).uninstall()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_destination_substitution_is_fail_closed_at_each_remove_uninstall_success_and_verify_position(self) -> None:
        positions = [*( ("remove", kind) for kind in ("agents", "commands")), ("success", "uninstall"), ("success", "verify")]
        for operation, position in (("uninstall", position) for position in positions):
            if position == ("success", "verify"):
                operation = "verify"
            with self.subTest(operation=operation, position=position), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                create_expected_links(repo, config_root)
                sentinel = root / "unrelated-target"
                sentinel.write_bytes(b"sentinel")
                before_repo = snapshot_tree(repo)
                swapped = False

                def hook(actual_position: str, kind: str) -> None:
                    nonlocal swapped
                    if (actual_position, kind) == position and not swapped:
                        target = config_root / (kind if actual_position == "remove" else "agents")
                        if target.exists() or target.is_symlink():
                            target.unlink()
                        os.symlink(sentinel, target)
                        swapped = True

                service = OpenCodeInstallService(repo, config_root, mutation_hook=hook)
                result = service.verify() if operation == "verify" else service.uninstall()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(b"sentinel", sentinel.read_bytes())

    def test_restoration_refuses_root_and_destination_substitution_and_reports_partial_restoration(self) -> None:
        for substitution in ("root", "destination"):
            with self.subTest(substitution=substitution), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                create_expected_links(repo, config_root)
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                sentinel = root / "unrelated-target"
                sentinel.write_bytes(b"sentinel")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                real_unlink = os.unlink
                calls = 0
                swapped = False

                def hook(position: str, kind: str) -> None:
                    nonlocal swapped
                    if position != "restore" or swapped:
                        return
                    if substitution == "root":
                        config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                    else:
                        os.symlink(sentinel, config_root / kind)
                    swapped = True

                def fail_second_unlink(target: str, *, dir_fd: int) -> None:
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        raise OSError("injected remove failure")
                    real_unlink(target, dir_fd=dir_fd)

                with patch("tools.opencode_install.os.unlink", side_effect=fail_second_unlink):
                    result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).uninstall()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertTrue(any("restore" in warning for warning in result.warnings))
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(b"sentinel", sentinel.read_bytes())
                if substitution == "root":
                    self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_configuration_root_rejects_mutable_ancestor_aliases_and_managed_source_containment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            unrelated = root / "unrelated-repository"
            unrelated.mkdir()
            (unrelated / "sentinel").write_bytes(b"unrelated")
            before = snapshot_tree(unrelated)
            aliased_parent = root / "alias-parent"
            os.symlink(unrelated, aliased_parent)
            for config_root in (
                aliased_parent / "opencode",
                repo / "opencode" / "nested-config",
                root / "missing-parent" / "opencode",
            ):
                with self.subTest(config_root=config_root):
                    result = OpenCodeInstallService(repo, config_root).setup()
                    self.assertFalse(result.ok)
                    self.assertEqual(before, snapshot_tree(unrelated))

    def test_root_substitution_before_creation_and_verify_success_reporting_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            parent = root / "safe-parent"
            parent.mkdir()
            config_root = parent / "opencode"
            unrelated = root / "unrelated-target"
            unrelated.mkdir()
            (unrelated / "sentinel").write_bytes(b"unrelated")
            before = snapshot_tree(unrelated)

            def create_root_alias(position: str, _kind: str) -> None:
                if position == "create-root":
                    os.symlink(unrelated, config_root)

            result = OpenCodeInstallService(repo, config_root, mutation_hook=create_root_alias).setup()
            self.assertFalse(result.ok)
            self.assertEqual(before, snapshot_tree(unrelated))

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            create_expected_links(repo, config_root)
            replacement = root / "replacement"
            replacement.mkdir()
            (replacement / "sentinel").write_bytes(b"replacement")
            before_repo = snapshot_tree(repo)
            before_replacement = snapshot_tree(replacement)

            def swap_before_verify_report(position: str, kind: str) -> None:
                if (position, kind) == ("success", "verify"):
                    config_root.rename(root / "bound-root")
                    replacement.rename(config_root)

            result = OpenCodeInstallService(repo, config_root, mutation_hook=swap_before_verify_report).verify()
            self.assertFalse(result.ok)
            self.assertEqual(before_repo, snapshot_tree(repo))
            self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_configuration_root_rejects_symlink_and_non_directory_without_touching_unrelated_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            unrelated = root / "unrelated-target"
            unrelated.mkdir()
            (unrelated / "sentinel").write_bytes(b"unrelated")
            before = snapshot_tree(unrelated)
            symlink_root = root / "symlink-root"
            os.symlink(unrelated, symlink_root)
            file_root = root / "file-root"
            file_root.write_bytes(b"not-a-directory")
            for config_root in (symlink_root, file_root):
                with self.subTest(config_root=config_root):
                    result = OpenCodeInstallService(repo, config_root).setup()
                    self.assertFalse(result.ok)
                    self.assertEqual(before, snapshot_tree(unrelated))

    def test_successful_link_creation_uses_the_bound_directory_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            config_root = root / "config"
            observed_dir_fds: list[int] = []
            real_symlink = os.symlink

            def observe(source: str, target: str, *, target_is_directory: bool, dir_fd: int) -> None:
                observed_dir_fds.append(dir_fd)
                real_symlink(source, target, target_is_directory=target_is_directory, dir_fd=dir_fd)

            with patch("tools.opencode_install.os.symlink", side_effect=observe):
                result = OpenCodeInstallService(repo, config_root).setup()

            self.assertTrue(result.ok)
            self.assertEqual(2, len(observed_dir_fds))
            self.assertTrue(all(descriptor >= 0 for descriptor in observed_dir_fds))
            self.assertEqual(
                {"agents", "commands"},
                {path.name for path in config_root.iterdir()},
            )

    def test_parent_binding_rejects_substitution_at_each_absent_root_position(self) -> None:
        for position in (
            "after-parent-validation",
            "after-parent-binding",
            "after-root-create",
            "after-root-open",
        ):
            with self.subTest(position=position), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                parent = root / "config"
                parent.mkdir()
                config_root = parent / "opencode"
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                swapped = False

                def hook(actual_position: str, _kind: str) -> None:
                    nonlocal swapped
                    if actual_position == position and not swapped:
                        parent.rename(root / "bound-parent")
                        replacement.rename(parent)
                        swapped = True

                result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).setup()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(before_replacement, snapshot_tree(parent))
                if position == "after-root-create":
                    self.assertTrue(any("cleanup was incomplete" in error for error in result.errors))

    def test_final_root_binding_rejects_existing_root_substitution_before_and_after_open(self) -> None:
        for position in ("before-root-open", "after-root-open"):
            with self.subTest(position=position), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                parent = root / "config"
                parent.mkdir()
                config_root = parent / "opencode"
                config_root.mkdir()
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                swapped = False

                def hook(actual_position: str, _kind: str) -> None:
                    nonlocal swapped
                    if actual_position == position and not swapped:
                        config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                        swapped = True

                result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).setup()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_root_binding_safely_removes_new_empty_root_after_hook_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            parent = root / "config"
            parent.mkdir()
            config_root = parent / "opencode"
            sentinel = parent / "sentinel"
            sentinel.write_bytes(b"safe-parent")

            def fail_after_create(position: str, _kind: str) -> None:
                if position == "after-root-create":
                    raise OSError("injected failure")

            bound, missing, errors = OpenCodeInstallService(
                repo,
                config_root,
                mutation_hook=fail_after_create,
            )._bind_config_root(create=True)

            self.assertIsNone(bound)
            self.assertFalse(missing)
            self.assertTrue(errors)
            self.assertFalse(config_root.exists())
            self.assertEqual(b"safe-parent", sentinel.read_bytes())

    def test_root_binding_reports_partial_cleanup_after_created_root_substitution(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            parent = root / "config"
            parent.mkdir()
            config_root = parent / "opencode"

            def replace_created_root(position: str, _kind: str) -> None:
                if position == "after-root-create":
                    config_root.rmdir()
                    config_root.mkdir()
                    (config_root / "sentinel").write_bytes(b"replacement")

            result = OpenCodeInstallService(
                repo,
                config_root,
                mutation_hook=replace_created_root,
            ).setup()

            self.assertFalse(result.ok)
            self.assertTrue(any("cleanup was incomplete" in error for error in result.errors))
            self.assertEqual(b"replacement", (config_root / "sentinel").read_bytes())

    def test_root_binding_closes_parent_descriptor_after_successful_safe_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            parent = root / "config"
            parent.mkdir()
            config_root = parent / "opencode"
            opened: list[tuple[str, int]] = []
            real_open = os.open

            def observe_open(
                path: str | os.PathLike[str],
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                descriptor = (
                    real_open(path, flags, mode, dir_fd=dir_fd)
                    if dir_fd is not None
                    else real_open(path, flags, mode)
                )
                opened.append((str(path), descriptor))
                return descriptor

            with patch("tools.opencode_install.os.open", side_effect=observe_open):
                bound, missing, errors = OpenCodeInstallService(repo, config_root)._bind_config_root(create=True)

            self.assertIsNotNone(bound)
            self.assertFalse(missing)
            self.assertEqual([], errors)
            assert bound is not None
            parent_descriptor = opened[0][1]
            os.fstat(parent_descriptor)
            OpenCodeInstallService._close_bound_root(bound)
            with self.assertRaises(OSError):
                os.fstat(parent_descriptor)

    def test_root_binding_closes_parent_and_root_descriptors_on_post_open_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = create_opencode_repo(root)
            parent = root / "config"
            parent.mkdir()
            config_root = parent / "opencode"
            opened: list[int] = []
            closed: list[int] = []
            real_open = os.open
            real_close = os.close

            def observe_open(
                path: str | os.PathLike[str],
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                descriptor = (
                    real_open(path, flags, mode, dir_fd=dir_fd)
                    if dir_fd is not None
                    else real_open(path, flags, mode)
                )
                opened.append(descriptor)
                return descriptor

            def observe_close(descriptor: int) -> None:
                closed.append(descriptor)
                real_close(descriptor)

            def fail_after_open(position: str, _kind: str) -> None:
                if position == "after-root-open":
                    raise OSError("injected failure")

            with (
                patch("tools.opencode_install.os.open", side_effect=observe_open),
                patch("tools.opencode_install.os.close", side_effect=observe_close),
            ):
                bound, _, errors = OpenCodeInstallService(
                    repo,
                    config_root,
                    mutation_hook=fail_after_open,
                )._bind_config_root(create=True)

            self.assertIsNone(bound)
            self.assertTrue(errors)
            self.assertEqual(set(opened), set(closed))
            self.assertFalse(config_root.exists())

    def test_early_setup_and_uninstall_reports_revalidate_root_and_destinations(self) -> None:
        cases = (
            ("setup", False, "expected", "root"),
            ("setup", True, "missing", "destination"),
            ("setup", True, "root-missing", "root"),
            ("uninstall", False, "missing", "root"),
            ("uninstall", True, "expected", "destination"),
            ("uninstall", False, "root-missing", "root"),
        )
        for operation, dry_run, state, substitution in cases:
            with self.subTest(operation=operation, dry_run=dry_run, state=state, substitution=substitution), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                if state == "expected":
                    create_expected_links(repo, config_root)
                elif state == "missing":
                    config_root.mkdir()
                else:
                    config_root.parent.mkdir(exist_ok=True)
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                sentinel = root / "sentinel"
                sentinel.write_bytes(b"sentinel")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                swapped = False

                def hook(position: str, kind: str) -> None:
                    nonlocal swapped
                    if (position, kind) != ("success", operation) or swapped:
                        return
                    if substitution == "root":
                        if config_root.exists() or config_root.is_symlink():
                            config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                    else:
                        if (config_root / "agents").exists() or (config_root / "agents").is_symlink():
                            (config_root / "agents").unlink()
                        os.symlink(sentinel, config_root / "agents")
                    swapped = True

                service = OpenCodeInstallService(repo, config_root, mutation_hook=hook)
                result = service.setup(dry_run=dry_run) if operation == "setup" else service.uninstall(dry_run=dry_run)

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(b"sentinel", sentinel.read_bytes())
                if substitution == "root":
                    self.assertEqual(before_replacement, snapshot_tree(config_root))

    def test_verify_visibility_rechecks_bound_root_without_following_destination_paths(self) -> None:
        for substitution in ("root", "destination"):
            with self.subTest(substitution=substitution), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                repo = create_opencode_repo(root)
                config_root = root / "config"
                create_expected_links(repo, config_root, relative=True)
                replacement = root / "replacement"
                replacement.mkdir()
                (replacement / "sentinel").write_bytes(b"replacement")
                sentinel = root / "sentinel"
                sentinel.write_bytes(b"sentinel")
                before_repo = snapshot_tree(repo)
                before_replacement = snapshot_tree(replacement)
                swapped = False

                def hook(position: str, kind: str) -> None:
                    nonlocal swapped
                    if (position, kind) != ("visibility", "verify") or swapped:
                        return
                    if substitution == "root":
                        config_root.rename(root / "bound-root")
                        replacement.rename(config_root)
                    else:
                        (config_root / "agents").unlink()
                        os.symlink(sentinel, config_root / "agents")
                    swapped = True

                result = OpenCodeInstallService(repo, config_root, mutation_hook=hook).verify()

                self.assertFalse(result.ok)
                self.assertTrue(swapped)
                self.assertEqual(before_repo, snapshot_tree(repo))
                self.assertEqual(b"sentinel", sentinel.read_bytes())
                if substitution == "root":
                    self.assertEqual(before_replacement, snapshot_tree(config_root))
