# 05. Sending Messages

`tguser` can send text and various media types from your account. Before sending, you must
[sign in](02-authentication.md).

## Where to Send: the Target (`--to`)

The target is the recipient. It is specified via the `--to` flag or positionally. Supported forms:

| Target type | Example |
|-------------|---------|
| Saved chat name (alias) | `--to work` |
| Numeric ID | `--to -1001234567890` |
| Username | `--to @durov` |
| Saved Messages (yourself) | `--to me` |

Aliases are configured with the `chat` command — see [04. Chat Management](04-chat-management.md).

## Two Syntaxes

All media commands accept arguments in **two ways** — pick whichever you prefer:

```bash
# via flags
tguser sendphoto a.png b.png --to work --caption "Photos"

# positionally
tguser sendphoto a.png b.png work "Photos"
```

**How positional arguments are parsed:** consecutive leading tokens that exist as files on disk
are treated as content; the next token is the target (if `--to` is not set), and the token after
it is the caption (if `--caption` is not set).

> Therefore, if a file at the given path does not exist, it will be mistaken for the target. Check your paths.

## Command Overview

| Command | What it sends | Caption (`--caption`) |
|---------|---------------|:---------------------:|
| `send` | Text message | — (extra text) |
| `sendfile` | File(s) as a document | ✓ |
| `sendphoto` | Photo (multiple → album) | ✓ |
| `sendvideo` | Video (multiple → album) | ✓ |
| `sendaudio` | Audio / music | ✓ |
| `sendvoice` | Voice message | ✓ |
| `sendvideonote` | Video note | — |
| `sendsticker` | Sticker (`.tgs`/`.webp`) | — |
| `sendcontact` | Contact | — |

## Text

```bash
tguser send "Hello!" --to work
tguser send "Hello!" work            # positionally
```

The `--caption` flag is optional for text; if set, its value is appended to the message
after a blank line:

```bash
tguser send "Title" --to me --caption "Details below"
```

## Files (Documents)

```bash
tguser sendfile report.pdf --to work --caption "Report"
tguser sendfile a.zip b.zip --to work          # multiple documents
```

## Photos

```bash
tguser sendphoto photo.png --to me --caption "Screenshot"
tguser sendphoto p1.png p2.png p3.png --to work --caption "Gallery"
```

With two or more files, photos are sent as an **album**; the caption applies to the first photo.

## Video

```bash
tguser sendvideo clip.mp4 --to me --caption "Recording"
tguser sendvideo a.mp4 b.mp4 --to work          # album
```

## Audio / Music

```bash
tguser sendaudio track.mp3 --to me --caption "Track"
tguser sendaudio one.mp3 two.mp3 --to me        # multiple tracks
```

## Voice Message

```bash
tguser sendvoice voice.ogg --to me --caption "Voice"
```

## Video Note

```bash
tguser sendvideonote note.mp4 --to me
```

## Sticker

```bash
tguser sendsticker sticker.webp --to me
```

## Contact

Send a contact (name + phone number):

```bash
# via flags
tguser sendcontact --phone +15551234567 --first-name John --last-name Doe --to work

# positionally: <phone> <first> [last] <target>
tguser sendcontact +15551234567 John Doe work
tguser sendcontact +15551234567 John work          # without a last name
```

| Flag | Description |
|------|-------------|
| `--phone` | Phone number (required) |
| `--first-name` | First name (required) |
| `--last-name` | Last name (optional) |
| `--to` | Target |

## Result

On a successful send, a panel is shown:

```
╭──────── ✓ Done ────────╮
│ Sent to work           │
╰─────────────────────────╯
```

If something goes wrong, see [07. Troubleshooting](07-troubleshooting.md).
