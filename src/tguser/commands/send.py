"""Команды отправки: текст, файлы, фото, аудио, видео, голосовое, кружок, стикер, контакт.

Все медиа-команды поддерживают два синтаксиса:

* через флаги:   ``tguser sendphoto a.png b.png --to chat --caption "текст"``
* позиционно:    ``tguser sendphoto a.png b.png chat "текст"``

Граница между файлами и (целью, подписью) определяется так: ведущие позиционные
аргументы, существующие как файлы на диске, считаются контентом; первый оставшийся
токен — это цель (если не задан ``--to``), второй — подпись (если не задан ``--caption``).
"""

from __future__ import annotations

from pathlib import Path

import typer
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from ..client import build_client, require_login, run_async
from ..config import Settings, get_settings
from ..console import console, fail, success
from ..db.database import init_db
from ..resolver import resolve_target

app = typer.Typer(help="Отправка сообщений и медиа.")

# Цель может быть отрицательным ID канала/группы (-100…); разрешаем такие токены
# как позиционные аргументы / значения опций, а не трактуем их как опции.
ALLOW_NEG = {"ignore_unknown_options": True}


# --------------------------------------------------------------------------- #
# Разбор позиционных аргументов
# --------------------------------------------------------------------------- #
def _split_media_args(
    items: list[str], to: str | None, caption: str | None
) -> tuple[list[str], str, str | None]:
    """Разделить позиционные аргументы на (файлы, цель, подпись).

    Ведущие токены-файлы → контент; следующий → цель (если нет ``--to``);
    следующий → подпись (если нет ``--caption``).
    """
    files: list[str] = []
    for token in items:
        if Path(token).expanduser().exists():
            files.append(token)
        else:
            break
    rest = items[len(files) :]

    if to is None and rest:
        to = rest.pop(0)
    if caption is None and rest:
        caption = rest.pop(0)

    if not files:
        raise fail(
            "Не найдено ни одного существующего файла. Проверьте пути.",
            title="Нет файлов",
        )
    if rest:
        raise fail(
            f"Лишние аргументы: {' '.join(rest)}", title="Неверные аргументы"
        )
    if to is None:
        raise fail("Не указана цель. Используйте --to или позиционный аргумент.")
    return files, to, caption


def _pick_target_caption(
    rest: list[str], to: str | None, caption: str | None
) -> tuple[str, str | None]:
    """Для команд без файлов: взять цель/подпись из ``--to``/``--caption`` или хвоста."""
    rest = list(rest)
    if to is None and rest:
        to = rest.pop(0)
    if caption is None and rest:
        caption = rest.pop(0)
    if rest:
        raise fail(f"Лишние аргументы: {' '.join(rest)}", title="Неверные аргументы")
    if to is None:
        raise fail("Не указана цель. Используйте --to или позиционный аргумент.")
    return to, caption


def _validate_files(files: list[str]) -> list[str]:
    resolved = []
    for f in files:
        p = Path(f).expanduser()
        if not p.exists():
            raise fail(f"Файл не найден: {f}", title="Нет файла")
        resolved.append(str(p))
    return resolved


# --------------------------------------------------------------------------- #
# Общий запуск отправки
# --------------------------------------------------------------------------- #
async def _run_send(settings: Settings, target_value: str, sender) -> str | int:
    """Резолвит цель, открывает клиент и вызывает ``sender(client, target)``."""
    sm = await init_db(settings.db_path)
    target = await resolve_target(sm, target_value)
    client = build_client(settings)
    async with client:
        with console.status("[cyan]Отправка…", spinner="dots"):
            await sender(client, target)
    return target


def _dispatch(target_value: str, sender) -> None:
    settings = get_settings()
    require_login(settings)
    target = run_async(_run_send(settings, target_value, sender))
    success(f"Отправлено в [bold]{target}[/bold]")


# --------------------------------------------------------------------------- #
# Текст
# --------------------------------------------------------------------------- #
@app.command(context_settings=ALLOW_NEG)
def send(
    message: str = typer.Argument(..., help="Текст сообщения"),
    rest: list[str] | None = typer.Argument(None, help="[цель] [подпись]"),
    to: str | None = typer.Option(None, "--to", help="Цель: имя чата / ID / @username"),
    caption: str | None = typer.Option(None, "--caption", help="Доп. подпись к тексту"),
) -> None:
    """Отправить текстовое сообщение."""
    target, cap = _pick_target_caption(rest or [], to, caption)
    text = message if not cap else f"{message}\n\n{cap}"

    async def sender(client, tgt):
        await client.send_message(tgt, text)

    _dispatch(target, sender)


