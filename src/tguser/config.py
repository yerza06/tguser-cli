"""Application configuration via pydantic-settings.

Sources (in priority order): environment variables prefixed with ``TGUSER_`` and the
``~/.config/tguser/.env`` file. The Kurigram session and the SQLite DB live in
``config_dir`` so that ``tguser`` can be run from any directory.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "tguser"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TGUSER_",
        env_file=DEFAULT_CONFIG_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_id: int | None = None
    api_hash: str | None = None
    phone_number: str | None = None

    config_dir: Path = Field(default=DEFAULT_CONFIG_DIR)
    session_name: str = "tguser"

    @field_validator("config_dir", mode="after")
    @classmethod
    def _expand(cls, value: Path) -> Path:
        return value.expanduser()

    @property
    def db_path(self) -> Path:
        return self.config_dir / "tguser.db"

    @property
    def session_file(self) -> Path:
        return self.config_dir / f"{self.session_name}.session"

    @property
    def env_file(self) -> Path:
        return self.config_dir / ".env"

    def ensure_config_dir(self) -> None:
        """Create the config directory if it does not exist yet."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    @property
    def has_credentials(self) -> bool:
        return self.api_id is not None and bool(self.api_hash)


def get_settings() -> Settings:
    """Load settings (the config directory is created if needed)."""
    settings = Settings()
    settings.ensure_config_dir()
    return settings


def _write_env(settings: Settings, values: dict[str, str]) -> None:
    """Merge ``values`` into ``~/.config/tguser/.env`` (creates/updates the file)."""
    settings.ensure_config_dir()
    lines: dict[str, str] = {}
    if settings.env_file.exists():
        for raw in settings.env_file.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, _, val = stripped.partition("=")
            lines[key.strip()] = val.strip()

    lines.update(values)

    content = "\n".join(f"{key}={value}" for key, value in lines.items()) + "\n"
    settings.env_file.write_text(content, encoding="utf-8")
    settings.env_file.chmod(0o600)


def save_credentials(settings: Settings, api_id: int, api_hash: str) -> None:
    """Write api_id/api_hash to ``~/.config/tguser/.env``."""
    _write_env(settings, {"TGUSER_API_ID": str(api_id), "TGUSER_API_HASH": api_hash})

    # Update the in-memory settings object so we don't have to re-read.
    settings.api_id = api_id
    settings.api_hash = api_hash


def save_phone_number(settings: Settings, phone_number: str) -> None:
    """Write the phone number to ``~/.config/tguser/.env``."""
    _write_env(settings, {"TGUSER_PHONE_NUMBER": phone_number})
    settings.phone_number = phone_number
