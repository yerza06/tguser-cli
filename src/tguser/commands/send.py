"""Sending commands: text, files, photo, audio, video, voice, video note, sticker, contact.

All media commands accept two syntaxes:

* via flags:   ``tguser sendphoto a.png b.png --to chat --caption "text"``
* positional:  ``tguser sendphoto a.png b.png chat "text"``

The boundary between files and (target, caption) is determined as follows: leading
positional arguments that exist as files on disk are treated as content; the first
remaining token is the target (unless ``--to`` is set), the second is the caption
(unless ``--caption`` is set).
"""

from __future__ import annotations

from pathlib import Path

import typer
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from ..client import build_client, require_login, run_async
from ..config import Settings, get_settings
from ..console import console, fail, success
from ..db.database import init_db
from ..i18n import t
from ..resolver import resolve_target

app = typer.Typer(help=t("send.help"))

# The target may be a negative channel/group ID (-100…); allow such tokens as
# positional arguments / option values instead of treating them as options.
ALLOW_NEG = {"ignore_unknown_options": True}


# --------------------------------------------------------------------------- #
# Positional argument parsing
# --------------------------------------------------------------------------- #
def _split_media_args(
    items: list[str], to: str | None, caption: str | None
) -> tuple[list[str], str, str | None]:
    """Split positional arguments into (files, target, caption).

    Leading file-tokens → content; the next → target (unless ``--to``);
    the next → caption (unless ``--caption``).
    """
    files: list[str] = []
    for token in items:
        if Path(token).expanduser().exists():
            files.append(token)
        else:
            break
    rest = items[len(files) :]

    if to is None and rest:
        to = rest.pop(0)
    if caption is None and rest:
        caption = rest.pop(0)

    if not files:
        raise fail(t("send.no_files"), title=t("send.no_files_title"))
    if rest:
        raise fail(
            t("common.extra_args", args=" ".join(rest)),
            title=t("common.invalid_args"),
        )
    if to is None:
        raise fail(t("common.no_target"))
    return files, to, caption


def _pick_target_caption(
    rest: list[str], to: str | None, caption: str | None
) -> tuple[str, str | None]:
    """For file-less commands: take target/caption from ``--to``/``--caption`` or the tail."""
    rest = list(rest)
    if to is None and rest:
        to = rest.pop(0)
    if caption is None and rest:
        caption = rest.pop(0)
    if rest:
        raise fail(
            t("common.extra_args", args=" ".join(rest)),
            title=t("common.invalid_args"),
        )
    if to is None:
        raise fail(t("common.no_target"))
    return to, caption


def _validate_files(files: list[str]) -> list[str]:
    resolved = []
    for f in files:
        p = Path(f).expanduser()
        if not p.exists():
            raise fail(t("send.file_not_found", file=f), title=t("send.no_file_title"))
        resolved.append(str(p))
    return resolved


# --------------------------------------------------------------------------- #
# Shared send runner
# --------------------------------------------------------------------------- #
async def _run_send(settings: Settings, target_value: str, sender) -> str | int:
    """Resolve the target, open the client and call ``sender(client, target)``."""
    sm = await init_db(settings.db_path)
    target = await resolve_target(sm, target_value)
    client = build_client(settings)
    async with client:
        with console.status(t("send.sending"), spinner="dots"):
            await sender(client, target)
    return target


def _dispatch(target_value: str, sender) -> None:
    settings = get_settings()
    require_login(settings)
    target = run_async(_run_send(settings, target_value, sender))
    success(t("send.sent", target=target))


