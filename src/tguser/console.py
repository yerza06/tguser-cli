"""Общий Rich Console и хелперы вывода."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
err_console = Console(stderr=True)


def success(message: str, title: str = "Готово") -> None:
    console.print(Panel(message, title=f"[bold green]✓ {title}", border_style="green"))


def error(message: str, title: str = "Ошибка") -> None:
    err_console.print(Panel(message, title=f"[bold red]✗ {title}", border_style="red"))


def fail(message: str, title: str = "Ошибка", code: int = 1) -> typer.Exit:
    """Вывести ошибку и вернуть исключение для ``raise``."""
    error(message, title=title)
    return typer.Exit(code)


def info(message: str) -> None:
    console.print(message)


def chat_table(rows: list[tuple[str, str, str, str]]) -> Table:
    """Собрать таблицу списка чатов из кортежей (name, chat_id, title, created)."""
    table = Table(title="Сохранённые чаты", header_style="bold cyan")
    table.add_column("Имя", style="bold")
    table.add_column("ID чата")
    table.add_column("Название")
    table.add_column("Создан", style="dim")
    for name, chat_id, title, created in rows:
        table.add_row(name, chat_id, title, created)
    return table


def dialogs_table(rows: list[dict]) -> Table:
    """Собрать таблицу диалогов из словарей (id, title, type, username)."""
    table = Table(title="Диалоги", header_style="bold cyan")
    table.add_column("ID чата", style="bold")
    table.add_column("Название")
    table.add_column("Тип", style="dim")
    table.add_column("@username")
    for row in rows:
        table.add_row(str(row["id"]), row["title"], row["type"], row["username"])
    return table
