"""Команды авторизации: login / logout / whoami."""

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
from ..config import Settings, get_settings, save_credentials
from ..console import console, fail, success

app = typer.Typer(help="Авторизация Telegram-аккаунта.")


def _ensure_credentials(
    settings: Settings, api_id: int | None, api_hash: str | None
) -> None:
    """Дополнить недостающие api_id/api_hash из промптов и сохранить в .env."""
    if api_id is None:
        api_id = settings.api_id
    if api_hash is None:
        api_hash = settings.api_hash

    if api_id is None:
        console.print(
            "Получите api_id/api_hash на [link]https://my.telegram.org[/link] "
            "(API development tools)."
        )
        api_id = int(Prompt.ask("api_id"))
    if not api_hash:
        api_hash = Prompt.ask("api_hash")

    save_credentials(settings, api_id, api_hash)


async def _login(settings: Settings, phone: str | None) -> None:
    client = build_client(settings)
    await client.connect()
    try:
        phone = phone or Prompt.ask("Номер телефона (в формате +7…)")
        sent = await client.send_code(phone)
        code = Prompt.ask("Код из Telegram")
        try:
            await client.sign_in(phone, sent.phone_code_hash, code)
        except SessionPasswordNeeded:
            password = Prompt.ask("Пароль двухфакторной аутентификации", password=True)
            await client.check_password(password)

        me = await client.get_me()
    finally:
        await client.disconnect()

    handle = f"@{me.username}" if me.username else "—"
    success(
        f"Вход выполнен как [bold]{me.first_name or ''}[/bold] "
        f"({handle}, id={me.id})",
        title="Авторизация",
    )


@app.command()
def login(
    api_id: int | None = typer.Option(None, "--api-id", help="api_id с my.telegram.org"),
    api_hash: str | None = typer.Option(None, "--api-hash", help="api_hash с my.telegram.org"),
    phone: str | None = typer.Option(None, "--phone", help="Номер телефона"),
) -> None:
    """Войти в Telegram-аккаунт (интерактивно)."""
    settings = get_settings()
    _ensure_credentials(settings, api_id, api_hash)
    try:
        run_async(_login(settings, phone))
    except (PhoneCodeInvalid, BadRequest) as exc:
        raise fail(str(exc), title="Не удалось войти")


async def _logout(settings: Settings) -> None:
    client = build_client(settings)
    await client.connect()
    try:
        await client.log_out()
    finally:
        # log_out уже разрывает соединение; disconnect на всякий случай игнорируем.
        try:
            await client.disconnect()
        except ConnectionError:
            pass


@app.command()
def logout() -> None:
    """Выйти из аккаунта и удалить локальную сессию."""
    settings = get_settings()
    if not settings.session_file.exists():
        raise fail("Активной сессии нет.", title="Нет сессии")
    run_async(_logout(settings))
    settings.session_file.unlink(missing_ok=True)
    success("Сессия удалена, выход выполнен.", title="Выход")


async def _whoami(settings: Settings) -> Table:
    client = build_client(settings)
    async with client:
        me = await client.get_me()

    table = Table(title="Текущий аккаунт", header_style="bold cyan", show_header=False)
    table.add_column("Поле", style="bold")
    table.add_column("Значение")
    table.add_row("ID", str(me.id))
    table.add_row("Имя", f"{me.first_name or ''} {me.last_name or ''}".strip() or "—")
    table.add_row("Username", f"@{me.username}" if me.username else "—")
    table.add_row("Телефон", f"+{me.phone_number}" if me.phone_number else "—")
    return table


@app.command()
def whoami() -> None:
    """Показать данные текущего аккаунта."""
    from ..client import require_login

    settings = get_settings()
    require_login(settings)
    table = run_async(_whoami(settings))
    console.print(table)
