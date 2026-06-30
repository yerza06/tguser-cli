"""Корневое CLI-приложение tguser."""

from __future__ import annotations

import typer

from . import __version__
from .commands import auth, chat, discovery, send

app = typer.Typer(
    name="tguser",
    help="Отправка сообщений в Telegram от имени пользователя (MTProto) для ИИ-агентов.",
    no_args_is_help=True,
    add_completion=True,
)

# Команды авторизации — на верхнем уровне (tguser login / logout / whoami).
app.registered_commands.extend(auth.app.registered_commands)

# Под-приложение для управления чатами (tguser chat …).
app.add_typer(chat.app, name="chat")

# Команды обнаружения чатов (tguser dialogs / resolve).
app.registered_commands.extend(discovery.app.registered_commands)

# Команды отправки — на верхнем уровне (tguser send / sendphoto / …).
app.registered_commands.extend(send.app.registered_commands)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"tguser {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-V", callback=_version_callback, is_eager=True,
        help="Показать версию и выйти.",
    ),
) -> None:
    """tguser — отправка в Telegram от имени пользователя."""


if __name__ == "__main__":
    app()
