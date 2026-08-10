# tguser

CLI-инструмент для отправки сообщений в **Telegram от имени пользователя** (протокол MTProto,
не бот) — для ИИ-агентов вроде Hermes-Agent, OpenClaw, Claude Code, Codex CLI и т.п.

Агент может писать в личные чаты, группы и каналы как обычный человек, а именованные
идентификаторы чатов хранятся локально в SQLite (по аналогии с `git remote`).

## Стек

Python 3.13 · [uv](https://docs.astral.sh/uv/) · [Kurigram](https://github.com/KurimuzonAkuma/pyrogram)
(форк Pyrogram) · [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) ·
Pydantic-Settings · SQLAlchemy 2.0 (async) + aiosqlite.

## Установка

```bash
uv tool install .
```

Команда собирает пакет, создаёт для него изолированное окружение в
`~/.local/share/uv/tools/tguser/` и кладёт исполняемый файл в `~/.local/bin/tguser`. После этого
`tguser` вызывается **из любой директории** — без `uv run` и без перехода в корень репозитория.
Это то, что нужно ИИ-агентам: их рабочий каталог заранее неизвестен.

```bash
uv tool install . --force    # переустановить после изменений в коде
uv tool install -e .         # editable-режим: правки применяются сразу
uv tool uninstall tguser     # удалить
```

Для разработки самого инструмента достаточно `uv sync` — тогда запуск идёт через
`uv run tguser …` из корня проекта. Подробности — в [docs/ru/01-installation.md](docs/ru/01-installation.md).

## Авторизация

Получите `api_id` и `api_hash` на <https://my.telegram.org> (раздел *API development tools*),
затем войдите:

```bash
tguser login            # спросит api_id/api_hash (если не заданы), телефон и код
tguser whoami           # показать текущий аккаунт
tguser logout           # выйти и удалить сессию
```

Учётные данные сохраняются в `~/.config/tguser/.env`, сессия — в `~/.config/tguser/tguser.session`,
база чатов — в `~/.config/tguser/tguser.db`.

Можно задать переменные окружения вручную (см. `.env.example`):

```bash
export TGUSER_API_ID=1234567
export TGUSER_API_HASH=0123456789abcdef0123456789abcdef
```

## Управление чатами

```bash
tguser chat add work -1001234567890     # добавить alias
tguser chat list                        # таблица всех чатов (или просто `tguser chat`)
tguser chat get-id work                 # вывести ID
tguser chat replace-id work -100999     # заменить ID
tguser chat rename work team            # переименовать
tguser chat remove team                 # удалить
```

## Отправка

Цель (`--to`) — это **имя сохранённого чата**, числовой ID, `@username` или `me` (Избранное).
Все медиа-команды поддерживают два синтаксиса — флаги и позиционные аргументы:

```bash
# Текст
tguser send "Привет" --to work
tguser send "Привет" work

# Фото (несколько — альбомом), с подписью
tguser sendphoto a.png b.png --to work --caption "Фотографии"
tguser sendphoto a.png b.png work "Фотографии"

# Документы (несколько можно сгруппировать через -G/--group)
tguser sendfile report.pdf --to work --caption "Отчёт"
tguser sendfile part1.pdf part2.pdf --to work --group

# Аудио / видео / голосовое / видео-кружок / стикер
tguser sendaudio track.mp3 --to me
tguser sendvideo clip.mp4 me "Клип"
tguser sendvoice voice.ogg --to me
tguser sendvideonote note.mp4 --to me
tguser sendsticker sticker.webp --to me

# Контакт
tguser sendcontact --phone +77001234567 --first-name Иван --last-name Петров --to work
tguser sendcontact +77001234567 Иван Петров work
```

## Структура

```
src/tguser/
├── cli.py            # корневое Typer-приложение
├── config.py         # Pydantic-Settings
├── client.py         # клиент Kurigram + run_async
├── console.py        # Rich-хелперы вывода
├── resolver.py       # alias из БД → chat_id
├── db/               # модели и CRUD (SQLAlchemy async)
└── commands/         # auth / chat / send
```

## Планы

После рабочего прототипа на Python — возможный порт CLI на Rust (Typer → clap, Kurigram → grammers/tdlib).
