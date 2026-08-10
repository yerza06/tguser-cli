# tguser Documentation (English)

`tguser` is a CLI tool for sending messages to **Telegram as a user** (MTProto protocol, not a bot).
It lets you write to private chats, groups, and channels like a regular person, while named chat
identifiers are stored locally in SQLite (similar to `git remote`).

**Stack:** Python 3.13 · uv · Kurigram (a Pyrogram fork) · Typer + Rich · Pydantic-Settings · SQLAlchemy 2.0 (async) + SQLite.

## Table of Contents

| Section | Description |
|---------|-------------|
| [01. Installation](01-installation.md) | Requirements, installing globally with `uv tool install .` |
| [02. Authentication](02-authentication.md) | Getting api_id/api_hash, login, logout, current account |
| [03. Configuration](03-configuration.md) | `TGUSER_*` variables, file locations |
| [04. Chat Management](04-chat-management.md) | Named chat aliases (`chat add/list/…`) |
| [05. Sending Messages](05-sending.md) | Text, files, photos, videos, audio, contacts, and more |
| [06. AI Agent Integration](06-ai-agents.md) | Calling `tguser` globally, exit codes, typical commands |
| [07. Troubleshooting](07-troubleshooting.md) | Common errors and how to fix them |
| [08. Chat Discovery](08-discovery.md) | How to find a chat's ID (`dialogs`, `resolve`) |

## Quick Start

```bash
uv tool install .                      # install tguser globally (from the project root)
tguser login                           # sign in to your account
tguser chat add work -1001234567890    # save a chat under the name "work"
tguser send "Hello" --to work          # send a message
```

After `uv tool install .` the `tguser` command is available from any directory — no `uv run`
needed. For details and the development workflow (`uv sync` + `uv run`), see
[01. Installation](01-installation.md).

> See also the short overview in the root [README.md](../../README.md).
