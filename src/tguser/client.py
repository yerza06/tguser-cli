"""Kurigram client factory and a coroutine runner helper."""

from __future__ import annotations

import asyncio
from typing import Awaitable, TypeVar

from pyrogram import Client

from .config import Settings

T = TypeVar("T")


def run_async(coro: Awaitable[T]) -> T:
    """Run a coroutine from a synchronous Typer command."""
    return asyncio.run(coro)


def build_client(settings: Settings) -> Client:
    """Create a Kurigram client. Session and workdir live in the config directory."""
    return Client(
        name=settings.session_name,
        api_id=settings.api_id,
        api_hash=settings.api_hash,
        workdir=str(settings.config_dir),
    )


def require_login(settings: Settings) -> None:
    """Ensure credentials and a session file exist, otherwise prompt to sign in."""
    from .console import fail
    from .i18n import t

    if not settings.has_credentials:
        raise fail(t("client.no_credentials"), title=t("client.no_credentials_title"))
    if not settings.session_file.exists():
        raise fail(t("client.no_session"), title=t("client.no_session_title"))
