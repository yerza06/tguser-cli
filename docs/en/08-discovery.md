# 08. Chat Discovery (how to find an ID)

To send a message or save an alias you usually need a chat's identifier. Telegram **does not
show** the numeric ID (`-100…`) in its interface, so `tguser` helps you find it with two
commands. Both require an active session — [sign in](02-authentication.md) first.

## `tguser dialogs` — list your dialogs

Shows every chat you are a member of (private chats, groups, **private** groups and channels),
along with their numeric IDs.

```bash
tguser dialogs                 # all dialogs
tguser dialogs --search proj   # filter by title or @username
tguser dialogs --limit 50      # limit the count
```

```
                          Dialogs
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┓
┃ Chat ID        ┃ Title        ┃ Type    ┃ @username ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━┩
│ -1001234567890 │ Project Team │ channel │ —         │
│ 123456789      │ John Smith   │ private │ @john     │
└────────────────┴──────────────┴─────────┴───────────┘
```

| Option | Short | Description |
|--------|-------|-------------|
| `--search` | `-s` | Filter by substring in title or @username |
| `--limit` | `-n` | How many dialogs to request (default 100) |

## `tguser resolve` — find an ID by @username or link

```bash
tguser resolve @durov
tguser resolve "https://t.me/durov"
tguser resolve "https://t.me/+AbCdEf123456"   # private invite link
```

```
╭──────── ✓ Chat found ────────╮
│ Pavel Durov (private)        │
│ ID: 123456789               │
╰───────────────────────────────╯
```

## A private group or channel without a @username

Private chats have no public `@username`. You can still get their ID:

1. **`tguser dialogs`** — you are a **member** of such a chat, so it appears in your dialog
   list. Filter by title: `tguser dialogs -s <part of the title>` and copy the ID.
2. **Invite link** `t.me/+…` — if you have an invite link, pass it to
   `tguser resolve "https://t.me/+…"`.

## Saving a discovered chat

Once you have the ID, save it under a name (see [04. Chat Management](04-chat-management.md)):

```bash
tguser chat add team -1001234567890
```

Or pass a `@username` or link straight to `chat add` — with an active session the ID and title
are resolved automatically:

```bash
tguser chat add news @somechannel
```
