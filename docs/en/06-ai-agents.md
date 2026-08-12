# 06. AI Agent Integration

`tguser` was built for AI agents (Hermes-Agent, OpenClaw, Claude Code, Codex CLI, etc.) from the
start: the agent runs a plain shell command and a Telegram message goes out from your user account.

## Required step: install globally

An agent runs commands from an arbitrary working directory — whichever project it is currently
working on. `uv run tguser …` is a poor fit for that: `uv run` is tied to a project, so from another
directory it resolves (and syncs) *that* project's environment, which has no `tguser` in it. The
call then fails with "command not found" — unless `tguser` is already on `PATH`, which is exactly
what a global install gives you.

So install the tool globally before wiring up any agent:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
```

The command builds the package, creates an isolated environment for it under
`~/.local/share/uv/tools/tguser/`, and places the executable at `~/.local/bin/tguser`. From then on
the agent can call `tguser` from any directory, just like `git` or `ls`. See
[01. Installation](01-installation.md) for a breakdown of what the command does.

To confirm the setup is agent-ready:

```bash
cd /tmp && tguser whoami     # should show the current account from any directory
```

## What the agent needs to know

- **The command is the same everywhere** — `tguser`, with no prefix and no `cd` into the repository.
- **State is global.** Credentials, the session, and the chat database live in `~/.config/tguser/`,
  so the result does not depend on the working directory (see
  [03. Configuration](03-configuration.md)).
- **Leave the state files alone.** `tguser.session` and `tguser.db` in `~/.config/tguser/` must
  never be deleted: the first one is your Telegram authorization, the second holds every saved chat
  name. Deleting them breaks the agent completely and requires a human (another interactive
  `tguser login`, rebuilding the aliases by hand) — see
  [03. Configuration](03-configuration.md#-never-delete-tgusersession-or-tguserdb).
- **Signing in is interactive.** `tguser login` asks for a phone number and a code — a human does
  that once. The agent only sends; no repeated login is needed.
- **Prefer chat aliases for `--to`.** A human saves the alias once
  (`tguser chat add work -1001234567890`) and the agent uses the readable `--to work` instead of a
  numeric ID (see [04. Chat Management](04-chat-management.md)).
- **Exit codes.** `0` on success, `1` on failure (including Telegram errors), `130` on interrupt.
  The error text goes to stderr, so an agent can tell a successful send from a failed one.
- **Output language.** English by default; `TGUSER_LANG=ru` switches messages to Russian.

## Typical calls

```bash
tguser send "Task finished" --to work
tguser sendfile report.pdf --to work --caption "Weekly report"
tguser sendphoto chart.png --to me
```

For the full command list and syntax, see [05. Sending Messages](05-sending.md).

> 🚧 Dedicated **skills** for specific agents (ready-made tool descriptions) will be added later.
