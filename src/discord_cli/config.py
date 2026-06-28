from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    token: str
    default_guild_id: int | None
    default_channel_id: int | None
    message_fetch_limit: int


def load_settings(env_path: str | Path | None = None) -> Settings:
    if env_path is not None:
        load_dotenv(env_path, override=False)
    else:
        load_dotenv(override=False)

    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN is required. Set it in .env or environment variables.")

    return Settings(
        token=token,
        default_guild_id=_read_optional_int("DEFAULT_GUILD_ID"),
        default_channel_id=_read_optional_int("DEFAULT_CHANNEL_ID"),
        message_fetch_limit=_read_positive_int("MESSAGE_FETCH_LIMIT", default=20),
    )


def _read_optional_int(name: str) -> int | None:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return None
    return int(raw_value)


def _read_positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default

    value = int(raw_value)
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer.")
    return value
