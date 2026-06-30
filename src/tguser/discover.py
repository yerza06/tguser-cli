"""Онлайн-обнаружение чатов через Kurigram: список диалогов и резолв по @username/ссылке."""

from __future__ import annotations

from pyrogram.types import Chat

from .client import build_client
from .config import Settings


def _chat_title(chat: Chat) -> str:
    """Человекочитаемое название чата: title / имя пользователя / @username."""
    if chat.title:
        return chat.title
    name = " ".join(filter(None, [chat.first_name, chat.last_name])).strip()
    if name:
        return name
    if chat.username:
        return f"@{chat.username}"
    return "—"


def _chat_type(chat: Chat) -> str:
    """Тип чата строкой (``private``/``group``/``supergroup``/``channel``/``bot``)."""
    return chat.type.name.lower() if chat.type is not None else "—"


async def resolve_online(settings: Settings, query: str) -> tuple[int, str, str]:
    """Резолв ``@username`` / t.me-ссылки / инвайт-ссылки в ``(id, title, type)``.

    Поддерживает ``@username``, ``t.me/<name>``, приватные инвайт-ссылки ``t.me/+…``
    и ссылки на сообщения ``t.me/c/<id>/<msg>``.
    """
    client = build_client(settings)
    async with client:
        chat = await client.get_chat(query)
    return chat.id, _chat_title(chat), _chat_type(chat)


async def fetch_dialogs(
    settings: Settings, limit: int, search: str | None
) -> list[dict]:
    """Список диалогов пользователя: ``[{id, title, type, username}, …]``.

    ``search`` (если задан) фильтрует по подстроке в названии или username
    (регистронезависимо).
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
