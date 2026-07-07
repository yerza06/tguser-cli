"""CRUD operations on named chats.

Each function takes a session factory (from :func:`tguser.db.database.init_db`)
and opens its own short-lived transaction.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from .models import Chat


class ChatExistsError(Exception):
    """A chat with this name already exists."""


class ChatNotFoundError(Exception):
    """A chat with this name was not found."""


async def add_chat(
    sm: async_sessionmaker, name: str, chat_id: str, title: str | None = None
) -> Chat:
    async with sm() as session:
        existing = await session.scalar(select(Chat).where(Chat.name == name))
        if existing is not None:
            raise ChatExistsError(name)
        chat = Chat(name=name, chat_id=chat_id, title=title)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        return chat


async def list_chats(sm: async_sessionmaker) -> list[Chat]:
    async with sm() as session:
        result = await session.scalars(select(Chat).order_by(Chat.name))
        return list(result)


async def get_chat(sm: async_sessionmaker, name: str) -> Chat:
    async with sm() as session:
        chat = await session.scalar(select(Chat).where(Chat.name == name))
        if chat is None:
            raise ChatNotFoundError(name)
        return chat


async def find_chat(sm: async_sessionmaker, name: str) -> Chat | None:
    """Return the chat by name, or ``None`` (without raising)."""
    async with sm() as session:
        return await session.scalar(select(Chat).where(Chat.name == name))


async def remove_chat(sm: async_sessionmaker, name: str) -> None:
    async with sm() as session:
        chat = await session.scalar(select(Chat).where(Chat.name == name))
        if chat is None:
            raise ChatNotFoundError(name)
        await session.delete(chat)
        await session.commit()


async def rename_chat(sm: async_sessionmaker, old_name: str, new_name: str) -> Chat:
    async with sm() as session:
        chat = await session.scalar(select(Chat).where(Chat.name == old_name))
        if chat is None:
            raise ChatNotFoundError(old_name)
        clash = await session.scalar(select(Chat).where(Chat.name == new_name))
        if clash is not None:
            raise ChatExistsError(new_name)
        chat.name = new_name
        await session.commit()
        await session.refresh(chat)
        return chat


async def replace_chat_id(sm: async_sessionmaker, name: str, new_id: str) -> Chat:
    async with sm() as session:
        chat = await session.scalar(select(Chat).where(Chat.name == name))
        if chat is None:
            raise ChatNotFoundError(name)
        chat.chat_id = new_id
        await session.commit()
        await session.refresh(chat)
        return chat
