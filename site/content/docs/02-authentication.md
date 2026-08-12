---
title: Authentication
slug: authentication
weight: 2
---

To send messages as a user, you need to sign in to your account once. `tguser` uses MTProto
via Kurigram, so `api_id` and `api_hash` are required.

## Step 1. Get api_id and api_hash

1. Open <https://my.telegram.org> and log in with your phone number.
2. Go to the **API development tools** section.
3. Create an application (any title and description will do).
4. Copy the **api_id** (a number) and **api_hash** (a string).

> These are secrets. Do not publish them or commit them to a repository.

## Step 2. Sign In

```bash
tguser login
```

The command will prompt you, in order, for:

- `api_id` and `api_hash` — if they are not set yet (they will be saved to `~/.config/tguser/.env`);
- your phone number in `+1…` format;
- the confirmation code from Telegram;
- your two-factor authentication password — **only if it is enabled**.

On success, a panel with the account's name, username, and id is shown.

### Passing Parameters Up Front

You can provide values as flags to avoid entering them interactively:

```bash
tguser login --api-id 1234567 --api-hash 0123456789abcdef0123456789abcdef --phone +15551234567
```

| Flag | Description |
|------|-------------|
| `--api-id` | api_id from my.telegram.org |
| `--api-hash` | api_hash from my.telegram.org |
| `--phone` | Phone number |

The confirmation code and 2FA password are still requested interactively.

## Check the Current Account

```bash
tguser whoami
```

Prints a table: ID, name, username, phone.

## Sign Out

```bash
tguser logout
```

Ends the session on Telegram's side and removes the local session file
`~/.config/tguser/tguser.session`.

## Where the Session Is Stored

After signing in, a session file `~/.config/tguser/tguser.session` is created. As long as it
exists and is valid, you don't need to `login` again — the sending commands work right away.

> ⚠️ **Never delete this file.** It stores your Telegram authorization key; without it every
> command stops working and you have to go through the interactive `tguser login` again (phone,
> code, cloud password). To sign out, use `tguser logout` — it properly terminates the session on
> Telegram's side and removes the file itself. The same applies to the chat database
> `~/.config/tguser/tguser.db`. Both files are explained in
> [03. Configuration](03-configuration.md#-never-delete-tgusersession-or-tguserdb).

For more on file locations and variables, see [03. Configuration](03-configuration.md).
