# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
- Internationalization (`src/tguser/i18n.py`): the CLI now speaks **English by default** —
  all `--help` texts, prompts, and messages. Set `TGUSER_LANG=ru` (env var or `.env`) to switch
  to Russian; unknown values fall back to English.

### Changed

- All in-code comments and docstrings translated to English.

## [0.1.0]

### Added

- Initial release of `tguser` — a CLI tool for sending Telegram messages as a user (MTProto).
- Authentication commands: `login`, `logout`, `whoami`.
- Chat alias management: `chat add/list/remove/get-id/replace-id/rename` (stored in SQLite).
- Sending commands: `send`, `sendfile`, `sendphoto`, `sendvideo`, `sendaudio`, `sendvoice`,
  `sendvideonote`, `sendsticker`, `sendcontact` — with both flag and positional syntax.
- Russian and English documentation under `docs/`.
