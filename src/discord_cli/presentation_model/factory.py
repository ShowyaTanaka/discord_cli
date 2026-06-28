from __future__ import annotations

from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary
from discord_cli.presentation_model.responses import (
    ChannelListResponse,
    ChannelPresentation,
    GuildListResponse,
    GuildPresentation,
    MessageListResponse,
    MessagePresentation,
    MessageResponse,
)


def build_guild_list_response(guilds: list[GuildSummary]) -> GuildListResponse:
    return GuildListResponse(guilds=[_build_guild_presentation(guild) for guild in guilds])


def build_channel_list_response(guild_id: int, channels: list[ChannelSummary]) -> ChannelListResponse:
    return ChannelListResponse(
        guild_id=guild_id,
        channels=[_build_channel_presentation(channel) for channel in channels],
    )


def build_message_list_response(channel_id: int, messages: list[MessageSummary]) -> MessageListResponse:
    return MessageListResponse(
        channel_id=channel_id,
        messages=[_build_message_presentation(message) for message in messages],
    )


def build_message_response(message: MessageSummary) -> MessageResponse:
    return MessageResponse(message=_build_message_presentation(message))


def _build_guild_presentation(guild: GuildSummary) -> GuildPresentation:
    return GuildPresentation(
        guild_id=guild.guild_id,
        name=guild.name,
        owner_id=guild.owner_id,
        member_count=guild.member_count,
    )


def _build_channel_presentation(channel: ChannelSummary) -> ChannelPresentation:
    return ChannelPresentation(
        channel_id=channel.channel_id,
        name=channel.name,
        channel_type=channel.channel_type,
        category_id=channel.category_id,
        position=channel.position,
    )


def _build_message_presentation(message: MessageSummary) -> MessagePresentation:
    return MessagePresentation(
        message_id=message.message_id,
        channel_id=message.channel_id,
        author_id=message.author_id,
        author_name=message.author_name,
        created_at=message.created_at,
        edited_at=message.edited_at,
        content=message.content,
        jump_url=message.jump_url,
    )
