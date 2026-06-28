from __future__ import annotations

from discord_cli.formatters import (
    format_channels,
    format_guilds,
    format_message_detail,
    format_messages,
)
from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary


def test_format_guilds() -> None:
    rendered = format_guilds([GuildSummary(guild_id=1, name="test", owner_id=2, member_count=3)])

    assert rendered == "1\ttest\towner=2\tmembers=3"


def test_format_channels() -> None:
    rendered = format_channels(
        [ChannelSummary(channel_id=1, name="general", channel_type="text", category_id=None, position=0)]
    )

    assert rendered == "1\ttext\tgeneral\tcategory=-\tposition=0"


def test_format_messages_collapses_multiline_content() -> None:
    rendered = format_messages(
        [
            MessageSummary(
                message_id=1,
                channel_id=2,
                author_id=3,
                author_name="alice",
                created_at="2026-06-28T00:00:00+00:00",
                edited_at=None,
                content="hello\nworld",
                jump_url="https://discord.com/channels/1/2/3",
            )
        ]
    )

    assert rendered == "1\t2026-06-28T00:00:00+00:00\talice\thello world"


def test_format_message_detail() -> None:
    rendered = format_message_detail(
        MessageSummary(
            message_id=1,
            channel_id=2,
            author_id=3,
            author_name="alice",
            created_at="2026-06-28T00:00:00+00:00",
            edited_at=None,
            content="hello",
            jump_url="https://discord.com/channels/1/2/3",
        )
    )

    assert "message_id: 1" in rendered
    assert "jump_url: https://discord.com/channels/1/2/3" in rendered
