from __future__ import annotations

import pytest

from discord_cli.config import load_settings


def test_load_settings_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "token")
    monkeypatch.setenv("DEFAULT_GUILD_ID", "10")
    monkeypatch.setenv("DEFAULT_CHANNEL_ID", "20")
    monkeypatch.setenv("MESSAGE_FETCH_LIMIT", "30")

    settings = load_settings()

    assert settings.token == "token"
    assert settings.default_guild_id == 10
    assert settings.default_channel_id == 20
    assert settings.message_fetch_limit == 30


def test_load_settings_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DISCORD_BOT_TOKEN", raising=False)

    with pytest.raises(ValueError, match="DISCORD_BOT_TOKEN is required"):
        load_settings()


def test_load_settings_rejects_non_positive_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "token")
    monkeypatch.setenv("MESSAGE_FETCH_LIMIT", "0")

    with pytest.raises(ValueError, match="MESSAGE_FETCH_LIMIT must be a positive integer."):
        load_settings()