# --------------------------------------------------------------------------- #
# Медиа из файлов
# --------------------------------------------------------------------------- #
@app.command(context_settings=ALLOW_NEG)
def sendfile(
    items: list[str] = typer.Argument(..., help="Файлы [цель] [подпись]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
    caption: str | None = typer.Option(None, "--caption", help="Подпись"),
) -> None:
    """Отправить файл(ы) как документ."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        for index, path in enumerate(files):
            await client.send_document(tgt, path, caption=cap if index == 0 else None)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG)
def sendphoto(
    items: list[str] = typer.Argument(..., help="Фото [цель] [подпись]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
    caption: str | None = typer.Option(None, "--caption", help="Подпись"),
) -> None:
    """Отправить фото (несколько — альбомом)."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        if len(files) == 1:
            await client.send_photo(tgt, files[0], caption=cap)
        else:
            media = [
                InputMediaPhoto(path, caption=cap if i == 0 else None)
                for i, path in enumerate(files)
            ]
            await client.send_media_group(tgt, media)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG)
def sendvideo(
    items: list[str] = typer.Argument(..., help="Видео [цель] [подпись]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
    caption: str | None = typer.Option(None, "--caption", help="Подпись"),
) -> None:
    """Отправить видео (несколько — альбомом)."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        if len(files) == 1:
            await client.send_video(tgt, files[0], caption=cap)
        else:
            media = [
                InputMediaVideo(path, caption=cap if i == 0 else None)
                for i, path in enumerate(files)
            ]
            await client.send_media_group(tgt, media)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG)
def sendaudio(
    items: list[str] = typer.Argument(..., help="Аудио [цель] [подпись]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
    caption: str | None = typer.Option(None, "--caption", help="Подпись"),
) -> None:
    """Отправить аудио/музыку."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        for index, path in enumerate(files):
            await client.send_audio(tgt, path, caption=cap if index == 0 else None)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG)
def sendvoice(
    items: list[str] = typer.Argument(..., help="Файл [цель] [подпись]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
    caption: str | None = typer.Option(None, "--caption", help="Подпись"),
) -> None:
    """Отправить голосовое сообщение."""
    files, target, cap = _split_media_args(items, to, caption)
    files = _validate_files(files)

    async def sender(client, tgt):
        await client.send_voice(tgt, files[0], caption=cap)

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG)
def sendvideonote(
    items: list[str] = typer.Argument(..., help="Файл [цель]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
) -> None:
    """Отправить видео-кружок (video note)."""
    files, target, _ = _split_media_args(items, to, None)
    files = _validate_files(files)

    async def sender(client, tgt):
        await client.send_video_note(tgt, files[0])

    _dispatch(target, sender)


@app.command(context_settings=ALLOW_NEG)
def sendsticker(
    items: list[str] = typer.Argument(..., help="Файл .tgs/.webp [цель]"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
) -> None:
    """Отправить стикер."""
    files, target, _ = _split_media_args(items, to, None)
    files = _validate_files(files)

    async def sender(client, tgt):
        await client.send_sticker(tgt, files[0])

    _dispatch(target, sender)


# --------------------------------------------------------------------------- #
# Контакт
# --------------------------------------------------------------------------- #
@app.command(context_settings=ALLOW_NEG)
def sendcontact(
    args: list[str] | None = typer.Argument(
        None, help="Позиционно: <phone> <first> [last] <target>"
    ),
    phone: str | None = typer.Option(None, "--phone", help="Номер телефона"),
    first_name: str | None = typer.Option(None, "--first-name", help="Имя"),
    last_name: str | None = typer.Option(None, "--last-name", help="Фамилия"),
    to: str | None = typer.Option(None, "--to", help="Цель"),
) -> None:
    """Отправить контакт."""
    args = list(args or [])

    # Позиционный разбор, только если соответствующие флаги не заданы.
    if phone is None and args:
        phone = args.pop(0)
    if first_name is None and args:
        first_name = args.pop(0)
    # Если осталось 2 токена — это [last_name, target]; если 1 — это target.
    if len(args) >= 2 and last_name is None:
        last_name = args.pop(0)
    if to is None and args:
        to = args.pop(0)

    if args:
        raise fail(f"Лишние аргументы: {' '.join(args)}", title="Неверные аргументы")
    if not phone or not first_name:
        raise fail("Нужны --phone и --first-name (или позиционно).")
    if to is None:
        raise fail("Не указана цель. Используйте --to или позиционный аргумент.")

    async def sender(client, tgt):
        await client.send_contact(
            tgt, phone_number=phone, first_name=first_name, last_name=last_name
        )

    _dispatch(to, sender)
