# 01. Installation

## Requirements

- **Python 3.13** (pinned in `.python-version`).
- **[uv](https://docs.astral.sh/uv/)** — the package and environment manager.
- A Telegram account and access to <https://my.telegram.org> to obtain `api_id`/`api_hash`
  (see [02. Authentication](02-authentication.md)).

## Recommended: install globally

`tguser` is a tool, not a library: it is meant to be run from any directory — including by AI
agents, whose working directory is not known in advance. So the primary installation method is
`uv tool install`:

```bash
uv tool install .        # from the project root
```

After that the command is available simply as `tguser` — no `uv run`, no dependency on the
repository directory:

```bash
cd ~/any/directory
tguser --version         # tguser 0.1.0
```

### What `uv tool install .` does

`uv tool` is a manager for "tools" (the equivalent of `pipx`). `uv tool install .`:

1. **Builds the package** from the current directory (`.` is the project root containing
   `pyproject.toml`).
2. **Creates a dedicated isolated environment** for `tguser` under
   `~/.local/share/uv/tools/tguser/`. Its dependencies (Kurigram, Typer, SQLAlchemy, …) are
   installed there and do not mix with the system Python or with other projects' environments.
3. **Places the `tguser` executable** in `~/.local/bin/`. The executable comes from the
   `[project.scripts]` section of `pyproject.toml` (`tguser = "tguser.cli:main"`).
4. Because `~/.local/bin` is on your `PATH`, the `tguser` command works from **any** directory.

Note that the isolation applies to code and dependencies only. Your data — the `.env` with
`api_id`/`api_hash`, the session file, and the chat database — lives in `~/.config/tguser/` and is
**shared** across every way of running the tool (see [03. Configuration](03-configuration.md)).
So if you already signed in via `uv run tguser login`, you do not need to sign in again after
`uv tool install`.

### Verifying the installation

```bash
which tguser             # /home/<user>/.local/bin/tguser
tguser --version         # tguser 0.1.0
tguser --help            # tree of all commands
uv tool list             # list every tool installed through uv
```

If the `--help` output lists commands like `login`, `chat`, `send`, `sendphoto`, etc., the
installation was successful.

> If the shell answers `tguser: command not found` after installing, `~/.local/bin` is not on your
> `PATH`. Run `uv tool update-shell` and restart the terminal (see
> [07. Troubleshooting](07-troubleshooting.md)).

### Upgrading and uninstalling

```bash
uv tool install . --force    # reinstall after changing the code
uv tool uninstall tguser     # remove the tool
```

`uv tool install .` copies the code at install time, so after editing the repository you have to
reinstall with `--force`. For development, an alternative is an editable install, where changes are
picked up immediately without reinstalling:

```bash
uv tool install -e .
```

## Alternative: running from the repository

If you are developing `tguser` itself and would rather not install it globally, just sync the
dependencies:

```bash
uv sync
```

This creates a `.venv/` virtual environment, installs all dependencies from `pyproject.toml`, and
installs the `tguser` package itself in editable mode. Run it with the `uv run` prefix, and **only
from inside the repository** (the root or a subdirectory of it):

```bash
uv run tguser <command> [arguments]
```

Throughout the rest of the documentation, commands are written simply as `tguser …`, assuming a
global installation.

## Next Steps

Continue to [02. Authentication](02-authentication.md) to sign in to your Telegram account.
