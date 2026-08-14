"""tguser — a CLI for sending Telegram messages as a user (MTProto)."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _distribution_version

try:
    # Single source of truth is [project.version] in pyproject.toml; this reads the
    # metadata of the installed distribution (uv installs the project for both
    # `uv run` and `uv tool install`).
    __version__ = _distribution_version("tguser")
except PackageNotFoundError:  # running from a source tree that was never installed
    __version__ = "0.0.0+unknown"
