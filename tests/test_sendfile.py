from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from typer.testing import CliRunner

from tguser.cli import app
from tguser.commands import send as send_module


class SendfileTestCase(unittest.IsolatedAsyncioTestCase):
    async def _run_sendfile(
        self,
        file_count: int,
        *,
        group: bool,
        caption: str | None = "Caption",
    ) -> MagicMock:
        with tempfile.TemporaryDirectory() as directory:
            files = []
            for index in range(file_count):
                path = Path(directory) / f"file-{index}.txt"
                path.touch()
                files.append(str(path))

            with patch.object(send_module, "_dispatch") as dispatch:
                send_module.sendfile(files, "me", caption, group)

            target, sender = dispatch.call_args.args
            self.assertEqual(target, "me")

            client = MagicMock()
            client.send_document = AsyncMock()
            client.send_media_group = AsyncMock()
            await sender(client, 123)
            return client

    async def test_default_sends_documents_separately(self) -> None:
        client = await self._run_sendfile(3, group=False)

        self.assertEqual(client.send_document.await_count, 3)
        client.send_media_group.assert_not_awaited()
        self.assertEqual(
            [call.kwargs["caption"] for call in client.send_document.await_args_list],
            ["Caption", None, None],
        )

    async def test_group_with_one_file_sends_regular_document(self) -> None:
        client = await self._run_sendfile(1, group=True)

        client.send_document.assert_awaited_once()
        self.assertEqual(
            client.send_document.await_args.kwargs["caption"], "Caption"
        )
        client.send_media_group.assert_not_awaited()

    async def test_group_sends_two_to_ten_documents_as_album(self) -> None:
        client = await self._run_sendfile(3, group=True)

        client.send_document.assert_not_awaited()
        client.send_media_group.assert_awaited_once()
        media = client.send_media_group.await_args.args[1]
        self.assertEqual(len(media), 3)
        self.assertTrue(
            all(isinstance(item, send_module.InputMediaDocument) for item in media)
        )
        self.assertEqual([item.caption for item in media], ["Caption", None, None])

    async def test_group_splits_eleven_files_into_album_and_document(self) -> None:
        client = await self._run_sendfile(11, group=True)

        client.send_media_group.assert_awaited_once()
        self.assertEqual(len(client.send_media_group.await_args.args[1]), 10)
        client.send_document.assert_awaited_once()
        self.assertNotIn("caption", client.send_document.await_args.kwargs)

    async def test_group_splits_large_batches_and_sends_single_remainder(self) -> None:
        client = await self._run_sendfile(21, group=True)

        self.assertEqual(client.send_media_group.await_count, 2)
        self.assertEqual(
            [
                len(call.args[1])
                for call in client.send_media_group.await_args_list
            ],
            [10, 10],
        )
        first_group = client.send_media_group.await_args_list[0].args[1]
        second_group = client.send_media_group.await_args_list[1].args[1]
        self.assertEqual(
            [item.caption for item in first_group],
            ["Caption", *([None] * 9)],
        )
        self.assertTrue(all(item.caption is None for item in second_group))
        client.send_document.assert_awaited_once()
        self.assertNotIn("caption", client.send_document.await_args.kwargs)


class SendfileHelpTestCase(unittest.TestCase):
    def test_group_flags_are_shown_in_help(self) -> None:
        result = CliRunner().invoke(app, ["sendfile", "--help"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("--group", result.output)
        self.assertIn("-G", result.output)


if __name__ == "__main__":
    unittest.main()
