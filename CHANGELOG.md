# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`TGUSER_PHONE_NUMBER`** — the phone number is now a regular setting alongside `TGUSER_API_ID`
  and `TGUSER_API_HASH`. `tguser login` takes it from `--phone`, then the environment (or
  `~/.config/tguser/.env`), and only asks interactively as a last resort. A number entered at the
  prompt is saved to `~/.config/tguser/.env` (mode 600) after a successful sign-in, so repeated
  logins no longer ask for it.

- **Documentation website** at <https://yerza06.github.io/tguser-cli/> — a landing page plus the
  full English and Russian documentation, with full-text search, a language switcher and a dark
  theme. Built with Hugo and the Hextra theme from `site/`, and deployed to GitHub Pages by
  `.github/workflows/pages.yml` on every push to `main`.

- The root `README.md` is now in **English** and carries a `for-the-badge` shields.io badge row
  (Python, uv, Telegram/MTProto, MIT, Typer, Rich, Pydantic, SQLAlchemy, SQLite) next to the
  existing skills.sh badge; the Russian version moved to `README-ru.md` with the same badges, and
  both files link to each other at the top. `docs/ru/README.md` now points at `README-ru.md`.

- **Agent Skill** in `skills/tguser/` following the open
  [Agent Skills](https://agentskills.io/specification) specification, so AI agents (Claude Code,
  Codex CLI, Cursor, OpenCode, OpenClaw, Cline, Zed, Warp and others) can be taught the tool with
  a single `npx skills add https://github.com/yerza06/tguser-cli --skills tguser`. `SKILL.md` holds
  the short instructions — install check, the interactive-login gate, targets, the send commands,
  output and exit codes — and
  `references/reference.md` the full flag tables, parsing rules, configuration and troubleshooting.
- `skills.sh.json` describing how the repository page is grouped on skills.sh.
- `LICENSE` (MIT) and matching `license`/`license-files` metadata in `pyproject.toml`; the project
  was previously unlicensed.
- Documentation: a "Ready-made skill" section in `06-ai-agents.md` (RU/EN) with the install
  command and the per-agent skill directories, replacing the placeholder note that skills would
  come later; the root README gained a skill section and skills.sh/license badges.
- `sendfile -G/--group` option for sending documents as albums, automatically split into
  groups of up to 10 files.
- `tguser dialogs` command — lists all dialogs you are a member of (private chats, groups,
  private groups and channels) with their numeric IDs. Supports `--search/-s` (filter by title
  or `@username`) and `--limit/-n`.
- `tguser resolve <query>` command — resolves a `@username`, `t.me/…` link, or private invite
  link `t.me/+…` to its numeric chat ID and title.
- Automatic resolution in `tguser chat add`: passing a `@username` or link with an active
  session now stores the resolved numeric ID and title; add `--no-resolve` to store the value
  as-is. Without a session it falls back to storing the raw value with a warning.
- `src/tguser/discover.py` module with `resolve_online()` and `fetch_dialogs()` online helpers.
- Documentation: new section `08-discovery.md` (RU/EN) explaining how to find a chat ID,
  including private chats without a `@username`.
- Documentation: installing straight from GitHub with
  `uv tool install git+https://github.com/yerza06/tguser-cli.git` (branch/tag pinning included) is
  now the primary path in `01-installation.md` (RU/EN), the READMEs, `06-ai-agents.md` and
  `07-troubleshooting.md`; installing from a clone is kept as the alternative.
- `[project.urls]` in `pyproject.toml` pointing at the public repository.
- Documentation: warnings that `~/.config/tguser/tguser.session` and `~/.config/tguser/tguser.db`
  must never be deleted (root README, docs indexes, `02-authentication.md`,
  `04-chat-management.md`, `06-ai-agents.md`), with a full explanation in `03-configuration.md`
  (RU/EN) — what each file stores, why it is needed, what breaks if it is removed, and how to back
  the directory up — plus a recovery entry in `07-troubleshooting.md`.
- Internationalization (`src/tguser/i18n.py`): the CLI now speaks **English by default** —
  all `--help` texts, prompts, and messages. Set `TGUSER_LANG=ru` (env var or `.env`) to switch
  to Russian; unknown values fall back to English.

### Changed

- **Documentation moved** from `docs/en/` and `docs/ru/` into `site/content/docs/`, where the two
  languages now sit side by side as `05-sending.md` and `05-sending.ru.md`. The pages are published
  under clean URLs (`/docs/sending/`); the filenames keep their numeric prefixes so the existing
  relative cross-links keep resolving. Links to `docs/**` in the READMEs now point at the website.
- Documentation now recommends installing globally with `uv tool install .` instead of running
  through `uv run` from the repository: `01-installation.md` (RU/EN) explains what the command does
  (isolated environment in `~/.local/share/uv/tools/`, executable in `~/.local/bin/`), how to
  reinstall (`--force`), and the editable variant (`-e`); `uv sync` + `uv run` is kept as the
  development workflow.
- `06-ai-agents.md` (RU/EN) filled in: why agents need a global install (arbitrary working
  directory), global state in `~/.config/tguser/`, exit codes, and typical calls.
- `07-troubleshooting.md` (RU/EN): new entries for `tguser: command not found` (PATH /
  `uv tool update-shell`) and for code changes not taking effect after `uv tool install`.
- All in-code comments and docstrings translated to English.

## [0.1.0]

### Added

- Initial release of `tguser` — a CLI tool for sending Telegram messages as a user (MTProto).
- Authentication commands: `login`, `logout`, `whoami`.
- Chat alias management: `chat add/list/remove/get-id/replace-id/rename` (stored in SQLite).
- Sending commands: `send`, `sendfile`, `sendphoto`, `sendvideo`, `sendaudio`, `sendvoice`,
  `sendvideonote`, `sendsticker`, `sendcontact` — with both flag and positional syntax.
- Russian and English documentation under `docs/`.
