from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from tguser.commands import auth as auth_module
from tguser.config import Settings


def _settings(config_dir: str, phone_number: str | None = None) -> Settings:
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings(_env_file=None, config_dir=Path(config_dir))
    settings.api_id = 1234567
    settings.api_hash = "hash"
    settings.phone_number = phone_number
    return settings


def _client() -> MagicMock:
    client = MagicMock()
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.send_code = AsyncMock(return_value=MagicMock(phone_code_hash="code-hash"))
    client.sign_in = AsyncMock()
    client.get_me = AsyncMock(
        return_value=MagicMock(id=1, first_name="Test", username="test")
    )
    return client


class LoginPhoneNumberTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_phone_number_from_settings_skips_the_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = _settings(directory, phone_number="+15551234567")
            client = _client()

            with (
                patch.object(auth_module, "build_client", return_value=client),
                patch.object(auth_module.Prompt, "ask", return_value="12345") as ask,
            ):
                await auth_module._login(settings, None)

            client.send_code.assert_awaited_once_with("+15551234567")
            # Only the confirmation code is still asked for.
            self.assertEqual(ask.call_count, 1)

    async def test_flag_takes_precedence_over_settings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = _settings(directory, phone_number="+15551234567")
            client = _client()

            with (
                patch.object(auth_module, "build_client", return_value=client),
                patch.object(auth_module.Prompt, "ask", return_value="12345"),
            ):
                await auth_module._login(settings, "+15559876543")

            client.send_code.assert_awaited_once_with("+15559876543")
            self.assertEqual(settings.phone_number, "+15559876543")

    async def test_prompted_phone_number_is_saved_to_env(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = _settings(directory)
            client = _client()

            with (
                patch.object(auth_module, "build_client", return_value=client),
                patch.object(
                    auth_module.Prompt, "ask", side_effect=[" +15551234567 ", "12345"]
                ),
            ):
                await auth_module._login(settings, None)

            client.send_code.assert_awaited_once_with("+15551234567")
            self.assertIn(
                "TGUSER_PHONE_NUMBER=+15551234567",
                settings.env_file.read_text(encoding="utf-8"),
            )
            self.assertEqual(settings.phone_number, "+15551234567")

    async def test_unchanged_phone_number_does_not_rewrite_env(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = _settings(directory, phone_number="+15551234567")
            client = _client()

            with (
                patch.object(auth_module, "build_client", return_value=client),
                patch.object(auth_module.Prompt, "ask", return_value="12345"),
            ):
                await auth_module._login(settings, None)

            self.assertFalse(settings.env_file.exists())


if __name__ == "__main__":
    unittest.main()
