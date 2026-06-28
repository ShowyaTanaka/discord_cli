from __future__ import annotations

from collections.abc import Iterable

from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary


def format_guilds(guilds: Iterable[GuildSummary]) -> str:
    rows = [
        f"{guild.guild_id}\t{guild.name}\towner={guild.owner_id or '-'}\tmembers={guild.member_count or '-'}"
        for guild in guilds
    ]
    return _join_rows(rows, empty_message="No guilds found.")


def format_channels(channels: Iterable[ChannelSummary]) -> str:
    rows = [
        (
            f"{channel.channel_id}\t{channel.channel_type}\t{channel.name}"
            f"\tcategory={channel.category_id or '-'}\tposition={channel.position if channel.position is not None else '-'}"
        )
        for channel in channels
    ]
    return _join_rows(rows, empty_message="No channels found.")


def format_messages(messages: Iterable[MessageSummary]) -> str:
    rows = [
        (
            f"{message.message_id}\t{message.created_at}\t{message.author_name}"
            f"\t{_single_line(message.content)}"
        )
        for message in messages
    ]
    return _join_rows(rows, empty_message="No messages found.")


def format_message_detail(message: MessageSummary) -> str:
    return "\n".join(
        [
            f"message_id: {message.message_id}",
            f"channel_id: {message.channel_id}",
            f"author_id: {message.author_id or '-'}",
            f"author_name: {message.author_name}",
            f"created_at: {message.created_at}",
            f"edited_at: {message.edited_at or '-'}",
            f"content: {_single_line(message.content)}",
            f"jump_url: {message.jump_url}",
        ]
    )


def _join_rows(rows: list[str], empty_message: str) -> str:
    return "\n".join(rows) if rows else empty_message


def _single_line(text: str) -> str:
    collapsed = " ".join(text.splitlines()).strip()
    return collapsed or "<empty>"
