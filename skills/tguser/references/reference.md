# tguser — full reference

Detailed reference for the `tguser` CLI. Read this when the lean instructions in `SKILL.md`
aren't enough — for full flag tables, parsing rules, configuration, or troubleshooting.

## Table of contents

- [Global options](#global-options)
- [Version & environment](#version--environment)
- [Authentication commands](#authentication-commands)
- [Configuration & file locations](#configuration--file-locations)
- [Separate profiles](#separate-profiles)
- [Chat discovery](#chat-discovery)
- [Chat management](#chat-management)
- [Sending — flags & positional syntax](#sending--flags--positional-syntax)
- [sendcontact](#sendcontact)
- [Argument-parsing gotchas](#argument-parsing-gotchas)
- [Troubleshooting](#troubleshooting)

## Global options

| Option | Description |
|--------|-------------|
| `--version`, `-V` | Print the version and exit |
| `--install-completion` | Install shell completion |
| `--show-completion` | Print the completion script |
| `--help` | Help for any command |

## Version & environment

```bash
tguser version      # panel: version, Python, Kurigram, config path, session, credentials, language
tguser --version    # single line: `tguser 1.0.1`
```

Use `tguser version` to answer environment questions without asking the user — it reports whether
credentials are set and whether a session file exists, so it distinguishes "not installed" from
"installed but not signed in". Use `--version` when you need a parseable single line.

The command reads only: it never creates `~/.config/tguser` and never touches the network, so it is
safe to run before `login`.

## Authentication commands

```bash
tguser login        # interactive sign-in (cannot be automated by an agent)
tguser whoami       # show the active account
tguser logout       # end the session and delete the local session file
```

`login` prompts, in order, for: `api_id`/`api_hash` (only if not set yet — saved to
`~/.config/tguser/.env`), phone number in `+1…` format (only if not set — also saved to
`.env` after a successful sign-in), the SMS confirmation code, and the 2FA password
**only if enabled**. On success it prints a panel with name, username, and id.

You can pre-fill some values as flags or environment variables (the code and 2FA password are
still asked interactively):

| Flag | Environment variable | Description |
|------|----------------------|-------------|
| `--api-id` | `TGUSER_API_ID` | api_id from my.telegram.org |
| `--api-hash` | `TGUSER_API_HASH` | api_hash from my.telegram.org |
| `--phone` | `TGUSER_PHONE_NUMBER` | Phone number |

Get `api_id`/`api_hash` at <https://my.telegram.org> → **API development tools**. These are
secrets — never commit or publish them.

`logout` ends the session on Telegram's side and removes `~/.config/tguser/tguser.session`.

`whoami` prints a table with `ID`, `Name`, `Username`, `Phone`. It requires a session, which
makes it the cheapest way for an agent to check whether sending will work.

## Configuration & file locations

Configured via environment variables (Pydantic-Settings), prefix `TGUSER_`. Environment
variables take precedence over the `~/.config/tguser/.env` file.

| Variable | Default | Description |
|----------|---------|-------------|
| `TGUSER_API_ID` | — | api_id from my.telegram.org |
| `TGUSER_API_HASH` | — | api_hash from my.telegram.org |
| `TGUSER_PHONE_NUMBER` | — | Phone number for `login` (asked interactively if unset) |
| `TGUSER_CONFIG_DIR` | `~/.config/tguser` | Directory for session, database, and `.env` |
| `TGUSER_SESSION_NAME` | `tguser` | Session name (file `<name>.session`) |
| `TGUSER_LANG` | `en` | Output language: `en` or `ru`; unknown values fall back to `en` |

Files inside `TGUSER_CONFIG_DIR` (default `~/.config/tguser/`):

| File | Purpose |
|------|---------|
| `.env` | api_id/api_hash (created by `login`, permissions `0600`) |
| `tguser.session` | Kurigram session file |
| `tguser.db` | SQLite database of named chats |

Because everything lives in one config directory, `tguser` can be run from any working
directory — the session and chat database are always found.

`TGUSER_LANG` is resolved **once at process start** (it also localizes `--help` text), so it
must be set in the environment or in `.env` before the command runs.

## Separate profiles

To use a different account or an isolated database (e.g. for testing), point at another dir:

```bash
export TGUSER_CONFIG_DIR=/path/to/another/profile
tguser login
```

## Chat discovery

Both commands require an active session.

**`tguser dialogs [OPTIONS]`** — lists every chat you are a member of, with numeric IDs.
Output is a table: Chat ID, Title, Type, @username. Type is one of `private`, `bot`, `group`,
`supergroup`, `channel`. A missing username renders as `—`.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--search` | `-s` | — | Case-insensitive substring filter over title and @username |
| `--limit` | `-n` | `100` | How many dialogs to request |

**`tguser resolve QUERY`** — resolves one identifier to its numeric ID and title. Accepts
`@username`, `t.me/<name>`, an invite link `t.me/+…`, or a message link `t.me/c/<id>/<msg>`.
Prints a panel with `<title> (<type>)` and `ID: <id>`; exits 1 if the chat cannot be resolved.

Private groups and channels have no `@username`, so `resolve` cannot find them by name — use
`dialogs -s <part of the title>`, or `resolve` with an invite link.

## Chat management

| Command | Purpose |
|---------|---------|
| `tguser chat add <name> <chat_id> [--no-resolve]` | Add an alias |
| `tguser chat list` | Show all saved chats (bare `tguser chat` does the same) |
| `tguser chat get-id <name>` | Print only the ID for the name |
| `tguser chat replace-id <name> <new_id>` | Replace the stored ID |
| `tguser chat rename <old> <new>` | Rename an alias |
| `tguser chat remove <name>` | Remove an alias |

`<chat_id>` may be a numeric ID (negative for groups/channels, e.g. `-1001234567890`), a
`@username`, a `t.me/…` link, or `me` (Saved Messages). Negative IDs are entered as-is.

With an active session, a non-numeric `<chat_id>` is resolved online and stored as a numeric ID
plus the chat title. `--no-resolve` skips that and stores the raw string. Without a session the
command still works — it stores the raw value and prints a yellow warning. `chat add` is the
only chat command that does not need a session.

`chat list` shows Name, Chat ID, Title and Created. `get-id` prints the bare ID with no panel
or table, which makes it the only directly script-parseable output in the CLI.

## Sending — flags & positional syntax

Both syntaxes are equivalent:

```bash
tguser sendphoto a.png b.png --to work --caption "Photos"   # flags (preferred)
tguser sendphoto a.png b.png work "Photos"                  # positional
```

**Positional parsing:** consecutive leading tokens that exist as files on disk are content; the
next token is the target (when `--to` is absent); the token after that is the caption (when
`--caption` is absent). Because a nonexistent path is mistaken for the target, prefer flags.

Per-command behaviour with several files:

| Command | Options | Multiple files |
|---------|---------|----------------|
| `send` | `--to`, `--caption` | n/a — the caption is appended to the message after a blank line |
| `sendfile` | `--to`, `--caption`, `--group`/`-G` | Default: one document per file, caption on the first. With `-G`: albums of up to 10, caption on the very first item |
| `sendphoto` | `--to`, `--caption` | 1 file → single photo; 2+ → one album, caption on the first. No batching — more than 10 fails at the API |
| `sendvideo` | `--to`, `--caption` | Same as `sendphoto` |
| `sendaudio` | `--to`, `--caption` | Sent one at a time, caption on the first; never an album |
| `sendvoice` | `--to`, `--caption` | Only the first file is sent |
| `sendvideonote` | `--to` | Only the first file is sent |
| `sendsticker` | `--to` | Only the first file is sent; `.tgs`/`.webp` |

`-G`/`--group` is the only short option on any send command. A `-G` batch that ends up with a
single file falls back to a plain document send and loses the caption.

`~` is expanded in file paths, and paths are resolved to absolute before sending.

## sendcontact

```bash
tguser sendcontact --phone +15551234567 --first-name John --last-name Doe --to work
tguser sendcontact +15551234567 John Doe work     # positional: <phone> <first> [last] <target>
tguser sendcontact +15551234567 John work         # without a last name
```

| Flag | Description |
|------|-------------|
| `--phone` | Phone number (required) |
| `--first-name` | First name (required) |
| `--last-name` | Last name (optional) |
| `--to` | Target |

Positional quirk: the last name is only consumed when **two or more** tokens remain, so
`tguser sendcontact +15551234567 John work` correctly reads `work` as the target and leaves the
last name empty. Use flags to avoid thinking about it.

## Argument-parsing gotchas

Every send command, plus `chat add`, `chat replace-id` and `resolve`, is configured with
`ignore_unknown_options`. This is what lets you write `-1001234567890` without escaping it —
Click would otherwise read it as an unknown option.

The trade-off: **misspelled flags are not rejected on those commands.** A typo like `--capton`
is not an error; it becomes a positional token and is either swallowed as the target/caption or
reported as `Extra arguments`. If a send behaves unexpectedly, check the flag spelling first.

The commands *without* this setting — `dialogs`, `login`, `logout`, `whoami`, `chat list`,
`chat remove`, `chat get-id`, `chat rename` — do reject unknown flags normally.

Target resolution order: the value is looked up as a saved alias first; a match wins over
everything else. Otherwise the raw value is passed through, with numeric strings coerced to
integers. So naming an alias `me` would shadow Saved Messages.

## Troubleshooting

| Symptom | Cause & fix |
|---------|-------------|
| `✗ No credentials` — api_id/api_hash not set | Run `tguser login` (asks for and saves them), or set `TGUSER_API_ID`/`TGUSER_API_HASH`. |
| `✗ No session` — sign in first | `~/.config/tguser/tguser.session` is missing or deleted. Ask the user to run `tguser login` (interactive). |
| `✗ No files` — path is wrong | Media commands treat only **existing** files as content. If the first positional arg isn't a real file it's read as the target, leaving no content. Check paths; use the `--to` flag. |
| Files after the first one were ignored | The file scan stops at the first token that isn't an existing path. Everything after it is target/caption. Verify each path exists. |
| Only one voice note / sticker / video note was sent | By design — those commands send only the first file. |
| An album of 11+ photos failed | `sendphoto`/`sendvideo` do not batch. Split into groups of 10, or use `sendfile -G`. |
| Negative IDs for channels/groups | Enter them as-is (e.g. `-1001234567890`) — no escaping or `--` needed. |
| `Chat … already exists` | For `chat add`, alias names must be unique. Pick another name or use `chat replace-id`. |
| `Chat … not found` | For `get-id`/`remove`/`rename`/`replace-id`, the name must exist. Check `tguser chat list`. |
| `✗ Invalid arguments` — Extra arguments | Too many positional args, or a misspelled flag became one. Order for media: `<files…> <target> <caption>`. Prefer `--to`/`--caption`. |
| `chat add` stored `@name` instead of an ID | No active session at the time, or `--no-resolve` was passed. Sign in and use `chat replace-id`. |
| Command "succeeds" but nothing sends | Verify the session: `tguser whoami`. If it errors, re-login. Otherwise check internet / Telegram availability. |
| `tguser: command not found` | Not installed globally. Run `uv tool install git+https://github.com/yerza06/tguser-cli.git`; ensure `~/.local/bin` is on `PATH`. |
