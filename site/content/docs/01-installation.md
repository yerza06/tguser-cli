---
title: Installation
slug: installation
weight: 1
---

## Requirements

- **Python 3.13** (pinned in `.python-version`).
- **[uv](https://docs.astral.sh/uv/)** — the package and environment manager.
- A Telegram account and access to <https://my.telegram.org> to obtain `api_id`/`api_hash`
  (see [02. Authentication](02-authentication.md)).

## Recommended: install globally from GitHub

`tguser` is a tool, not a library: it is meant to be run from any directory — including by AI
agents, whose working directory is not known in advance. So the primary installation method is
`uv tool install` straight from the repository, with no cloning:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
```

`uv` downloads the sources, builds the package, and installs it into an isolated environment.
No copy of the repository is left behind — only the installed tool.

You can pin a specific branch or tag:

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git@dev      # branch
uv tool install git+https://github.com/yerza06/tguser-cli.git@v1.0.1   # tag
```

After that the command is available simply as `tguser` — no `uv run`, no dependency on the
repository directory:

```bash
cd ~/any/directory
tguser --version         # tguser 1.0.1
```

### What `uv tool install` does

`uv tool` is a manager for "tools" (the equivalent of `pipx`). `uv tool install`:

1. **Builds the package** from the given source — a local directory (`.` is the project root
   containing `pyproject.toml`) or a Git repository (`git+https://…`).
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
tguser --version         # tguser 1.0.1
tguser version           # version + environment (see below)
tguser --help            # tree of all commands
uv tool list             # list every tool installed through uv
```

If the `--help` output lists commands like `login`, `chat`, `send`, `sendphoto`, etc., the
installation was successful.

`tguser version` is the fuller check — besides the version it shows where the configuration lives
and whether an account is already signed in, which is the quickest way to describe your setup in a
bug report:

```console
$ tguser version
╭──────────────────────────────── Version info ────────────────────────────────╮
│     Version:  1.0.1                                                          │
│      Python:  3.13.11                                                        │
│    Kurigram:  2.2.23                                                         │
│      Config:  /home/user/.config/tguser                                      │
│     Session:  present                                                        │
│ Credentials:  set                                                            │
│    Language:  en                                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

`Session: missing` or `Credentials: not set` means the account is not signed in yet — see
[02. Authentication](02-authentication.md). The command reads only; it never creates the
configuration directory.

> If the shell answers `tguser: command not found` after installing, `~/.local/bin` is not on your
> `PATH`. Run `uv tool update-shell` and restart the terminal (see
> [07. Troubleshooting](07-troubleshooting.md)).

### Upgrading and uninstalling

```bash
# installed from GitHub — pull the latest version
uv tool install git+https://github.com/yerza06/tguser-cli.git --force

# installed from a clone — reinstall after changing the code
uv tool install . --force

uv tool uninstall tguser     # remove the tool
```

`uv tool install` copies the code at install time, so new commits (or edits in your clone) do not
reach an already-installed tool by themselves — reinstall with `--force`. For development, an
alternative is an editable install of the clone, where changes are picked up immediately without
reinstalling:

```bash
uv tool install -e .
```

## Alternative: install from a clone

If you want the sources at hand (to read the code, patch it, or run the tests):

```bash
git clone https://github.com/yerza06/tguser-cli.git
cd tguser-cli
uv tool install .        # from the project root
```

The result is the same global `tguser` command available from any directory; only the source of
the code differs.

## For development: running from the repository

If you are developing `tguser` itself and would rather not install it globally, just clone the
repository and sync the dependencies:

```bash
git clone https://github.com/yerza06/tguser-cli.git
cd tguser-cli
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
