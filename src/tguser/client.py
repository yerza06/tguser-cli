"""Фабрика клиента Kurigram и хелпер запуска корутин."""

from __future__ import annotations

import asyncio
from typing import Awaitable, TypeVar

from pyrogram import Client

from .config import Settings

T = TypeVar("T")


def run_async(coro: Awaitable[T]) -> T:
    """Выполнить корутину из синхронной команды Typer."""
    return asyncio.run(coro)


def build_client(settings: Settings) -> Client:
    """Создать клиент Kurigram. Сессия и workdir — в каталоге конфигурации."""
    return Client(
        name=settings.session_name,
        api_id=settings.api_id,
        api_hash=settings.api_hash,
        workdir=str(settings.config_dir),
    )


def require_login(settings: Settings) -> None:
    """Проверить, что есть учётные данные и файл сессии, иначе подсказать вход."""
    from .console import fail

    if not settings.has_credentials:
        raise fail(
            "Не заданы api_id/api_hash. Выполните: [bold]tguser login[/bold]",
            title="Нет учётных данных",
        )
    if not settings.session_file.exists():
        raise fail(
            "Сессия не найдена. Сначала войдите: [bold]tguser login[/bold]",
            title="Нет сессии",
        )
