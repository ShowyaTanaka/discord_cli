from __future__ import annotations

import json

from discord_cli.models import AuthorSummary, ChannelSummary, GuildSummary, MessageSummary
from discord_cli.presentation_model.factory import (
    build_channel_list_response,
    build_guild_list_response,
    build_message_list_response,
    build_message_response,
)
from discord_cli.presentation_model.serializer import to_json


def test_build_guild_list_response_to_json() -> None:
    response = build_guild_list_response([GuildSummary(guild_id=1, name="test", owner_id=2, member_count=3)])

    rendered = json.loads(to_json(response))

    assert rendered == {
        "guilds": [
            {
                "guild_id": 1,
                "name": "test",
                "owner_id": 2,
                "member_count": 3,
            }
        ]
    }


def test_build_channel_list_response_to_json() -> None:
    response = build_channel_list_response(
        10,
        [ChannelSummary(channel_id=1, name="general", channel_type="text", category_id=None, position=0)],
    )

    rendered = json.loads(to_json(response))

    assert rendered == {
        "guild_id": 10,
        "channels": [
            {
                "channel_id": 1,
                "name": "general",
                "channel_type": "text",
                "category_id": None,
                "position": 0,
            }
        ],
    }


def test_build_message_list_response_to_json() -> None:
    response = build_message_list_response(
        2,
        [
            MessageSummary(
                message_id=1,
                channel_id=2,
                author=AuthorSummary(
                    author_id=3,
                    author_name="alice",
                    global_name="Alice",
                    bot=False,
                    discriminator="1234",
                    avatar_url="https://cdn.example/avatar.png",
                ),
                created_at="2026-06-28T00:00:00+00:00",
                edited_at=None,
                content="hello\nworld",
                jump_url="https://discord.com/channels/1/2/3",
            )
        ],
    )

    rendered = json.loads(to_json(response))

    assert rendered == {
        "channel_id": 2,
        "messages": [
            {
                "message_id": 1,
                "channel_id": 2,
                "author": {
                    "author_id": 3,
                    "author_name": "alice",
                    "global_name": "Alice",
                    "bot": False,
                    "discriminator": "1234",
                    "avatar_url": "https://cdn.example/avatar.png",
                },
                "created_at": "2026-06-28T00:00:00+00:00",
                "edited_at": None,
                "content": "hello\nworld",
                "jump_url": "https://discord.com/channels/1/2/3",
            }
        ],
    }


def test_build_message_response_to_json() -> None:
    response = build_message_response(
        MessageSummary(
            message_id=1,
            channel_id=2,
            author=AuthorSummary(
                author_id=3,
                author_name="alice",
                global_name="Alice",
                bot=False,
                discriminator="1234",
                avatar_url="https://cdn.example/avatar.png",
            ),
            created_at="2026-06-28T00:00:00+00:00",
            edited_at=None,
            content="hello",
            jump_url="https://discord.com/channels/1/2/3",
        )
    )

    rendered = json.loads(to_json(response))

    assert rendered["message"]["message_id"] == 1
    assert rendered["message"]["author"]["author_id"] == 3
    assert rendered["message"]["jump_url"] == "https://discord.com/channels/1/2/3"
