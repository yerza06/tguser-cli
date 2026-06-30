"""Резолв цели отправки: alias из БД → chat_id, иначе значение как есть."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker

from .db.repository import find_chat


def _coerce(value: str) -> str | int:
    """Числовую строку привести к int, остальное (``@username``, ``me``) оставить строкой."""
    raw = value.strip()
    try:
        return int(raw)
    except ValueError:
        return raw


async def resolve_target(sm: async_sessionmaker, value: str) -> str | int:
    """Если ``value`` — имя сохранённого чата, вернуть его chat_id; иначе сам ``value``.

    Kurigram ``send_*`` принимают и int (chat id), и строку (``@username``/``me``).
    """
    chat = await find_chat(sm, value)
    target = chat.chat_id if chat is not None else value
    return _coerce(target)
