"""Root tguser CLI application."""

from __future__ import annotations

import typer

from . import __version__
from .commands import auth, chat, discovery, send
from .i18n import t

app = typer.Typer(
    name="tguser",
    help=t("app.help"),
    no_args_is_help=True,
    add_completion=True,
)

# Auth commands live at the top level (tguser login / logout / whoami).
app.registered_commands.extend(auth.app.registered_commands)

# Sub-application for chat management (tguser chat …).
app.add_typer(chat.app, name="chat")

# Chat discovery commands (tguser dialogs / resolve).
app.registered_commands.extend(discovery.app.registered_commands)

# Sending commands at the top level (tguser send / sendphoto / …).
app.registered_commands.extend(send.app.registered_commands)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"tguser {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-V", callback=_version_callback, is_eager=True,
        help=t("app.version_help"),
    ),
) -> None:
    """tguser — send Telegram messages as a user."""
