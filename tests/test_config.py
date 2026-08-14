from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tguser.config import Settings, save_credentials, save_phone_number


def _settings(config_dir: str) -> Settings:
    # _env_file=None keeps the tests away from the real ~/.config/tguser/.env.
    return Settings(_env_file=None, config_dir=Path(config_dir))


def _read_env(settings: Settings) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in settings.env_file.read_text(encoding="utf-8").splitlines():
        key, _, val = raw.partition("=")
        values[key] = val
    return values


class PhoneNumberSettingTestCase(unittest.TestCase):
    def test_phone_number_is_read_from_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"TGUSER_PHONE_NUMBER": "+15551234567"}):
                settings = _settings(directory)

            self.assertEqual(settings.phone_number, "+15551234567")

    def test_phone_number_defaults_to_none(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True):
                settings = _settings(directory)

            self.assertIsNone(settings.phone_number)

    def test_credentials_do_not_require_a_phone_number(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True):
                settings = _settings(directory)
            settings.api_id = 1234567
            settings.api_hash = "hash"

            self.assertTrue(settings.has_credentials)


class SaveCredentialsTestCase(unittest.TestCase):
    def test_save_phone_number_creates_a_private_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True):
                settings = _settings(directory)
            save_phone_number(settings, "+15551234567")

            self.assertEqual(
                _read_env(settings), {"TGUSER_PHONE_NUMBER": "+15551234567"}
            )
            self.assertEqual(settings.env_file.stat().st_mode & 0o777, 0o600)
            self.assertEqual(settings.phone_number, "+15551234567")

    def test_save_phone_number_keeps_existing_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True):
                settings = _settings(directory)
            save_credentials(settings, 1234567, "hash")
            save_phone_number(settings, "+15551234567")

            self.assertEqual(
                _read_env(settings),
                {
                    "TGUSER_API_ID": "1234567",
                    "TGUSER_API_HASH": "hash",
                    "TGUSER_PHONE_NUMBER": "+15551234567",
                },
            )

    def test_save_credentials_keeps_an_existing_phone_number(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True):
                settings = _settings(directory)
            save_phone_number(settings, "+15551234567")
            save_credentials(settings, 1234567, "hash")

            self.assertEqual(
                _read_env(settings),
                {
                    "TGUSER_PHONE_NUMBER": "+15551234567",
                    "TGUSER_API_ID": "1234567",
                    "TGUSER_API_HASH": "hash",
                },
            )
            self.assertEqual(settings.api_id, 1234567)
            self.assertEqual(settings.api_hash, "hash")


if __name__ == "__main__":
    unittest.main()
