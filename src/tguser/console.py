"""Shared Rich Console and output helpers."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .i18n import t

console = Console()
err_console = Console(stderr=True)


def success(message: str, title: str | None = None) -> None:
    title = title if title is not None else t("common.done")
    console.print(Panel(message, title=f"[bold green]✓ {title}", border_style="green"))


def error(message: str, title: str | None = None) -> None:
    title = title if title is not None else t("common.error")
    err_console.print(Panel(message, title=f"[bold red]✗ {title}", border_style="red"))


def fail(message: str, title: str | None = None, code: int = 1) -> typer.Exit:
    """Print an error and return an exception to ``raise``."""
    error(message, title=title)
    return typer.Exit(code)


def info(message: str) -> None:
    console.print(message)


def chat_table(rows: list[tuple[str, str, str, str]]) -> Table:
    """Build the saved-chats table from (name, chat_id, title, created) tuples."""
    table = Table(title=t("console.chats_title"), header_style="bold cyan")
    table.add_column(t("console.col_name"), style="bold")
    table.add_column(t("console.col_chat_id"))
    table.add_column(t("console.col_title"))
    table.add_column(t("console.col_created"), style="dim")
    for name, chat_id, title, created in rows:
        table.add_row(name, chat_id, title, created)
    return table


def dialogs_table(rows: list[dict]) -> Table:
    """Build the dialogs table from (id, title, type, username) dicts."""
    table = Table(title=t("console.dialogs_title"), header_style="bold cyan")
    table.add_column(t("console.col_chat_id"), style="bold")
    table.add_column(t("console.col_title"))
    table.add_column(t("console.col_type"), style="dim")
    table.add_column(t("console.col_username"))
    for row in rows:
        table.add_row(str(row["id"]), row["title"], row["type"], row["username"])
    return table
