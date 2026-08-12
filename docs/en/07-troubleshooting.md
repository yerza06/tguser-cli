# 07. Troubleshooting

## `tguser: command not found`

Either the tool is not installed globally, or the directory holding its executable is not on your
`PATH`.

1. Install it: `uv tool install git+https://github.com/yerza06/tguser-cli.git`
   (or `uv tool install .` from the root of a clone — see [01. Installation](01-installation.md)).
2. Check that it registered: `uv tool list` should include `tguser`.
3. If it is installed but the command still isn't found, `~/.local/bin` is missing from `PATH`.
   Add it with `uv tool update-shell`, then restart the terminal.

To verify: `which tguser` should print a path like `/home/<user>/.local/bin/tguser`.

## Code changes don't take effect / outdated version

`uv tool install` copies the code at install time, so new commits on GitHub and edits in a local
clone do not affect an already installed tool. Reinstall it:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git --force   # installed from GitHub
uv tool install . --force                                              # installed from a clone
```

Or install a clone in editable mode (`uv tool install -e .`), where changes are picked up
immediately.

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

## `tguser.session` or `tguser.db` was deleted

These files must not be deleted — they hold the entire state of the tool, and there is no automatic
recovery (see
[03. Configuration](03-configuration.md#-never-delete-tgusersession-or-tguserdb) for what each file
does). If one is already gone:

- **`tguser.session`** — your authorization is lost. Run `tguser login` again: you will need your
  phone number, the code from Telegram, and your cloud password if two-factor authentication is on.
  The old session stays in your account's active devices — terminate it manually in the Telegram
  app (*Settings → Devices*).
- **`tguser.db`** — every alias is lost. The database is recreated empty and the chat names have to
  be added by hand. Use `tguser dialogs` and `tguser resolve` to find the IDs (see
  [08. Chat Discovery](08-discovery.md)), then `tguser chat add <name> <id>`.

If you have a backup of the directory, just copy the files back into `~/.config/tguser/` while
`tguser` is not running.

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
