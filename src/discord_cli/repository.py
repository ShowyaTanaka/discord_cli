from __future__ import annotations

from datetime import UTC

import discord

from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary


class DiscordRepository:
    def __init__(self) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        self._client = discord.Client(intents=intents)

    async def __aenter__(self) -> "DiscordRepository":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def login(self, token: str) -> None:
        await self._client.login(token)

    async def close(self) -> None:
        if not self._client.is_closed():
            await self._client.close()

    async def list_guilds(self) -> list[GuildSummary]:
        guilds: list[GuildSummary] = []
        async for guild in self._client.fetch_guilds(limit=None):
            guilds.append(
                GuildSummary(
                    guild_id=guild.id,
                    name=guild.name,
                    owner_id=guild.owner_id,
                    member_count=guild.approximate_member_count,
                )
            )
        return guilds

    async def list_channels(self, guild_id: int) -> list[ChannelSummary]:
        guild = await self._client.fetch_guild(guild_id)
        channels = await guild.fetch_channels()
        return [self._to_channel_summary(channel) for channel in sorted(channels, key=_channel_sort_key)]

    async def list_messages(self, channel_id: int, limit: int) -> list[MessageSummary]:
        channel = await self._fetch_messageable_channel(channel_id)
        messages = [self._to_message_summary(message) async for message in channel.history(limit=limit)]
        messages.reverse()
        return messages

    async def get_message(self, channel_id: int, message_id: int) -> MessageSummary:
        channel = await self._fetch_messageable_channel(channel_id)
        message = await channel.fetch_message(message_id)
        return self._to_message_summary(message)

    async def post_message(self, channel_id: int, content: str) -> MessageSummary:
        channel = await self._fetch_messageable_channel(channel_id)
        message = await channel.send(content)
        return self._to_message_summary(message)

    async def _fetch_messageable_channel(self, channel_id: int) -> discord.abc.Messageable:
        channel = await self._client.fetch_channel(channel_id)
        if not isinstance(channel, discord.abc.Messageable):
            raise TypeError(f"Channel {channel_id} does not support messages.")
        return channel

    def _to_channel_summary(self, channel: discord.abc.GuildChannel) -> ChannelSummary:
        return ChannelSummary(
            channel_id=channel.id,
            name=channel.name,
            channel_type=str(channel.type),
            category_id=getattr(channel, "category_id", None),
            position=getattr(channel, "position", None),
        )

    def _to_message_summary(self, message: discord.Message) -> MessageSummary:
        return MessageSummary(
            message_id=message.id,
            channel_id=message.channel.id,
            author_id=getattr(message.author, "id", None),
            author_name=str(message.author),
            created_at=message.created_at.astimezone(UTC).isoformat(),
            edited_at=message.edited_at.astimezone(UTC).isoformat() if message.edited_at else None,
            content=message.content,
            jump_url=message.jump_url,
        )


def _channel_sort_key(channel: discord.abc.GuildChannel) -> tuple[int, int, int]:
    return (getattr(channel, "category_id", 0) or 0, getattr(channel, "position", 0), channel.id)
