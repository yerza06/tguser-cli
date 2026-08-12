# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`tguser` — a Typer CLI that sends Telegram messages **as a user account (MTProto), not a bot**,
intended to be driven by AI agents. Chat aliases (`work` → `-1001234567890`) are kept locally in
SQLite, similar to `git remote`.

## Commands

```bash
uv sync                                          # install deps (Python 3.13, uv-managed)
uv run tguser --help                             # run the CLI from the source tree
uv run python -m unittest discover -s tests      # full test suite
uv run python -m unittest discover -s tests -k <pattern>   # a single test / subset

uv tool install .                                # install globally → ~/.local/bin/tguser
uv tool install . --force                        # reinstall after code changes
```

End users (and the AI agents this tool targets) are expected to install globally — the documented
path is `uv tool install git+https://github.com/yerza06/tguser-cli.git` (public repo), with
`uv tool install .` from a clone as the alternative — and to call plain `tguser` from any
directory; `uv run` is the development path only. The docs are written for the global install —
keep new examples prefix-free.

`tests/` is not a package, so dotted paths (`python -m unittest tests.test_sendfile....`) do **not**
work — always go through `discover -s tests` and narrow with `-k`.

There is no linter or formatter configured.

## Architecture

### CLI composition (`cli.py`)

Sub-apps are flattened into the root app rather than nested: `auth`, `discovery` and `send` have
their `registered_commands` extended onto `app`, so they appear as top-level commands
(`tguser login`, `tguser dialogs`, `tguser sendphoto`). Only `chat` is mounted as a real sub-typer
(`tguser chat …`). Adding a command to one of those modules automatically surfaces it top-level.

`main()` is the console-script entry point and the only place tracebacks are swallowed: `RPCError`
and any other exception become a Rich error panel + non-zero exit.

### Kurigram is imported as `pyrogram`

The dependency is `kurigram` (a Pyrogram fork), but the import name is `pyrogram`. Never add
`pyrogram` itself to the dependency list.

### Sync command → async work

Typer commands are synchronous. They build a coroutine and hand it to `run_async()`
(`client.py`, a thin `asyncio.run`). The send path is standardized in `send.py`:

`_dispatch(target_value, sender)` → `require_login()` → `_run_send()` → `init_db()` →
`resolve_target()` → open the Kurigram client → `await sender(client, target)`.

Each command only supplies the `sender` closure. Follow this shape for new send commands; it is
also what the tests hook into.

### Target resolution

`resolver.resolve_target()` looks the value up as an alias in SQLite first; if there is no match it
passes the raw value through, coercing numeric strings to `int`. So `--to` accepts an alias, a
numeric ID, `@username`, or `me` with no branching at the call site.

### Dual flag/positional syntax

Every media command accepts both `sendphoto a.png b.png --to work --caption "x"` and
`sendphoto a.png b.png work "x"`. `_split_media_args()` implements the boundary rule: leading
positional tokens that **exist on disk** are files; the first leftover is the target (unless `--to`),
the second is the caption (unless `--caption`), anything further is an error.

Because Telegram group/channel IDs are negative (`-100…`), every command that can receive an ID
positionally must pass `context_settings=ALLOW_NEG` (`{"ignore_unknown_options": True}`), otherwise
Click parses `-1001234567890` as an unknown option.

### i18n (`i18n.py`)

All user-facing text — including Typer `help=` strings — goes through `t("key")` against the
`MESSAGES` catalog (`{key: {"en": …, "ru": …}}`). English is the default; `TGUSER_LANG=ru` (env var
or `~/.config/tguser/.env`) switches. The language is resolved **once at import time** because
`help=` is evaluated while the CLI is being constructed — do not make language selection dynamic.
New strings must be added to `MESSAGES`, not inlined.

### Configuration and state

`Settings` (pydantic-settings, `TGUSER_` prefix) reads env vars and `~/.config/tguser/.env`. All
state lives in `config_dir` so the CLI works from any directory: `.env` (credentials, chmod 600),
`tguser.session`, `tguser.db`.

`db/database.py` caches the engine and sessionmaker in module-level globals and creates tables on
first `init_db()` call. There are no migrations — schema changes to `db/models.py` need to be
handled against existing user databases.

### Error reporting

Use `raise fail(message, title=...)` from `console.py` — it prints a red Rich panel and *returns*
a `typer.Exit` for the caller to raise. `success()` / `info()` are the counterparts. Commands
should not print raw exceptions or let tracebacks escape.

## Testing approach

Tests are stdlib `unittest` (`IsolatedAsyncioTestCase`), no network and no Telegram session. The
pattern in `tests/test_sendfile.py`: call the command function with `send_module._dispatch` patched,
pull the `sender` closure out of `dispatch.call_args`, then drive it with a `MagicMock` client whose
`send_*` methods are `AsyncMock`s. Use this to test send behaviour (batching, captions, album vs
single) without touching Kurigram.

## Agent skill (`skills/tguser/`)

`skills/tguser/SKILL.md` + `references/reference.md` are a **published artifact**, not internal
notes: users install them into their agent with `npx skills add yerza06/tguser-cli`, and skills.sh
serves them from the repo. Consequences:

- `name: tguser` in the frontmatter must keep matching the directory name (Agent Skills spec).
  Keep `SKILL.md` under ~500 lines; detail belongs in `references/`.
- The skill documents the *installed* CLI, so it must never reference `uv run` or a local path.
- Any change to a command, flag, or output shape means updating the skill **alongside** `docs/en/`
  and `docs/ru/` — an out-of-date skill silently misleads every agent that installed it.
- `metadata.version` in the frontmatter tracks the `pyproject.toml` version.

## Conventions

- Code, comments and docstrings are in **English**; the README, CHANGELOG and docs are bilingual.
- `docs/ru/` and `docs/en/` are parallel trees — changes to one need the matching change in the other.
- User-visible changes go in `CHANGELOG.md` under `[Unreleased]` (Keep a Changelog format).
- Git flow: `feat/*` branches → `dev` → `main`; Conventional Commits.
