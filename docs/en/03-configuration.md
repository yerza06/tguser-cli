# 03. Configuration

`tguser` is configured through environment variables (Pydantic-Settings) with the `TGUSER_` prefix.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TGUSER_API_ID` | — | api_id from my.telegram.org |
| `TGUSER_API_HASH` | — | api_hash from my.telegram.org |
| `TGUSER_CONFIG_DIR` | `~/.config/tguser` | Directory for the session, database, and `.env` |
| `TGUSER_SESSION_NAME` | `tguser` | Session name (file name `<name>.session`) |
| `TGUSER_LANG` | `en` | CLI output language: `en` or `ru` |

## Interface Language

By default the CLI (`--help`, messages, errors) is shown **in English**. To switch to
Russian, set `TGUSER_LANG=ru` — via an environment variable or in `.env`:

```bash
export TGUSER_LANG=ru
tguser --help          # help in Russian
```

> An unknown value falls back to English.

## Settings Sources and Priority

Settings are read from two sources (environment variables take precedence):

1. **Environment variables** `TGUSER_*`.
2. **The file** `~/.config/tguser/.env`.

Example `.env` (see also `.env.example` in the project root):

```dotenv
TGUSER_API_ID=1234567
TGUSER_API_HASH=0123456789abcdef0123456789abcdef
# TGUSER_CONFIG_DIR=~/.config/tguser
# TGUSER_SESSION_NAME=tguser
```

## File Locations

All working files live in `TGUSER_CONFIG_DIR` (by default `~/.config/tguser/`):

| File | Purpose |
|------|---------|
| `.env` | api_id/api_hash (created by `login`, permissions `0600`) |
| `tguser.session` | Kurigram session file |
| `tguser.db` | SQLite database with named chats |

Thanks to the single configuration directory, you can run `tguser` from any directory —
the session and chat database are always in the same place.

## ⚠️ Never delete `tguser.session` or `tguser.db`

These files are the **working state of the tool**, not a cache and not temporary files. `tguser`
keeps no duplicates of them, makes no backups, and cannot restore them for you. Do not delete them,
do not move them around by hand, and do not "clean up" `~/.config/tguser/` just in case.

### `tguser.session` — the Telegram session file

**What it is.** A Kurigram SQLite file created by `tguser login`. It holds the authorization key
(auth key) issued by Telegram after you entered your phone number and the code, the data center
number, and a cache of known chats (the peer cache). This file is what makes you an authorized
user: without it the library cannot connect to Telegram on your behalf.

**Why it matters.** As long as the file exists and is valid, you never have to sign in again —
`tguser send`, `sendphoto`, and the rest work immediately, with no phone number and no code. That
is essential for an AI agent: it cannot go through interactive authentication on its own.

**What happens if you delete it.** Every command that needs a connection (`send*`, `whoami`,
`dialogs`, `resolve`) fails with "no active session". You have to run `tguser login` again and
enter your phone number, the code from Telegram, and — if two-factor authentication is on — your
cloud password, which means a human has to be present. Your messages and chats are not lost; they
live on Telegram's servers.

One more thing: deleting the file does **not** end the session on Telegram's side — it stays in
your account's list of active devices, you just can no longer control it from the CLI. The proper
way to sign out is `tguser logout`: it terminates the session on the server first and removes the
file afterwards.

### `tguser.db` — the named-chat database

**What it is.** A SQLite database with a single `chats` table: the alias name, the chat identifier
(`-100…`, `@username`, or `me`), the chat title, and the creation timestamp. It is populated by
`tguser chat add`.

**Why it matters.** This is your address book — it lets you write `--to work` instead of
`--to -1001234567890`. Scripts and AI agent prompts are built around it: the agent's instructions
carry a readable chat name, not a numeric ID.

**What happens if you delete it.** The file is recreated on the next run — but **empty**. Every
saved alias is gone, and a command like `tguser send "text" --to work` will treat `work` as a raw
identifier and fail. The address book cannot be restored automatically: Telegram does not store
your local names. You have to look the IDs up again (`tguser dialogs`, `tguser resolve`) and re-add
the aliases by hand — and until you do, every script and agent that referenced those names is
broken.

### Backups

Copying the whole configuration directory is enough — it also contains the `.env` with your
`api_id`/`api_hash`:

```bash
cp -r ~/.config/tguser ~/backup/tguser-config
```

Make the copy while `tguser` is not running, and keep it somewhere safe: the session file and the
`.env` together give full access to your Telegram account. To restore, copy the files back into
`~/.config/tguser/`.

If you need to try something in isolation, leave the main directory alone and set up a separate
profile via `TGUSER_CONFIG_DIR` (see below).

## A Separate Profile

To use a different account or an isolated database (for example, for testing), set your own directory:

```bash
export TGUSER_CONFIG_DIR=/path/to/another/profile
tguser login
```
