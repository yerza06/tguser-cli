"""Resolve the send target: an alias from the DB → chat_id, otherwise the value as-is."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker

from .db.repository import find_chat


def _coerce(value: str) -> str | int:
    """Convert a numeric string to int; leave the rest (``@username``, ``me``) as a string."""
    raw = value.strip()
    try:
        return int(raw)
    except ValueError:
        return raw


async def resolve_target(sm: async_sessionmaker, value: str) -> str | int:
    """If ``value`` is a saved chat name, return its chat_id; otherwise ``value`` itself.

    Kurigram ``send_*`` accepts both an int (chat id) and a string (``@username``/``me``).
    """
    chat = await find_chat(sm, value)
    target = chat.chat_id if chat is not None else value
    return _coerce(target)
