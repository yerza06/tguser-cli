"""Команды обнаружения чатов: dialogs (список диалогов) и resolve (узнать ID)."""

from __future__ import annotations

import typer
from pyrogram.errors import RPCError

from ..client import require_login, run_async
from ..config import get_settings
from ..console import console, dialogs_table, fail, info, success
from ..discover import fetch_dialogs, resolve_online

# Отрицательные числовые ID не должны интерпретироваться как опции.
ALLOW_NEG = {"ignore_unknown_options": True}

app = typer.Typer()


@app.command("dialogs")
def dialogs(
    search: str | None = typer.Option(
        None, "--search", "-s", help="Фильтр по названию или @username"
    ),
    limit: int = typer.Option(100, "--limit", "-n", help="Сколько диалогов запросить"),
) -> None:
    """Показать ваши диалоги (включая закрытые чаты) с их ID."""
    settings = get_settings()
    require_login(settings)
    rows = run_async(fetch_dialogs(settings, limit=limit, search=search))
    if not rows:
        info("[dim]Диалоги не найдены.[/dim]")
        return
    console.print(dialogs_table(rows))


@app.command("resolve", context_settings=ALLOW_NEG)
def resolve(
    query: str = typer.Argument(
        ..., help="@username, t.me-ссылка или инвайт-ссылка t.me/+…"
    ),
) -> None:
    """Узнать числовой ID чата по @username или ссылке."""
    settings = get_settings()
    require_login(settings)
    try:
        chat_id, title, chat_type = run_async(resolve_online(settings, query))
    except RPCError as exc:
        raise fail(str(exc), title="Не удалось определить чат")
    success(
        f"[bold]{title}[/bold] ({chat_type})\nID: [bold]{chat_id}[/bold]",
        title="Чат найден",
    )
