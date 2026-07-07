"""Online chat discovery via Kurigram: listing dialogs and resolving by @username/link."""

from __future__ import annotations

from pyrogram.types import Chat

from .client import build_client
from .config import Settings


def _chat_title(chat: Chat) -> str:
    """Human-readable chat name: title / user's name / @username."""
    if chat.title:
        return chat.title
    name = " ".join(filter(None, [chat.first_name, chat.last_name])).strip()
    if name:
        return name
    if chat.username:
        return f"@{chat.username}"
    return "—"


def _chat_type(chat: Chat) -> str:
    """Chat type as a string (``private``/``group``/``supergroup``/``channel``/``bot``)."""
    return chat.type.name.lower() if chat.type is not None else "—"


async def resolve_online(settings: Settings, query: str) -> tuple[int, str, str]:
    """Resolve a ``@username`` / t.me link / invite link into ``(id, title, type)``.

    Supports ``@username``, ``t.me/<name>``, private invite links ``t.me/+…``,
    and message links ``t.me/c/<id>/<msg>``.
    """
    client = build_client(settings)
    async with client:
        chat = await client.get_chat(query)
    return chat.id, _chat_title(chat), _chat_type(chat)


async def fetch_dialogs(
    settings: Settings, limit: int, search: str | None
) -> list[dict]:
    """The user's dialogs: ``[{id, title, type, username}, …]``.

    ``search`` (if given) filters by substring in the title or username
    (case-insensitive).
    """
    needle = search.lower() if search else None
    out: list[dict] = []
    client = build_client(settings)
    async with client:
        async for dialog in client.get_dialogs(limit=limit):
            chat = dialog.chat
            title = _chat_title(chat)
            username = chat.username or ""
            if needle and needle not in f"{title} {username}".lower():
                continue
            out.append(
                {
                    "id": chat.id,
                    "title": title,
                    "type": _chat_type(chat),
                    "username": f"@{username}" if username else "—",
                }
            )
    return out
