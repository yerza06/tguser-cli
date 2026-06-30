# 07. Troubleshooting

## "No credentials" — api_id/api_hash are not set

```
✗ No credentials
api_id/api_hash are not set. Run: tguser login
```

You haven't entered api_id/api_hash yet. Run `tguser login` (it will ask for them and save them),
or set the `TGUSER_API_ID` and `TGUSER_API_HASH` variables — see [03. Configuration](03-configuration.md).

## "No session" — you need to sign in

```
✗ No session
Session not found. Sign in first: tguser login
```

The session file `~/.config/tguser/tguser.session` is missing or was deleted. Run `tguser login`.

## "No files" — the file path is wrong

```
✗ No files
No existing file was found. Check the paths.
```

Media-sending commands treat only **existing** files as content. If the first positional
argument is not a file on disk, it is interpreted as the target, leaving no content.
Make sure the file paths are correct and the files exist.

## Negative IDs for channels and groups

Telegram group and channel IDs are negative (for example, `-1001234567890`). Enter them **as-is**:

```bash
tguser chat add work -1001234567890
tguser send "Hello" --to -1001234567890
```

No escaping or `--` is needed — the tool handles such values correctly.

## "Chat … already exists" / "Chat … not found"

- For `chat add`, the alias name must be unique. If the name is taken, pick another one
  or replace the ID via `tguser chat replace-id`.
- For `chat get-id/remove/rename/replace-id`, the name must exist. Check the list:
  `tguser chat list`.

## "Extra arguments"

```
✗ Invalid arguments
Extra arguments: …
```

More positional arguments were passed than expected. As a reminder, the order for media is:
`<files…> <target> <caption>` (target and caption only if not set via the `--to`/`--caption` flags).
See [05. Sending Messages](05-sending.md).

## The command doesn't send, but there's no error

Make sure the session is valid: `tguser whoami`. If it shows an error, sign in again with
`tguser login`. For connection issues, check your internet and Telegram's availability.
