---
name: tguser
description: >-
  Send Telegram messages, files, photos, videos, voice notes and contacts AS A USER
  (MTProto, not a bot) via the `tguser` CLI, and manage saved chat aliases. Use whenever
  the user wants to deliver something to Telegram — "send a Telegram message", "notify me
  on Telegram", "message X on Telegram", "post this to my channel or group", "send this
  file/photo to Telegram", "ping my saved messages" — including the Russian equivalents
  ("отправь в телеграм", "напиши в телеграм", "уведоми в телеграм", "скинь файл в телеграм").
  Also covers finding a chat's numeric ID (`dialogs`, `resolve`) and saving chats under short
  names. Trigger even when the user does not say "tguser" explicitly but clearly wants to send
  or post something to Telegram from this machine.
license: MIT
compatibility: Requires Python 3.13+, uv, and a one-time interactive Telegram login by a human.
metadata:
  author: yerza06
  version: "0.1.0"
---

# tguser — send Telegram messages as a user

`tguser` sends messages and media to Telegram **from a real user account** (MTProto via
Kurigram), not from a bot. Chats can be saved under short names in a local SQLite database,
like `git remote`.

Source: <https://github.com/yerza06/tguser-cli>

## 1. Check the tool is installed

```bash
command -v tguser
```

If that prints nothing, install it globally:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
```

Install **globally**, never `uv run tguser`. `uv run` resolves the environment of whatever
project the current directory belongs to, so it fails from anywhere except the tguser repo
itself. A global install puts the binary at `~/.local/bin/tguser` and it works from any
directory, like `git`.

## 2. Check the session before sending

```bash
tguser whoami
```

Exit code 0 means a working session; it prints a table with ID, name, username and phone.

If it fails with **`✗ No session`** or **`✗ No credentials`**, the account is not signed in.
**Do not try to sign in yourself.** `tguser login` is interactive — it prompts for a phone
number, an SMS code, and possibly a 2FA password, none of which an agent can supply. Stop and
ask the user to run it:

```bash
tguser login
```

(In Claude Code the user can run it inline by typing `! tguser login`.)

Signing in is a one-time human step. Afterwards the session at
`~/.config/tguser/tguser.session` persists and every send works unattended.

## 3. Pick a target

Every send needs a recipient, passed as `--to`:

| Form | Example | Notes |
|------|---------|-------|
| Saved alias | `--to work` | Created with `tguser chat add`; checked first |
| Numeric ID | `--to -1001234567890` | Groups/channels are negative — type the `-` as-is, no escaping |
| Username | `--to @durov` | |
| Yourself | `--to me` | Saved Messages — the right target for notifications and for testing |

Use `--to me` for self-notifications and to verify things work without messaging anyone else.

**Don't know the ID?** See [Finding a chat](#finding-a-chat) below.

## 4. Send

### Always use flags, not positional arguments

Media commands also accept a positional form (`tguser sendphoto a.png work "caption"`), but the
parser decides where the file list ends by testing **whether each token exists on disk**, and it
stops at the first token that does not. A typo'd or missing path is therefore silently
reinterpreted as the *recipient* — the message goes to the wrong place or fails with a confusing
"No files" error.

So always pass `--to` (and `--caption` where relevant) explicitly, and confirm media files exist
before sending:

```bash
tguser send "Build finished ✅" --to me
tguser sendphoto ./out/chart.png --to work --caption "Latest chart"
tguser sendfile ./report.pdf --to work --caption "Q4 report"
```

### Commands

| Command | Sends | `--caption` | Multiple files |
|---------|-------|:-----------:|----------------|
| `send "text"` | Text message | ✓ (appended after a blank line) | — |
| `sendfile FILES…` | Document(s) | ✓ | Each sent separately; `-G`/`--group` makes albums, auto-split into batches of 10 |
| `sendphoto FILES…` | Photo | ✓ | 2+ → one album, caption on the first. **Max 10** — more fails at the API |
| `sendvideo FILES…` | Video | ✓ | 2+ → one album, caption on the first. **Max 10** |
| `sendaudio FILES…` | Audio / music | ✓ | Sent one by one, caption on the first — never an album |
| `sendvoice FILE` | Voice message | ✓ | **Only the first file** is sent; extras are ignored |
| `sendvideonote FILE` | Round video note | — | **Only the first file** |
| `sendsticker FILE` | Sticker (`.tgs`/`.webp`) | — | **Only the first file** |
| `sendcontact` | Contact | — | `--phone`, `--first-name`, optional `--last-name` |

Examples:

```bash
tguser send "Hello!" --to @durov
tguser sendphoto a.png b.png c.png --to work --caption "Gallery"
tguser sendfile *.log --to work --group --caption "Today's logs"
tguser sendaudio track.mp3 --to me --caption "New track"
tguser sendcontact --phone +15551234567 --first-name John --last-name Doe --to work
```

## Output and exit codes

**Read this before parsing anything.** `tguser` has **no `--json`, `--quiet` or `--verbose`
mode**. All output is human-oriented Rich formatting:

- Success → a green bordered panel (`✓ Done`, `✓ Sent to <target>`) on **stdout**.
- Errors → a red bordered panel (`✗ No session`, `✗ No files`, `✗ Could not send`, …) on
  **stderr**.
- `whoami`, `chat list` and `dialogs` print box-drawing tables on stdout.

| Exit code | Meaning |
|-----------|---------|
| `0` | Success |
| `1` | Failure — bad arguments, no session, or a Telegram error |
| `130` | Interrupted (Ctrl-C) |

**Branch on the exit code, never on the text.** Message text is localized (English by default,
Russian when `TGUSER_LANG=ru`) and Rich wraps and truncates it to the terminal width, so string
matching is unreliable.

The one exception is `tguser chat get-id <name>`, which prints the bare ID and nothing else —
use it when a script needs a value:

```bash
CHAT_ID=$(tguser chat get-id work)
```

## Saved chat aliases

Save any chat you will reuse under a short name, so raw IDs never need to be pasted again:

```bash
tguser chat add work -1001234567890     # save an alias
tguser chat add news @somechannel       # @username/link → resolved to ID + title when signed in
tguser chat list                        # table of saved chats (bare `tguser chat` does the same)
tguser chat get-id work                 # print just the ID
tguser chat replace-id work -100999     # point the alias at a different chat
tguser chat rename work team            # rename
tguser chat remove team                 # delete
```

`chat add` accepts a numeric ID, `@username`, a `t.me/…` link, or `me`. With an active session a
non-numeric value is resolved online to its numeric ID and title; add `--no-resolve` to store the
raw value instead. Without a session it stores the raw value and prints a warning.

Alias names must be unique. `get-id`, `remove`, `rename` and `replace-id` require an existing
name — check `tguser chat list` first.

## Finding a chat

Telegram's UI does not show numeric IDs. Two commands find them (both need an active session):

```bash
tguser dialogs                  # every chat you are in, with IDs
tguser dialogs -s proj          # filter by title or @username
tguser dialogs -n 50            # how many dialogs to request (default 100)

tguser resolve @durov
tguser resolve "https://t.me/durov"
tguser resolve "https://t.me/+AbCdEf123456"    # private invite link
```

`dialogs` is the way to reach a **private** group or channel: it has no `@username`, but you are
a member, so it appears in the list. Filter by title and copy the ID.

Then save it: `tguser chat add team -1001234567890`.

## Don't touch the state files

Everything lives in `~/.config/tguser/`: `.env` (credentials, mode 600), `tguser.session`
(the Telegram authorization) and `tguser.db` (saved aliases). **Never delete or move them.**
Losing the session forces another interactive login by the user; losing the database loses every
saved alias. Neither can be restored by an agent.

## More detail

Full flag tables, the exact positional-parsing rules, configuration variables, separate
profiles, and a troubleshooting table: [`references/reference.md`](references/reference.md).
