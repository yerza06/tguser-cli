# 04. Chat Management

The `chat` command manages **named identifiers** for chats, groups, and channels — similar to
`git remote`. Instead of specifying a numeric ID like `-1001234567890` every time, you save it
under a friendly name (an alias) and use that name in `--to`.

Identifiers are stored in the SQLite database `~/.config/tguser/tguser.db`.

## Subcommand Overview

| Command | Purpose |
|---------|---------|
| `tguser chat add <name> <chat_id>` | Add an alias |
| `tguser chat list` | Show all saved chats |
| `tguser chat get-id <name>` | Print the ID by name |
| `tguser chat replace-id <name> <new_id>` | Replace the ID |
| `tguser chat rename <old> <new>` | Rename an alias |
| `tguser chat remove <name>` | Remove an alias |

> `tguser chat` with no subcommand is equivalent to `tguser chat list`.

## Add a Chat

```bash
tguser chat add work -1001234567890
```

```
╭────────────── ✓ Done ──────────────╮
│ Added chat work → -1001234567890   │
╰─────────────────────────────────────╯
```

As `chat_id` you can store:

- a numeric ID (negative for groups/channels, e.g. `-1001234567890`);
- a `@username` (e.g. `@durov`);
- `me` — Saved Messages.

> Negative IDs are entered as-is — no escaping is needed.

### Automatic resolution of @username and links

If you pass a `@username` or a link (`t.me/…`, invite link `t.me/+…`) with an active session,
`tguser` resolves the numeric ID and title for you and stores those:

```bash
tguser chat add news @somechannel
# Added chat news → -1001234567890 (Some Channel)
```

To skip resolution and store the value as-is, add `--no-resolve`:

```bash
tguser chat add news @somechannel --no-resolve
```

> Don't know the ID or `@username`? See [08. Chat Discovery](08-discovery.md) —
> the `dialogs` and `resolve` commands help you find an ID, including for private chats.

## List Chats

```bash
tguser chat list      # or simply: tguser chat
```

```
                 Saved chats
┏━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Name ┃ Chat ID        ┃ Title  ┃ Created          ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ work │ -1001234567890 │ —      │ 2026-06-30 11:20 │
└──────┴────────────────┴────────┴──────────────────┘
```

## Get an ID by Name

```bash
tguser chat get-id work
# -1001234567890
```

Handy for scripts: the command prints only the ID itself.

## Replace an ID

```bash
tguser chat replace-id work -100999
```

## Rename

```bash
tguser chat rename work team
```

## Remove

```bash
tguser chat remove team
```

## Next

How to use saved names when sending is covered in [05. Sending Messages](05-sending.md).
