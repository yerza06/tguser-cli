"""Lightweight internationalization for CLI output.

The active language is resolved once, at import time, so that Typer ``help=`` texts
(evaluated while the CLI is being built) are already localized. Resolution order:

1. the ``TGUSER_LANG`` environment variable;
2. a ``TGUSER_LANG=`` entry in the ``.env`` file inside the config directory;
3. the default, ``"en"``.

Unknown languages fall back to English. Use :func:`t` to look up a message by key.
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_LANG = "en"
SUPPORTED = ("en", "ru")


def _lang_from_env_file() -> str | None:
    """Read ``TGUSER_LANG`` from the config-dir ``.env`` without importing config."""
    config_dir = os.environ.get("TGUSER_CONFIG_DIR")
    base = Path(config_dir).expanduser() if config_dir else Path.home() / ".config" / "tguser"
    env_file = base / ".env"
    try:
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if stripped.startswith("#") or "=" not in stripped:
                continue
            key, _, value = stripped.partition("=")
            if key.strip() == "TGUSER_LANG":
                return value.strip()
    except OSError:
        return None
    return None


def _resolve_lang() -> str:
    """Determine the active language (see module docstring for the order)."""
    candidate = os.environ.get("TGUSER_LANG") or _lang_from_env_file() or DEFAULT_LANG
    candidate = candidate.strip().lower()
    return candidate if candidate in SUPPORTED else DEFAULT_LANG


LANG = _resolve_lang()


def t(key: str, /, **kwargs: object) -> str:
    """Return the localized message for ``key``, formatted with ``kwargs``.

    Falls back to English if the key is missing a translation for the active language,
    and to the key itself if the key is unknown (should not happen in practice).
    """
    entry = MESSAGES.get(key)
    if entry is None:
        return key
    template = entry.get(LANG) or entry.get(DEFAULT_LANG) or key
    return template.format(**kwargs) if kwargs else template


# --------------------------------------------------------------------------- #
# Message catalog: {key: {"en": ..., "ru": ...}}
# --------------------------------------------------------------------------- #
MESSAGES: dict[str, dict[str, str]] = {
    # --- common -----------------------------------------------------------
    "common.done": {"en": "Done", "ru": "Готово"},
    "common.error": {"en": "Error", "ru": "Ошибка"},
    "common.invalid_args": {"en": "Invalid arguments", "ru": "Неверные аргументы"},
    "common.extra_args": {
        "en": "Extra arguments: {args}",
        "ru": "Лишние аргументы: {args}",
    },
    "common.no_target": {
        "en": "No target specified. Use --to or a positional argument.",
        "ru": "Не указана цель. Используйте --to или позиционный аргумент.",
    },
    "common.telegram_error_title": {"en": "Telegram error", "ru": "Ошибка Telegram"},
    "common.unexpected_error_title": {
        "en": "Unexpected error",
        "ru": "Непредвиденная ошибка",
    },
    # --- app / cli --------------------------------------------------------
    "app.help": {
        "en": "Send Telegram messages as a user (MTProto) for AI agents.",
        "ru": "Отправка сообщений в Telegram от имени пользователя (MTProto) для ИИ-агентов.",
    },
    "app.version_help": {
        "en": "Show version and exit.",
        "ru": "Показать версию и выйти.",
    },
    # --- info / version ---------------------------------------------------
    "info.version_help": {
        "en": "Show the version and environment information.",
        "ru": "Показать версию и информацию об окружении.",
    },
    "info.title": {"en": "Version info", "ru": "Информация о версии"},
    "info.label_version": {"en": "Version:", "ru": "Версия:"},
    "info.label_python": {"en": "Python:", "ru": "Python:"},
    "info.label_kurigram": {"en": "Kurigram:", "ru": "Kurigram:"},
    "info.label_config": {"en": "Config:", "ru": "Конфигурация:"},
    "info.label_session": {"en": "Session:", "ru": "Сессия:"},
    "info.label_credentials": {"en": "Credentials:", "ru": "Учётные данные:"},
    "info.label_language": {"en": "Language:", "ru": "Язык:"},
    "info.session_present": {"en": "present", "ru": "есть"},
    "info.session_missing": {"en": "missing", "ru": "нет"},
    "info.credentials_set": {"en": "set", "ru": "заданы"},
    "info.credentials_missing": {"en": "not set", "ru": "не заданы"},
    "info.unknown": {"en": "unknown", "ru": "неизвестно"},
    # --- auth -------------------------------------------------------------
    "auth.help": {
        "en": "Telegram account authentication.",
        "ru": "Авторизация Telegram-аккаунта.",
    },
    "auth.login_help": {
        "en": "Sign in to your Telegram account (interactive).",
        "ru": "Войти в Telegram-аккаунт (интерактивно).",
    },
    "auth.logout_help": {
        "en": "Log out and delete the local session.",
        "ru": "Выйти из аккаунта и удалить локальную сессию.",
    },
    "auth.whoami_help": {
        "en": "Show the current account details.",
        "ru": "Показать данные текущего аккаунта.",
    },
    "auth.opt_api_id": {
        "en": "api_id from my.telegram.org",
        "ru": "api_id с my.telegram.org",
    },
    "auth.opt_api_hash": {
        "en": "api_hash from my.telegram.org",
        "ru": "api_hash с my.telegram.org",
    },
    "auth.opt_phone": {
        "en": "Phone number (default: $TGUSER_PHONE_NUMBER)",
        "ru": "Номер телефона (по умолчанию: $TGUSER_PHONE_NUMBER)",
    },
    "auth.get_credentials": {
        "en": "Get api_id/api_hash at [link]https://my.telegram.org[/link] (API development tools).",
        "ru": "Получите api_id/api_hash на [link]https://my.telegram.org[/link] (API development tools).",
    },
    "auth.prompt_phone": {
        "en": "Phone number (e.g. +1…)",
        "ru": "Номер телефона (в формате +7…)",
    },
    "auth.prompt_code": {"en": "Code from Telegram", "ru": "Код из Telegram"},
    "auth.prompt_password": {
        "en": "Two-factor authentication password",
        "ru": "Пароль двухфакторной аутентификации",
    },
    "auth.signed_in": {
        "en": "Signed in as [bold]{name}[/bold] ({handle}, id={id})",
        "ru": "Вход выполнен как [bold]{name}[/bold] ({handle}, id={id})",
    },
    "auth.title": {"en": "Authentication", "ru": "Авторизация"},
    "auth.login_failed": {"en": "Failed to sign in", "ru": "Не удалось войти"},
    "auth.no_active_session": {
        "en": "No active session.",
        "ru": "Активной сессии нет.",
    },
    "auth.logged_out": {
        "en": "Session deleted, logged out.",
        "ru": "Сессия удалена, выход выполнен.",
    },
    "auth.logout_title": {"en": "Logout", "ru": "Выход"},
    "auth.whoami_title": {"en": "Current account", "ru": "Текущий аккаунт"},
    "auth.field_name": {"en": "Name", "ru": "Имя"},
    "auth.field_phone": {"en": "Phone", "ru": "Телефон"},
    # --- chat -------------------------------------------------------------
    "chat.help": {
        "en": "Manage saved chats (alias → ID).",
        "ru": "Управление сохранёнными чатами (alias → ID).",
    },
    "chat.add_help": {
        "en": "Add a new chat alias (@username/links are resolved when signed in).",
        "ru": "Добавить новый alias чата (@username/ссылки резолвятся при активной сессии).",
    },
    "chat.list_help": {
        "en": "Show all saved chats.",
        "ru": "Показать все сохранённые чаты.",
    },
    "chat.remove_help": {"en": "Remove a chat alias.", "ru": "Удалить alias чата."},
    "chat.get_id_help": {
        "en": "Print the ID of a saved chat.",
        "ru": "Вывести ID сохранённого чата.",
    },
    "chat.replace_id_help": {
        "en": "Replace the ID of a saved chat.",
        "ru": "Заменить ID у сохранённого чата.",
    },
    "chat.rename_help": {
        "en": "Rename a chat alias.",
        "ru": "Переименовать alias чата.",
    },
    "chat.arg_name": {"en": "Chat name (alias)", "ru": "Имя (alias) чата"},
    "chat.arg_chat_id": {
        "en": "Chat ID / @username / link",
        "ru": "ID чата / @username / ссылка",
    },
    "chat.opt_no_resolve": {
        "en": "Store the value as-is, without online resolution",
        "ru": "Сохранить значение как есть, без онлайн-резолва",
    },
    "chat.arg_name_simple": {"en": "Chat name", "ru": "Имя чата"},
    "chat.arg_new_id": {"en": "New chat ID", "ru": "Новый ID чата"},
    "chat.arg_old_name": {"en": "Current name", "ru": "Текущее имя"},
    "chat.arg_new_name": {"en": "New name", "ru": "Новое имя"},
    "chat.exists": {
        "en": "Chat named [bold]{name}[/bold] already exists.",
        "ru": "Чат с именем [bold]{name}[/bold] уже существует.",
    },
    "chat.not_found": {
        "en": "Chat [bold]{name}[/bold] not found.",
        "ru": "Чат [bold]{name}[/bold] не найден.",
    },
    "chat.added": {
        "en": "Added chat [bold]{name}[/bold] → {id}{suffix}",
        "ru": "Добавлен чат [bold]{name}[/bold] → {id}{suffix}",
    },
    "chat.list_empty": {
        "en": "[dim]No chats saved. Add one: tguser chat add <name> <id>[/dim]",
        "ru": "[dim]Список чатов пуст. Добавьте: tguser chat add <name> <id>[/dim]",
    },
    "chat.removed": {
        "en": "Chat [bold]{name}[/bold] removed.",
        "ru": "Чат [bold]{name}[/bold] удалён.",
    },
    "chat.id_replaced": {
        "en": "Chat [bold]{name}[/bold] ID changed to {id}",
        "ru": "ID чата [bold]{name}[/bold] изменён на {id}",
    },
    "chat.renamed": {
        "en": "Chat renamed: [bold]{old}[/bold] → [bold]{new}[/bold]",
        "ru": "Чат переименован: [bold]{old}[/bold] → [bold]{new}[/bold]",
    },
    "chat.resolve_failed": {
        "en": "[yellow]Could not resolve the ID ({error}). Storing “{value}” as-is.[/yellow]",
        "ru": "[yellow]Не удалось определить ID ({error}). Сохраняю «{value}» как есть.[/yellow]",
    },
    "chat.no_session_resolve": {
        "en": "[yellow]No active session — storing the value as-is "
        "(sign in with [bold]tguser login[/bold] for auto-resolution).[/yellow]",
        "ru": "[yellow]Нет активной сессии — сохраняю значение как есть "
        "(войдите через [bold]tguser login[/bold] для авторезолва).[/yellow]",
    },
    # --- console tables ---------------------------------------------------
    "console.chats_title": {"en": "Saved chats", "ru": "Сохранённые чаты"},
    "console.dialogs_title": {"en": "Dialogs", "ru": "Диалоги"},
    "console.col_name": {"en": "Name", "ru": "Имя"},
    "console.col_chat_id": {"en": "Chat ID", "ru": "ID чата"},
    "console.col_title": {"en": "Title", "ru": "Название"},
    "console.col_created": {"en": "Created", "ru": "Создан"},
    "console.col_type": {"en": "Type", "ru": "Тип"},
    "console.col_username": {"en": "@username", "ru": "@username"},
    # --- send -------------------------------------------------------------
    "send.help": {"en": "Send messages and media.", "ru": "Отправка сообщений и медиа."},
    "send.no_files": {
        "en": "No existing file was found. Check the paths.",
        "ru": "Не найдено ни одного существующего файла. Проверьте пути.",
    },
    "send.no_files_title": {"en": "No files", "ru": "Нет файлов"},
    "send.file_not_found": {
        "en": "File not found: {file}",
        "ru": "Файл не найден: {file}",
    },
    "send.no_file_title": {"en": "No file", "ru": "Нет файла"},
    "send.sending": {"en": "[cyan]Sending…", "ru": "[cyan]Отправка…"},
    "send.sent": {
        "en": "Sent to [bold]{target}[/bold]",
        "ru": "Отправлено в [bold]{target}[/bold]",
    },
    "send.failed_title": {"en": "Could not send", "ru": "Не удалось отправить"},
    "send.failed": {
        "en": "Failed to send to '{target}': {error}",
        "ru": "Не удалось отправить в «{target}»: {error}",
    },
    "send.cmd_send": {
        "en": "Send a text message.",
        "ru": "Отправить текстовое сообщение.",
    },
    "send.cmd_sendfile": {
        "en": "Send file(s) as a document.",
        "ru": "Отправить файл(ы) как документ.",
    },
    "send.cmd_sendphoto": {
        "en": "Send a photo (multiple → album).",
        "ru": "Отправить фото (несколько — альбомом).",
    },
    "send.cmd_sendvideo": {
        "en": "Send a video (multiple → album).",
        "ru": "Отправить видео (несколько — альбомом).",
    },
    "send.cmd_sendaudio": {"en": "Send audio / music.", "ru": "Отправить аудио/музыку."},
    "send.cmd_sendvoice": {
        "en": "Send a voice message.",
        "ru": "Отправить голосовое сообщение.",
    },
    "send.cmd_sendvideonote": {
        "en": "Send a video note.",
        "ru": "Отправить видео-кружок (video note).",
    },
    "send.cmd_sendsticker": {"en": "Send a sticker.", "ru": "Отправить стикер."},
    "send.cmd_sendcontact": {"en": "Send a contact.", "ru": "Отправить контакт."},
    "send.arg_message": {"en": "Message text", "ru": "Текст сообщения"},
    "send.arg_rest": {"en": "[target] [caption]", "ru": "[цель] [подпись]"},
    "send.opt_to_full": {
        "en": "Target: chat name / ID / @username",
        "ru": "Цель: имя чата / ID / @username",
    },
    "send.opt_caption_text": {
        "en": "Extra caption for the text",
        "ru": "Доп. подпись к тексту",
    },
    "send.opt_to": {"en": "Target", "ru": "Цель"},
    "send.opt_caption": {"en": "Caption", "ru": "Подпись"},
    "send.opt_group": {
        "en": "Group multiple documents into albums",
        "ru": "Сгруппировать несколько документов в альбомы",
    },
    "send.arg_files": {"en": "Files [target] [caption]", "ru": "Файлы [цель] [подпись]"},
    "send.arg_photos": {"en": "Photos [target] [caption]", "ru": "Фото [цель] [подпись]"},
    "send.arg_videos": {"en": "Videos [target] [caption]", "ru": "Видео [цель] [подпись]"},
    "send.arg_audio": {"en": "Audio [target] [caption]", "ru": "Аудио [цель] [подпись]"},
    "send.arg_voice": {"en": "File [target] [caption]", "ru": "Файл [цель] [подпись]"},
    "send.arg_note": {"en": "File [target]", "ru": "Файл [цель]"},
    "send.arg_sticker": {
        "en": "File .tgs/.webp [target]",
        "ru": "Файл .tgs/.webp [цель]",
    },
    "send.arg_contact": {
        "en": "Positional: <phone> <first> [last] <target>",
        "ru": "Позиционно: <phone> <first> [last] <target>",
    },
    "send.opt_phone": {"en": "Phone number", "ru": "Номер телефона"},
    "send.opt_first": {"en": "First name", "ru": "Имя"},
    "send.opt_last": {"en": "Last name", "ru": "Фамилия"},
    "send.contact_need_fields": {
        "en": "--phone and --first-name are required (or positional).",
        "ru": "Нужны --phone и --first-name (или позиционно).",
    },
    # --- discovery --------------------------------------------------------
    "discovery.dialogs_help": {
        "en": "Show your dialogs (including private chats) with their IDs.",
        "ru": "Показать ваши диалоги (включая закрытые чаты) с их ID.",
    },
    "discovery.resolve_help": {
        "en": "Find a chat's numeric ID by @username or link.",
        "ru": "Узнать числовой ID чата по @username или ссылке.",
    },
    "discovery.opt_search": {
        "en": "Filter by title or @username",
        "ru": "Фильтр по названию или @username",
    },
    "discovery.opt_limit": {
        "en": "How many dialogs to request",
        "ru": "Сколько диалогов запросить",
    },
    "discovery.arg_query": {
        "en": "@username, t.me link, or invite link t.me/+…",
        "ru": "@username, t.me-ссылка или инвайт-ссылка t.me/+…",
    },
    "discovery.no_dialogs": {
        "en": "[dim]No dialogs found.[/dim]",
        "ru": "[dim]Диалоги не найдены.[/dim]",
    },
    "discovery.resolve_failed_title": {
        "en": "Could not resolve the chat",
        "ru": "Не удалось определить чат",
    },
    "discovery.chat_found_title": {"en": "Chat found", "ru": "Чат найден"},
    "discovery.chat_found": {
        "en": "[bold]{title}[/bold] ({type})\nID: [bold]{id}[/bold]",
        "ru": "[bold]{title}[/bold] ({type})\nID: [bold]{id}[/bold]",
    },
    # --- client / login guard --------------------------------------------
    "client.no_credentials_title": {
        "en": "No credentials",
        "ru": "Нет учётных данных",
    },
    "client.no_credentials": {
        "en": "api_id/api_hash are not set. Run: [bold]tguser login[/bold]",
        "ru": "Не заданы api_id/api_hash. Выполните: [bold]tguser login[/bold]",
    },
    "client.no_session_title": {"en": "No session", "ru": "Нет сессии"},
    "client.no_session": {
        "en": "Session not found. Sign in first: [bold]tguser login[/bold]",
        "ru": "Сессия не найдена. Сначала войдите: [bold]tguser login[/bold]",
    },
}
