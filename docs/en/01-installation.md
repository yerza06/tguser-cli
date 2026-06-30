# 01. Installation

## Requirements

- **Python 3.13** (pinned in `.python-version`).
- **[uv](https://docs.astral.sh/uv/)** — the package and environment manager.
- A Telegram account and access to <https://my.telegram.org> to obtain `api_id`/`api_hash`
  (see [02. Authentication](02-authentication.md)).

## Installing Dependencies

From the project root:

```bash
uv sync
```

This creates a `.venv/` virtual environment, installs all dependencies from `pyproject.toml`,
and installs the `tguser` package itself in editable mode.

## Verifying the Installation

```bash
uv run tguser --version      # tguser 0.1.0
uv run tguser --help         # tree of all commands
```

If the `--help` output lists commands like `login`, `chat`, `send`, `sendphoto`, etc., the
installation was successful.

## Running a Command

Throughout this documentation, commands are written as `tguser …`. When running from the
repository, prefix them with `uv run`:

```bash
uv run tguser <command> [arguments]
```

> To call `tguser` directly without `uv run`, install the tool globally, for example via
> `uv tool install .` from the project root.

## Next Steps

Continue to [02. Authentication](02-authentication.md) to sign in to your Telegram account.
