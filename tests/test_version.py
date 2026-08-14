from __future__ import annotations

import platform
import unittest

from typer.testing import CliRunner

from tguser import __version__
from tguser.cli import app


class VersionCommandTestCase(unittest.TestCase):
    """Assert on language-independent values only: the panel labels are localized
    and Rich draws a border that may wrap long values."""

    def test_version_command_reports_version_and_environment(self) -> None:
        result = CliRunner().invoke(app, ["version"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn(__version__, result.output)
        self.assertIn(platform.python_version(), result.output)

    def test_version_flag_prints_a_single_line(self) -> None:
        result = CliRunner().invoke(app, ["--version"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), f"tguser {__version__}")

    def test_command_and_flag_agree(self) -> None:
        runner = CliRunner()

        command = runner.invoke(app, ["version"])
        flag = runner.invoke(app, ["--version"])

        self.assertIn(__version__, command.output)
        self.assertIn(__version__, flag.output)

    def test_version_is_listed_in_help(self) -> None:
        result = CliRunner().invoke(app, ["--help"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("version", result.output)


if __name__ == "__main__":
    unittest.main()
