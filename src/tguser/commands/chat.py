"""Named chat identifier management (similar to ``git remote``)."""

from __future__ import annotations

import typer
from pyrogram.errors import RPCError

from ..client import run_async
from ..config import get_settings
from ..console import chat_table, console, fail, info, success
from ..db.database import init_db
from ..db.repository import (
    ChatExistsError,
    ChatNotFoundError,
    add_chat,
    get_chat,
    list_chats,
    remove_chat,
    rename_chat,
    replace_chat_id,
)
from ..discover import resolve_online
from ..i18n import t

app = typer.Typer(help=t("chat.help"))

# Telegram group/channel IDs are negative (-100…). Without this, Click treats them
# as unknown options; the flag disables that interpretation for positional arguments.
ALLOW_NEG = {"ignore_unknown_options": True}


async def _sessionmaker():
    settings = get_settings()
    return await init_db(settings.db_path)


def _needs_resolution(value: str) -> bool:
    """``True`` for ``@username``/links — values worth resolving to a numeric ID.

    Numeric IDs and ``me`` are stored as-is.
    """
    raw = value.strip()
    if raw == "me":
        return False
    try:
        int(raw)
    except ValueError:
        return True
    return False


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Without a subcommand — show the list of saved chats."""
    if ctx.invoked_subcommand is None:
        _list()


@app.command("add", context_settings=ALLOW_NEG, help=t("chat.add_help"))
def add(
    name: str = typer.Argument(..., help=t("chat.arg_name")),
    chat_id: str = typer.Argument(..., help=t("chat.arg_chat_id")),
    no_resolve: bool = typer.Option(
        False, "--no-resolve", help=t("chat.opt_no_resolve")
    ),
) -> None:
    """Add a new chat alias.

    If a ``@username`` or link is given and a session is active, the numeric ID and
    title are resolved automatically. ``--no-resolve`` stores the value as-is.
    """
    settings = get_settings()
    stored_id = chat_id
    title: str | None = None

    if not no_resolve and _needs_resolution(chat_id):
        if settings.has_credentials and settings.session_file.exists():
            try:
                resolved_id, title, _ = run_async(resolve_online(settings, chat_id))
                stored_id = str(resolved_id)
            except RPCError as exc:
                info(t("chat.resolve_failed", error=exc, value=chat_id))
                title = None
        else:
            info(t("chat.no_session_resolve"))

    async def _run():
        sm = await _sessionmaker()
        return await add_chat(sm, name, stored_id, title)

    try:
        chat = run_async(_run())
    except ChatExistsError:
        raise fail(t("chat.exists", name=name))
    suffix = f" ([dim]{chat.title}[/dim])" if chat.title else ""
    success(t("chat.added", name=chat.name, id=chat.chat_id, suffix=suffix))


def _list() -> None:
    async def _run():
        sm = await _sessionmaker()
        return await list_chats(sm)

    chats = run_async(_run())
    if not chats:
        info(t("chat.list_empty"))
        return
    rows = [
        (
            c.name,
            c.chat_id,
            c.title or "—",
            c.created_at.strftime("%Y-%m-%d %H:%M"),
        )
        for c in chats
    ]
    console.print(chat_table(rows))


@app.command("list", help=t("chat.list_help"))
def list_cmd() -> None:
    """Show all saved chats."""
    _list()


@app.command("remove", help=t("chat.remove_help"))
def remove(name: str = typer.Argument(..., help=t("chat.arg_name_simple"))) -> None:
    """Remove a chat alias."""

    async def _run():
        sm = await _sessionmaker()
        await remove_chat(sm, name)

    try:
        run_async(_run())
    except ChatNotFoundError:
        raise fail(t("chat.not_found", name=name))
    success(t("chat.removed", name=name))


@app.command("get-id", help=t("chat.get_id_help"))
def get_id(name: str = typer.Argument(..., help=t("chat.arg_name_simple"))) -> None:
    """Print the ID of a saved chat."""

    async def _run():
        sm = await _sessionmaker()
        return await get_chat(sm, name)

    try:
        chat = run_async(_run())
    except ChatNotFoundError:
        raise fail(t("chat.not_found", name=name))
    console.print(chat.chat_id)


@app.command("replace-id", context_settings=ALLOW_NEG, help=t("chat.replace_id_help"))
def replace_id(
    name: str = typer.Argument(..., help=t("chat.arg_name_simple")),
    new_id: str = typer.Argument(..., help=t("chat.arg_new_id")),
) -> None:
    """Replace the ID of a saved chat."""

    async def _run():
        sm = await _sessionmaker()
        return await replace_chat_id(sm, name, new_id)

    try:
        chat = run_async(_run())
    except ChatNotFoundError:
        raise fail(t("chat.not_found", name=name))
    success(t("chat.id_replaced", name=chat.name, id=chat.chat_id))


@app.command("rename", help=t("chat.rename_help"))
def rename(
    old_name: str = typer.Argument(..., help=t("chat.arg_old_name")),
    new_name: str = typer.Argument(..., help=t("chat.arg_new_name")),
) -> None:
    """Rename a chat alias."""

    async def _run():
        sm = await _sessionmaker()
        return await rename_chat(sm, old_name, new_name)

    try:
        chat = run_async(_run())
    except ChatNotFoundError:
        raise fail(t("chat.not_found", name=old_name))
    except ChatExistsError:
        raise fail(t("chat.exists", name=new_name))
    success(t("chat.renamed", old=old_name, new=chat.name))
