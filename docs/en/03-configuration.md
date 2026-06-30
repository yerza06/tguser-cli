# 03. Configuration

`tguser` is configured through environment variables (Pydantic-Settings) with the `TGUSER_` prefix.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TGUSER_API_ID` | — | api_id from my.telegram.org |
| `TGUSER_API_HASH` | — | api_hash from my.telegram.org |
| `TGUSER_CONFIG_DIR` | `~/.config/tguser` | Directory for the session, database, and `.env` |
| `TGUSER_SESSION_NAME` | `tguser` | Session name (file name `<name>.session`) |

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

## A Separate Profile

To use a different account or an isolated database (for example, for testing), set your own directory:

```bash
export TGUSER_CONFIG_DIR=/path/to/another/profile
tguser login
```
