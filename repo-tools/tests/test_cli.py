"""Tests for repo_tools.cli argument parsing."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from repo_tools.cli import main


class TestCliNoArgs:
    def test_no_args_returns_2(self, capsys):
        """Calling main() with no arguments should print usage and return 2."""
        result = main([])
        assert result == 2
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower() or "repo-tools" in captured.out.lower()


class TestCliCheckSubcommand:
    def test_parse_check_verbose(self):
        """'check -v' should set command='check' and verbose=True."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.check.run", mock_run):
            result = main(["check", "-v"])

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.command == "check"
        assert args.verbose is True

    def test_parse_check_no_flags(self):
        """'check' alone should set verbose=False."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.check.run", mock_run):
            result = main(["check"])

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.command == "check"
        assert args.verbose is False


class TestCliPushSubcommand:
    def test_parse_push_dry_run_force(self):
        """'push --dry-run --force' should set both flags."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.push.run", mock_run):
            result = main(["push", "--dry-run", "--force"])

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.command == "push"
        assert args.dry_run is True
        assert args.force is True

    def test_parse_push_defaults(self):
        """'push' with no flags should have dry_run=False, force=False."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.push.run", mock_run):
            main(["push"])

        args = mock_run.call_args[0][0]
        assert args.dry_run is False
        assert args.force is False


class TestCliSyncSubcommand:
    def test_parse_sync_full(self):
        """'sync abc1234 --dry-run --no-push --force' should parse correctly."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.sync.run", mock_run):
            main(["sync", "abc1234", "--dry-run", "--no-push", "--force"])

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.command == "sync"
        assert args.commit == "abc1234"
        assert args.dry_run is True
        assert args.no_push is True
        assert args.force is True

    def test_parse_sync_defaults(self):
        """'sync' with no arguments should have sensible defaults."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.sync.run", mock_run):
            main(["sync"])

        args = mock_run.call_args[0][0]
        assert args.commit is None
        assert args.dry_run is False
        assert args.no_push is False
        assert args.force is False
        assert args.verify is False
        assert args.rebuild is False

    def test_parse_sync_verify_rebuild(self):
        """'sync --verify --rebuild' should set both flags."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.sync.run", mock_run):
            main(["sync", "--verify", "--rebuild"])

        args = mock_run.call_args[0][0]
        assert args.verify is True
        assert args.rebuild is True

    def test_parse_sync_theme_repo(self):
        """'sync --theme-repo /custom/path' should set theme_repo."""
        from pathlib import Path

        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.sync.run", mock_run):
            main(["sync", "--theme-repo", "/custom/path"])

        args = mock_run.call_args[0][0]
        assert args.theme_repo == Path("/custom/path")


class TestCliVisualizeSubcommand:
    def test_parse_visualize_with_path(self):
        """'visualize /tmp/foo' should set path='/tmp/foo'."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.visualizer.__main__.run", mock_run):
            main(["visualize", "/tmp/foo"])

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.command == "visualize"
        assert args.path == "/tmp/foo"

    def test_parse_visualize_default_path(self):
        """'visualize' with no path should default to '.'."""
        mock_run = MagicMock(return_value=0)
        with patch("repo_tools.visualizer.__main__.run", mock_run):
            main(["visualize"])

        args = mock_run.call_args[0][0]
        assert args.path == "."


class TestCliInvalidSubcommand:
    def test_unknown_subcommand_exits(self):
        """An unrecognised subcommand should cause argparse to exit with code 2."""
        with pytest.raises(SystemExit) as exc_info:
            main(["nonexistent"])
        assert exc_info.value.code == 2
