"""Meta commands: version (tool version and environment diagnostics)."""

from __future__ import annotations

import platform
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version

import typer

from .. import __version__
from ..config import Settings
from ..console import info_panel
from ..i18n import LANG, t

app = typer.Typer()


def version_line() -> str:
    """Single-line version string, shared with the ``--version`` flag."""
    return f"tguser {__version__}"


def _kurigram_version() -> str:
    """Version of the installed Kurigram (imported as ``pyrogram``, shipped as ``kurigram``)."""
    try:
        return distribution_version("kurigram")
    except PackageNotFoundError:
        return t("info.unknown")


@app.command("version", help=t("info.version_help"))
def version() -> None:
    """Show the tool version along with the environment it runs in."""
    # Settings() rather than get_settings(): this command only reads, so it must not
    # create the config directory as a side effect.
    settings = Settings()
    rows = [
        (t("info.label_version"), __version__),
        (t("info.label_python"), platform.python_version()),
        (t("info.label_kurigram"), _kurigram_version()),
        (t("info.label_config"), str(settings.config_dir)),
        (
            t("info.label_session"),
            t("info.session_present")
            if settings.session_file.exists()
            else t("info.session_missing"),
        ),
        (
            t("info.label_credentials"),
            t("info.credentials_set")
            if settings.has_credentials
            else t("info.credentials_missing"),
        ),
        (t("info.label_language"), LANG),
    ]
    info_panel(rows, title=t("info.title"))
