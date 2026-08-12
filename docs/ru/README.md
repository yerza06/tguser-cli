# Документация tguser (русский)

`tguser` — CLI-инструмент для отправки сообщений в **Telegram от имени пользователя**
(протокол MTProto, не бот). Позволяет писать в личные чаты, группы и каналы как обычный
человек, а именованные идентификаторы чатов хранятся локально в SQLite (по аналогии с `git remote`).

**Стек:** Python 3.13 · uv · Kurigram (форк Pyrogram) · Typer + Rich · Pydantic-Settings · SQLAlchemy 2.0 (async) + SQLite.

## Оглавление

| Раздел | Описание |
|--------|----------|
| [01. Установка](01-installation.md) | Требования, глобальная установка из GitHub через `uv tool install` |
| [02. Авторизация](02-authentication.md) | Получение api_id/api_hash, вход, выход, текущий аккаунт |
| [03. Конфигурация](03-configuration.md) | Переменные `TGUSER_*`, расположение файлов |
| [04. Управление чатами](04-chat-management.md) | Именованные alias чатов (`chat add/list/…`) |
| [05. Отправка сообщений](05-sending.md) | Текст, файлы, фото, видео, аудио, контакты и др. |
| [06. Интеграция с ИИ-агентами](06-ai-agents.md) | Глобальный вызов `tguser`, коды выхода, готовый Agent Skill |
| [07. Решение проблем](07-troubleshooting.md) | Частые ошибки и их устранение |
| [08. Обнаружение чатов](08-discovery.md) | Как узнать ID чата (`dialogs`, `resolve`) |

## Быстрый старт

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git   # установить глобально из GitHub
tguser login                           # вход в аккаунт
tguser chat add work -1001234567890    # сохранить чат под именем work
tguser send "Привет" --to work         # отправить сообщение
```

После `uv tool install` команда `tguser` доступна из любой директории — без `uv run`.
Установка из клона репозитория и режим разработки (`uv sync` + `uv run`) —
в [01. Установка](01-installation.md).

> ⚠️ **Не удаляйте файлы `~/.config/tguser/tguser.session` и `~/.config/tguser/tguser.db`** —
> это авторизация в Telegram и база сохранённых чатов. Что это за файлы, зачем они нужны и что
> будет, если их удалить, — в [03. Конфигурация](03-configuration.md#-файлы-tgusersession-и-tguserdb-нельзя-удалять).

> См. также краткий обзор в корневом [README.md](../../README.md).
