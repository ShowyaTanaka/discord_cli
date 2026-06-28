from __future__ import annotations

from pathlib import Path

import pytest

from discord_cli.config import load_settings


def test_load_settings_reads_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("DISCORD_BOT_TOKEN", "DEFAULT_GUILD_ID", "DEFAULT_CHANNEL_ID", "MESSAGE_FETCH_LIMIT"):
        monkeypatch.delenv(key, raising=False)

    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "DISCORD_BOT_TOKEN=token",
                "DEFAULT_GUILD_ID=10",
                "DEFAULT_CHANNEL_ID=20",
                "MESSAGE_FETCH_LIMIT=30",
            ]
        ),
        encoding="utf-8",
    )

    settings = load_settings(env_path=env_path)

    assert settings.token == "token"
    assert settings.default_guild_id == 10
    assert settings.default_channel_id == 20
    assert settings.message_fetch_limit == 30


def test_load_settings_requires_token(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("DISCORD_BOT_TOKEN", "DEFAULT_GUILD_ID", "DEFAULT_CHANNEL_ID", "MESSAGE_FETCH_LIMIT"):
        monkeypatch.delenv(key, raising=False)

    env_path = tmp_path / ".env"
    env_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="DISCORD_BOT_TOKEN is required"):
        load_settings(env_path=env_path)


def test_load_settings_rejects_non_positive_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("DISCORD_BOT_TOKEN", "DEFAULT_GUILD_ID", "DEFAULT_CHANNEL_ID", "MESSAGE_FETCH_LIMIT"):
        monkeypatch.delenv(key, raising=False)

    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "DISCORD_BOT_TOKEN=token",
                "MESSAGE_FETCH_LIMIT=0",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="MESSAGE_FETCH_LIMIT must be a positive integer."):
        load_settings(env_path=env_path)
