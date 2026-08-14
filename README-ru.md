# tguser

[English](README.md) · **Русский**

📖 **[Сайт документации](https://yerza06.github.io/tguser-cli/ru/)**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-managed-DE5FE9?style=for-the-badge&logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![Telegram](https://img.shields.io/badge/Telegram-MTProto-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/mtproto)
[![License](https://img.shields.io/badge/License-MIT-3DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

[![Typer](https://img.shields.io/badge/Typer-CLI-009485?style=for-the-badge&logo=typer&logoColor=white)](https://typer.tiangolo.com/)
[![Rich](https://img.shields.io/badge/Rich-%D0%B2%D1%8B%D0%B2%D0%BE%D0%B4-FAE742?style=for-the-badge&logo=rich&logoColor=black)](https://rich.readthedocs.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Settings-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%20async-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-aiosqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

[![skills.sh](https://www.skills.sh/b/yerza06/tguser-cli?style=for-the-badge&logo=vercel&logoColor=%23FFFFFF&label=skills.sh&color=%23000000)](https://www.skills.sh/yerza06/tguser-cli)
![GitHub watchers](https://img.shields.io/github/watchers/yerza06/tguser-cli?style=for-the-badge&logo=github&labelColor=%23000000&color=%23FFFFFF)
![GitHub Repo stars](https://img.shields.io/github/stars/yerza06/tguser-cli?style=for-the-badge&logo=github&labelColor=%23000000&color=%23FFFFFF)

CLI-инструмент для отправки сообщений в **Telegram от имени пользователя** (протокол MTProto,
не бот) — для ИИ-агентов вроде Hermes-Agent, OpenClaw, Claude Code, Codex CLI и т.п.

Агент может писать в личные чаты, группы и каналы как обычный человек, а именованные
идентификаторы чатов хранятся локально в SQLite (по аналогии с `git remote`).

## Стек

Python 3.13 · [uv](https://docs.astral.sh/uv/) · [Kurigram](https://github.com/KurimuzonAkuma/pyrogram)
(форк Pyrogram) · [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) ·
Pydantic-Settings · SQLAlchemy 2.0 (async) + aiosqlite.

## Установка

Прямо из GitHub, клонировать репозиторий не нужно:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
```

Если репозиторий уже склонирован (или вы хотите поправить код):

```bash
git clone https://github.com/yerza06/tguser-cli.git
cd tguser-cli
uv tool install .
```

Команда собирает пакет, создаёт для него изолированное окружение в
`~/.local/share/uv/tools/tguser/` и кладёт исполняемый файл в `~/.local/bin/tguser`. После этого
`tguser` вызывается **из любой директории** — без `uv run` и без перехода в корень репозитория.
Это то, что нужно ИИ-агентам: их рабочий каталог заранее неизвестен.

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git --force   # обновить до свежей версии
uv tool install . --force    # переустановить после изменений в коде (из клона)
uv tool install -e .         # editable-режим: правки применяются сразу
uv tool uninstall tguser     # удалить
```

Для разработки самого инструмента достаточно `uv sync` — тогда запуск идёт через
`uv run tguser …` из корня проекта. Подробности — в [Установке](https://yerza06.github.io/tguser-cli/ru/docs/installation/).

## Авторизация

Получите `api_id` и `api_hash` на <https://my.telegram.org> (раздел _API development tools_),
затем войдите:

```bash
tguser login            # спросит api_id/api_hash и телефон (если не заданы), а также код
tguser whoami           # показать текущий аккаунт
tguser logout           # выйти и удалить сессию
```

Учётные данные сохраняются в `~/.config/tguser/.env`, сессия — в `~/.config/tguser/tguser.session`,
база чатов — в `~/.config/tguser/tguser.db`.

> ⚠️ **Не удаляйте `~/.config/tguser/tguser.session` и `~/.config/tguser/tguser.db`.**
> Это рабочее состояние инструмента: авторизация в Telegram и все сохранённые имена чатов.
> Восстановить их автоматически нельзя — после удаления придётся заново проходить `tguser login`
> и заново добавлять все alias вручную. Чтобы выйти из аккаунта, используйте `tguser logout`,
> а не удаление файла. Подробнее — в
> [Конфигурация](https://yerza06.github.io/tguser-cli/ru/docs/configuration/#-файлы-tgusersession-и-tguserdb-нельзя-удалять).

Можно задать переменные окружения вручную (см. `.env.example`):

```bash
export TGUSER_API_ID=1234567
export TGUSER_API_HASH=0123456789abcdef0123456789abcdef
export TGUSER_PHONE_NUMBER=+79991234567   # необязательно: пропускает промпт телефона в `login`
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

## Skill для ИИ-агентов

В репозитории лежит готовый **Agent Skill** — описание инструмента, которое агент подгружает сам,
как только задача касается Telegram. Установка одной командой:

```bash
npx skills add https://github.com/yerza06/tguser-cli --skills tguser
```

Установщик спросит, для каких агентов настроить skill, и положит его в нужный каталог
(`~/.claude/skills/` для Claude Code, `~/.codex/skills/` для Codex CLI, `~/.agents/skills/` для
Cline/Zed/Warp и т.д.). Skill написан по открытой спецификации
[Agent Skills](https://agentskills.io/specification), поэтому работает в любом агенте с её
поддержкой.

Исходник — [`skills/tguser/`](skills/tguser/SKILL.md), подробности —
[Интеграция с ИИ-агентами](https://yerza06.github.io/tguser-cli/ru/docs/ai-agents/#готовый-skill).

> Skill не умеет входить в аккаунт: `tguser login` один раз выполняет человек.

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

skills/tguser/        # Agent Skill (skills.sh)
├── SKILL.md          # краткая инструкция + frontmatter
└── references/       # полные таблицы флагов и troubleshooting

site/                 # сайт документации (Hugo + Hextra → GitHub Pages)
├── hugo.yaml
└── content/          # лендинг и документация, английская и русская
```

## Планы

После рабочего прототипа на Python — возможный порт CLI на Rust (Typer → clap, Kurigram → grammers/tdlib).
