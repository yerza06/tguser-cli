"""Chat discovery commands: dialogs (list dialogs) and resolve (find an ID)."""

from __future__ import annotations

import typer
from pyrogram.errors import RPCError

from ..client import require_login, run_async
from ..config import get_settings
from ..console import console, dialogs_table, fail, info, success
from ..discover import fetch_dialogs, resolve_online
from ..i18n import t

# Negative numeric IDs must not be interpreted as options.
ALLOW_NEG = {"ignore_unknown_options": True}

app = typer.Typer()


@app.command("dialogs", help=t("discovery.dialogs_help"))
def dialogs(
    search: str | None = typer.Option(
        None, "--search", "-s", help=t("discovery.opt_search")
    ),
    limit: int = typer.Option(100, "--limit", "-n", help=t("discovery.opt_limit")),
) -> None:
    """Show your dialogs (including private chats) with their IDs."""
    settings = get_settings()
    require_login(settings)
    rows = run_async(fetch_dialogs(settings, limit=limit, search=search))
    if not rows:
        info(t("discovery.no_dialogs"))
        return
    console.print(dialogs_table(rows))


@app.command("resolve", context_settings=ALLOW_NEG, help=t("discovery.resolve_help"))
def resolve(
    query: str = typer.Argument(..., help=t("discovery.arg_query")),
) -> None:
    """Find a chat's numeric ID by @username or link."""
    settings = get_settings()
    require_login(settings)
    try:
        chat_id, title, chat_type = run_async(resolve_online(settings, query))
    except RPCError as exc:
        raise fail(str(exc), title=t("discovery.resolve_failed_title"))
    success(
        t("discovery.chat_found", title=title, type=chat_type, id=chat_id),
        title=t("discovery.chat_found_title"),
    )
