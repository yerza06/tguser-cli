"""Authentication commands: login / logout / whoami."""

from __future__ import annotations

import typer
from pyrogram.errors import (
    BadRequest,
    PhoneCodeInvalid,
    SessionPasswordNeeded,
)
from rich.prompt import Prompt
from rich.table import Table

from ..client import build_client, run_async
from ..config import Settings, get_settings, save_credentials, save_phone_number
from ..console import console, fail, success
from ..i18n import t

app = typer.Typer(help=t("auth.help"))


def _ensure_credentials(
    settings: Settings, api_id: int | None, api_hash: str | None
) -> None:
    """Fill missing api_id/api_hash from prompts and persist them to .env."""
    if api_id is None:
        api_id = settings.api_id
    if api_hash is None:
        api_hash = settings.api_hash

    if api_id is None:
        console.print(t("auth.get_credentials"))
        api_id = int(Prompt.ask("api_id"))
    if not api_hash:
        api_hash = Prompt.ask("api_hash")

    save_credentials(settings, api_id, api_hash)


async def _login(settings: Settings, phone: str | None) -> None:
    client = build_client(settings)
    await client.connect()
    try:
        phone = (phone or settings.phone_number or Prompt.ask(t("auth.prompt_phone"))).strip()
        sent = await client.send_code(phone)
        code = Prompt.ask(t("auth.prompt_code"))
        try:
            await client.sign_in(phone, sent.phone_code_hash, code)
        except SessionPasswordNeeded:
            password = Prompt.ask(t("auth.prompt_password"), password=True)
            await client.check_password(password)

        me = await client.get_me()
    finally:
        await client.disconnect()

    # Persist only after a successful sign-in, so a typo never ends up in .env.
    if phone != settings.phone_number:
        save_phone_number(settings, phone)

    handle = f"@{me.username}" if me.username else "—"
    success(
        t("auth.signed_in", name=me.first_name or "", handle=handle, id=me.id),
        title=t("auth.title"),
    )


@app.command(help=t("auth.login_help"))
def login(
    api_id: int | None = typer.Option(None, "--api-id", help=t("auth.opt_api_id")),
    api_hash: str | None = typer.Option(None, "--api-hash", help=t("auth.opt_api_hash")),
    phone: str | None = typer.Option(None, "--phone", help=t("auth.opt_phone")),
) -> None:
    """Sign in to the Telegram account (interactive)."""
    settings = get_settings()
    _ensure_credentials(settings, api_id, api_hash)
    try:
        run_async(_login(settings, phone))
    except (PhoneCodeInvalid, BadRequest) as exc:
        raise fail(str(exc), title=t("auth.login_failed"))


async def _logout(settings: Settings) -> None:
    client = build_client(settings)
    await client.connect()
    try:
        await client.log_out()
    finally:
        # log_out already tears down the connection; ignore a redundant disconnect.
        try:
            await client.disconnect()
        except ConnectionError:
            pass


@app.command(help=t("auth.logout_help"))
def logout() -> None:
    """Log out and delete the local session."""
    settings = get_settings()
    if not settings.session_file.exists():
        raise fail(t("auth.no_active_session"), title=t("client.no_session_title"))
    run_async(_logout(settings))
    settings.session_file.unlink(missing_ok=True)
    success(t("auth.logged_out"), title=t("auth.logout_title"))


async def _whoami(settings: Settings) -> Table:
    client = build_client(settings)
    async with client:
        me = await client.get_me()

    table = Table(title=t("auth.whoami_title"), header_style="bold cyan", show_header=False)
    table.add_column("field", style="bold")
    table.add_column("value")
    table.add_row("ID", str(me.id))
    table.add_row(t("auth.field_name"), f"{me.first_name or ''} {me.last_name or ''}".strip() or "—")
    table.add_row("Username", f"@{me.username}" if me.username else "—")
    table.add_row(t("auth.field_phone"), f"+{me.phone_number}" if me.phone_number else "—")
    return table


@app.command(help=t("auth.whoami_help"))
def whoami() -> None:
    """Show the current account details."""
    from ..client import require_login

    settings = get_settings()
    require_login(settings)
    table = run_async(_whoami(settings))
    console.print(table)