# --------------------------------------------------------------------------- #
# Text
# --------------------------------------------------------------------------- #
@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_send"))
def send(
    message: str = typer.Argument(..., help=t("send.arg_message")),
    rest: list[str] | None = typer.Argument(None, help=t("send.arg_rest")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to_full")),
    caption: str | None = typer.Option(None, "--caption", help=t("send.opt_caption_text")),
) -> None:
    """Send a text message."""
    target, cap = _pick_target_caption(rest or [], to, caption)
    text = message if not cap else f"{message}\n\n{cap}"

    async def sender(client, tgt):
        await client.send_message(tgt, text)

    _dispatch(target, sender)


# --------------------------------------------------------------------------- #
# Media from files
# --------------------------------------------------------------------------- #
@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendfile"))
def sendfile(
    items: list[str] = typer.Argument(..., help=t("send.arg_files")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
    caption: str | None = typer.Option(None, "--caption", help=t("send.opt_caption")),
) -> None:
    """Send file(s) as a document."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        for index, path in enumerate(files):
            await client.send_document(tgt, path, caption=cap if index == 0 else None)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendphoto"))
def sendphoto(
    items: list[str] = typer.Argument(..., help=t("send.arg_photos")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
    caption: str | None = typer.Option(None, "--caption", help=t("send.opt_caption")),
) -> None:
    """Send a photo (multiple → album)."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        if len(files) == 1:
            await client.send_photo(tgt, files[0], caption=cap)
        else:
            media = [
                InputMediaPhoto(path, caption=cap if i == 0 else None)
                for i, path in enumerate(files)
            ]
            await client.send_media_group(tgt, media)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendvideo"))
def sendvideo(
    items: list[str] = typer.Argument(..., help=t("send.arg_videos")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
    caption: str | None = typer.Option(None, "--caption", help=t("send.opt_caption")),
) -> None:
    """Send a video (multiple → album)."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        if len(files) == 1:
            await client.send_video(tgt, files[0], caption=cap)
        else:
            media = [
                InputMediaVideo(path, caption=cap if i == 0 else None)
                for i, path in enumerate(files)
            ]
            await client.send_media_group(tgt, media)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendaudio"))
def sendaudio(
    items: list[str] = typer.Argument(..., help=t("send.arg_audio")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
    caption: str | None = typer.Option(None, "--caption", help=t("send.opt_caption")),
) -> None:
    """Send audio / music."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        for index, path in enumerate(files):
            await client.send_audio(tgt, path, caption=cap if index == 0 else None)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendvoice"))
def sendvoice(
    items: list[str] = typer.Argument(..., help=t("send.arg_voice")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
    caption: str | None = typer.Option(None, "--caption", help=t("send.opt_caption")),
) -> None:
    """Send a voice message."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        await client.send_voice(tgt, files[0], caption=cap)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendvideonote"))
def sendvideonote(
    items: list[str] = typer.Argument(..., help=t("send.arg_note")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
) -> None:
    """Send a video note."""
    files, target, _ = _split_media_args(items, to, None)
    files = _validate_files(files)

    async def sender(client, tgt):
        await client.send_video_note(tgt, files[0])

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendsticker"))
def sendsticker(
    items: list[str] = typer.Argument(..., help=t("send.arg_sticker")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
) -> None:
    """Send a sticker."""
    files, target, _ = _split_media_args(items, to, None)
    files = _validate_files(files)

    async def sender(client, tgt):
        await client.send_sticker(tgt, files[0])

    _dispatch(target, sender)


# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #
@app.command(context_settings=ALLOW_NEG, help=t("send.cmd_sendcontact"))
def sendcontact(
    args: list[str] | None = typer.Argument(None, help=t("send.arg_contact")),
    phone: str | None = typer.Option(None, "--phone", help=t("send.opt_phone")),
    first_name: str | None = typer.Option(None, "--first-name", help=t("send.opt_first")),
    last_name: str | None = typer.Option(None, "--last-name", help=t("send.opt_last")),
    to: str | None = typer.Option(None, "--to", help=t("send.opt_to")),
) -> None:
    """Send a contact."""
    args = list(args or [])

    # Positional parsing only applies when the matching flags are not set.
    if phone is None and args:
        phone = args.pop(0)
    if first_name is None and args:
        first_name = args.pop(0)
    # If 2 tokens remain — they are [last_name, target]; if 1 — it is the target.
    if len(args) >= 2 and last_name is None:
        last_name = args.pop(0)
    if to is None and args:
        to = args.pop(0)

    if args:
        raise fail(
            t("common.extra_args", args=" ".join(args)),
            title=t("common.invalid_args"),
        )
    if not phone or not first_name:
        raise fail(t("send.contact_need_fields"))
    if to is None:
        raise fail(t("common.no_target"))

    async def sender(client, tgt):
        await client.send_contact(
            tgt, phone_number=phone, first_name=first_name, last_name=last_name
        )

    _dispatch(to, sender)
