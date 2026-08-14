# tguser

**English** · [Русский](README-ru.md)

📖 **[Documentation website](https://yerza06.github.io/tguser-cli/)**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-managed-DE5FE9?style=for-the-badge&logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![Telegram](https://img.shields.io/badge/Telegram-MTProto-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/mtproto)
[![License](https://img.shields.io/badge/License-MIT-3DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

[![Typer](https://img.shields.io/badge/Typer-CLI-009485?style=for-the-badge&logo=typer&logoColor=white)](https://typer.tiangolo.com/)
[![Rich](https://img.shields.io/badge/Rich-output-FAE742?style=for-the-badge&logo=rich&logoColor=black)](https://rich.readthedocs.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Settings-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%20async-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-aiosqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

[![skills.sh](https://www.skills.sh/b/yerza06/tguser-cli?style=for-the-badge&logo=vercel&logoColor=%23FFFFFF&label=skills.sh&color=%23000000)](https://www.skills.sh/yerza06/tguser-cli)
![GitHub watchers](https://img.shields.io/github/watchers/yerza06/tguser-cli?style=for-the-badge&logo=github&labelColor=%23000000&color=%23FFFFFF)
![GitHub Repo stars](https://img.shields.io/github/stars/yerza06/tguser-cli?style=for-the-badge&logo=github&labelColor=%23000000&color=%23FFFFFF)

A CLI tool for sending messages to **Telegram as a user account** (MTProto protocol, not a bot) —
built for AI agents such as Hermes-Agent, OpenClaw, Claude Code, Codex CLI and the like.

An agent can write to private chats, groups and channels like a regular person, while named chat
identifiers are stored locally in SQLite (similar to `git remote`).

## Stack

Python 3.13 · [uv](https://docs.astral.sh/uv/) · [Kurigram](https://github.com/KurimuzonAkuma/pyrogram)
(a Pyrogram fork) · [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) ·
Pydantic-Settings · SQLAlchemy 2.0 (async) + aiosqlite.

## Installation

Straight from GitHub — no need to clone the repository:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
```

If you already have a clone (or want to change the code):

```bash
git clone https://github.com/yerza06/tguser-cli.git
cd tguser-cli
uv tool install .
```

The command builds the package, creates an isolated environment for it in
`~/.local/share/uv/tools/tguser/` and puts the executable into `~/.local/bin/tguser`. After that
`tguser` runs **from any directory** — no `uv run`, no need to be in the repository root. That is
exactly what AI agents need: their working directory is not known in advance.

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git --force   # update to the latest version
uv tool install . --force    # reinstall after code changes (from a clone)
uv tool install -e .         # editable mode: edits apply immediately
uv tool uninstall tguser     # remove
```

For developing the tool itself `uv sync` is enough — then you run it as `uv run tguser …` from the
project root. Details: [Installation](https://yerza06.github.io/tguser-cli/docs/installation/).

## Authentication

Get your `api_id` and `api_hash` at <https://my.telegram.org> (the _API development tools_ section),
then sign in:

```bash
tguser login            # asks for api_id/api_hash and phone number (if unset), and the code
tguser whoami           # show the current account
tguser logout           # sign out and delete the session
```

Credentials are stored in `~/.config/tguser/.env`, the session in `~/.config/tguser/tguser.session`,
and the chat database in `~/.config/tguser/tguser.db`.

> ⚠️ **Never delete `~/.config/tguser/tguser.session` or `~/.config/tguser/tguser.db`.**
> They are the tool's working state: your Telegram authorization and every saved chat name.
> They cannot be restored automatically — once deleted you have to go through `tguser login` again
> and re-add every alias by hand. To sign out, use `tguser logout` rather than deleting the file.
> More details in
> [Configuration](https://yerza06.github.io/tguser-cli/docs/configuration/#-never-delete-tgusersession-or-tguserdb).

You can also set the environment variables manually (see `.env.example`):

```bash
export TGUSER_API_ID=1234567
export TGUSER_API_HASH=0123456789abcdef0123456789abcdef
export TGUSER_PHONE_NUMBER=+15551234567   # optional: skips the phone prompt in `login`
```

## Chat management

```bash
tguser chat add work -1001234567890     # add an alias
tguser chat list                        # table of all chats (or just `tguser chat`)
tguser chat get-id work                 # print the ID
tguser chat replace-id work -100999     # replace the ID
tguser chat rename work team            # rename
tguser chat remove team                 # delete
```

## Sending

The target (`--to`) is a **saved chat name**, a numeric ID, an `@username`, or `me` (Saved Messages).
All media commands support two syntaxes — flags and positional arguments:

```bash
# Text
tguser send "Hello" --to work
tguser send "Hello" work

# Photos (several are sent as an album), with a caption
tguser sendphoto a.png b.png --to work --caption "Photos"
tguser sendphoto a.png b.png work "Photos"

# Documents (several can be grouped with -G/--group)
tguser sendfile report.pdf --to work --caption "Report"
tguser sendfile part1.pdf part2.pdf --to work --group

# Audio / video / voice / video note / sticker
tguser sendaudio track.mp3 --to me
tguser sendvideo clip.mp4 me "Clip"
tguser sendvoice voice.ogg --to me
tguser sendvideonote note.mp4 --to me
tguser sendsticker sticker.webp --to me

# Contact
tguser sendcontact --phone +77001234567 --first-name John --last-name Smith --to work
tguser sendcontact +77001234567 John Smith work
```

## Skill for AI agents

The repository ships a ready-made **Agent Skill** — a description of the tool that an agent loads by
itself as soon as a task involves Telegram. One command to install:

```bash
npx skills add https://github.com/yerza06/tguser-cli --skills tguser
```

The installer asks which agents to set the skill up for and puts it into the right directory
(`~/.claude/skills/` for Claude Code, `~/.codex/skills/` for Codex CLI, `~/.agents/skills/` for
Cline/Zed/Warp and so on). The skill follows the open
[Agent Skills](https://agentskills.io/specification) specification, so it works in any agent that
supports it.

Source: [`skills/tguser/`](skills/tguser/SKILL.md); details in
[AI Agent Integration](https://yerza06.github.io/tguser-cli/docs/ai-agents/#ready-made-skill).

> The skill cannot sign in to an account: `tguser login` is run once by a human.

## Layout

```
src/tguser/
├── cli.py            # root Typer application
├── config.py         # Pydantic-Settings
├── client.py         # Kurigram client + run_async
├── console.py        # Rich output helpers
├── resolver.py       # alias from the DB → chat_id
├── db/               # models and CRUD (SQLAlchemy async)
└── commands/         # auth / chat / send

skills/tguser/        # Agent Skill (skills.sh)
├── SKILL.md          # short instructions + frontmatter
└── references/       # full flag tables and troubleshooting

site/                 # documentation website (Hugo + Hextra → GitHub Pages)
├── hugo.yaml
└── content/          # landing page + docs, English and Russian
```

## Plans

Once the Python prototype is solid — a possible port of the CLI to Rust (Typer → clap,
Kurigram → grammers/tdlib).
