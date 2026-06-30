"""Управление именованными идентификаторами чатов (по аналогии с ``git remote``)."""

from __future__ import annotations

import typer

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

app = typer.Typer(help="Управление сохранёнными чатами (alias → ID).")

# Telegram ID групп/каналов отрицательные (-100…). Без этого Click принимает их
# за неизвестные опции; флаг отключает такую интерпретацию для позиционных аргументов.
ALLOW_NEG = {"ignore_unknown_options": True}


async def _sessionmaker():
    settings = get_settings()
    return await init_db(settings.db_path)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Без подкоманды — показать список сохранённых чатов."""
    if ctx.invoked_subcommand is None:
        _list()


@app.command("add", context_settings=ALLOW_NEG)
def add(
    name: str = typer.Argument(..., help="Имя (alias) чата"),
    chat_id: str = typer.Argument(..., help="ID чата / @username"),
) -> None:
    """Добавить новый alias чата."""

    async def _run():
        sm = await _sessionmaker()
        return await add_chat(sm, name, chat_id)

    try:
        chat = run_async(_run())
    except ChatExistsError:
        raise fail(f"Чат с именем [bold]{name}[/bold] уже существует.")
    success(f"Добавлен чат [bold]{chat.name}[/bold] → {chat.chat_id}")


def _list() -> None:
    async def _run():
        sm = await _sessionmaker()
        return await list_chats(sm)

    chats = run_async(_run())
    if not chats:
        info("[dim]Список чатов пуст. Добавьте: tguser chat add <name> <id>[/dim]")
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


@app.command("list")
def list_cmd() -> None:
    """Показать все сохранённые чаты."""
    _list()


@app.command("remove")
def remove(name: str = typer.Argument(..., help="Имя чата")) -> None:
    """Удалить alias чата."""

    async def _run():
        sm = await _sessionmaker()
        await remove_chat(sm, name)

    try:
        run_async(_run())
    except ChatNotFoundError:
        raise fail(f"Чат [bold]{name}[/bold] не найден.")
    success(f"Чат [bold]{name}[/bold] удалён.")


@app.command("get-id")
def get_id(name: str = typer.Argument(..., help="Имя чата")) -> None:
    """Вывести ID сохранённого чата."""

    async def _run():
        sm = await _sessionmaker()
        return await get_chat(sm, name)

    try:
        chat = run_async(_run())
    except ChatNotFoundError:
        raise fail(f"Чат [bold]{name}[/bold] не найден.")
    console.print(chat.chat_id)


@app.command("replace-id", context_settings=ALLOW_NEG)
def replace_id(
    name: str = typer.Argument(..., help="Имя чата"),
    new_id: str = typer.Argument(..., help="Новый ID чата"),
) -> None:
    """Заменить ID у сохранённого чата."""

    async def _run():
        sm = await _sessionmaker()
        return await replace_chat_id(sm, name, new_id)

    try:
        chat = run_async(_run())
    except ChatNotFoundError:
        raise fail(f"Чат [bold]{name}[/bold] не найден.")
    success(f"ID чата [bold]{chat.name}[/bold] изменён на {chat.chat_id}")


@app.command("rename")
def rename(
    old_name: str = typer.Argument(..., help="Текущее имя"),
    new_name: str = typer.Argument(..., help="Новое имя"),
) -> None:
    """Переименовать alias чата."""

    async def _run():
        sm = await _sessionmaker()
        return await rename_chat(sm, old_name, new_name)

    try:
        chat = run_async(_run())
    except ChatNotFoundError:
        raise fail(f"Чат [bold]{old_name}[/bold] не найден.")
    except ChatExistsError:
        raise fail(f"Чат с именем [bold]{new_name}[/bold] уже существует.")
    success(f"Чат переименован: [bold]{old_name}[/bold] → [bold]{chat.name}[/bold]")
