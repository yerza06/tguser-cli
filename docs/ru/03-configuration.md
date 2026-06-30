# 03. Конфигурация

`tguser` настраивается через переменные окружения (Pydantic-Settings) с префиксом `TGUSER_`.

## Переменные окружения

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `TGUSER_API_ID` | — | api_id с my.telegram.org |
| `TGUSER_API_HASH` | — | api_hash с my.telegram.org |
| `TGUSER_CONFIG_DIR` | `~/.config/tguser` | Каталог для сессии, БД и `.env` |
| `TGUSER_SESSION_NAME` | `tguser` | Имя сессии (имя файла `<name>.session`) |

## Источники настроек и приоритет

Настройки читаются из двух источников (более высокий приоритет — у переменных окружения):

1. **Переменные окружения** `TGUSER_*`.
2. **Файл** `~/.config/tguser/.env`.

Пример `.env` (см. также `.env.example` в корне проекта):

```dotenv
TGUSER_API_ID=1234567
TGUSER_API_HASH=0123456789abcdef0123456789abcdef
# TGUSER_CONFIG_DIR=~/.config/tguser
# TGUSER_SESSION_NAME=tguser
```

## Расположение файлов

Все рабочие файлы лежат в `TGUSER_CONFIG_DIR` (по умолчанию `~/.config/tguser/`):

| Файл | Назначение |
|------|------------|
| `.env` | api_id/api_hash (создаётся командой `login`, права `0600`) |
| `tguser.session` | Файл сессии Kurigram |
| `tguser.db` | База SQLite с именованными чатами |

Благодаря единому каталогу конфигурации команду `tguser` можно запускать из любой директории —
сессия и база чатов находятся всегда в одном месте.

## Отдельное окружение

Чтобы использовать другой аккаунт или изолированную базу (например, для тестов), задайте
свой каталог:

```bash
export TGUSER_CONFIG_DIR=/path/to/another/profile
tguser login
```
