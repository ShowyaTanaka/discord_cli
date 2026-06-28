from __future__ import annotations

from datetime import UTC

import discord

from discord_cli.models import AuthorSummary, ChannelSummary, GuildSummary, MessageSummary, ThreadSummary


def to_guild_summary(guild: discord.Guild) -> GuildSummary:
    return GuildSummary(
        guild_id=guild.id,
        name=guild.name,
        owner_id=guild.owner_id,
        member_count=guild.approximate_member_count,
    )


def to_channel_summary(channel: discord.abc.GuildChannel) -> ChannelSummary:
    return ChannelSummary(
        channel_id=channel.id,
        name=channel.name,
        channel_type=str(channel.type),
        category_id=getattr(channel, "category_id", None),
        position=getattr(channel, "position", None),
    )


def to_message_summary(message: discord.Message) -> MessageSummary:
    return MessageSummary(
        message_id=message.id,
        channel_id=message.channel.id,
        author=to_author_summary(message.author),
        created_at=message.created_at.astimezone(UTC).isoformat(),
        edited_at=message.edited_at.astimezone(UTC).isoformat() if message.edited_at else None,
        content=message.content,
        jump_url=message.jump_url,
    )


def to_author_summary(author: discord.abc.User) -> AuthorSummary:
    avatar = getattr(author, "display_avatar", None)
    return AuthorSummary(
        author_id=getattr(author, "id", None),
        author_name=str(author),
        global_name=getattr(author, "global_name", None),
        bot=getattr(author, "bot", False),
        discriminator=getattr(author, "discriminator", "0000"),
        avatar_url=str(avatar.url) if avatar is not None else None,
    )


def to_thread_summary(thread: discord.Thread) -> ThreadSummary:
    return ThreadSummary(
        thread_id=thread.id,
        parent_channel_id=thread.parent_id,
        name=thread.name,
        thread_type=str(thread.type),
        owner_id=thread.owner_id,
        message_count=thread.message_count,
        member_count=thread.member_count,
        archived=thread.archived,
    )
