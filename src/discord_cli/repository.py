from __future__ import annotations

import discord

from discord_cli.mapper import to_channel_summary, to_guild_summary, to_message_summary, to_thread_summary
from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary, ThreadSummary


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
            guilds.append(to_guild_summary(guild))
        return guilds

    async def list_channels(self, guild_id: int) -> list[ChannelSummary]:
        guild = await self._client.fetch_guild(guild_id)
        channels = await guild.fetch_channels()
        return [to_channel_summary(channel) for channel in sorted(channels, key=_channel_sort_key)]

    async def list_messages(self, channel_id: int, limit: int) -> list[MessageSummary]:
        channel = await self._fetch_messageable_channel(channel_id)
        messages = [to_message_summary(message) async for message in channel.history(limit=limit)]
        messages.reverse()
        return messages

    async def get_message(self, channel_id: int, message_id: int) -> MessageSummary:
        channel = await self._fetch_messageable_channel(channel_id)
        message = await channel.fetch_message(message_id)
        return to_message_summary(message)

    async def post_message(self, channel_id: int, content: str) -> MessageSummary:
        channel = await self._fetch_messageable_channel(channel_id)
        message = await channel.send(content)
        return to_message_summary(message)

    async def create_text_channel(
        self,
        guild_id: int,
        name: str,
        *,
        category_id: int | None = None,
        topic: str | None = None,
        position: int | None = None,
        nsfw: bool = False,
        reason: str | None = None,
    ) -> ChannelSummary:
        guild = await self._client.fetch_guild(guild_id)
        category = None
        if category_id is not None:
            category_channel = await self._client.fetch_channel(category_id)
            if not isinstance(category_channel, discord.CategoryChannel):
                raise TypeError(f"Channel {category_id} is not a category channel.")
            category = category_channel

        channel = await guild.create_text_channel(
            name=name,
            category=category,
            topic=topic if topic is not None else discord.utils.MISSING,
            position=position if position is not None else discord.utils.MISSING,
            nsfw=nsfw,
            reason=reason,
        )
        return to_channel_summary(channel)

    async def create_thread(
        self,
        channel_id: int,
        name: str,
        *,
        message_id: int | None = None,
        content: str | None = None,
        auto_archive_duration: int | None = None,
        private: bool = False,
        invitable: bool = True,
        slowmode_delay: int | None = None,
        reason: str | None = None,
    ) -> ThreadSummary:
        channel = await self._client.fetch_channel(channel_id)

        if isinstance(channel, discord.TextChannel):
            return await self._create_text_channel_thread(
                channel,
                name=name,
                message_id=message_id,
                auto_archive_duration=auto_archive_duration,
                private=private,
                invitable=invitable,
                slowmode_delay=slowmode_delay,
                reason=reason,
            )

        if isinstance(channel, discord.ForumChannel):
            return await self._create_forum_thread(
                channel,
                name=name,
                content=content,
                auto_archive_duration=auto_archive_duration,
                slowmode_delay=slowmode_delay,
                reason=reason,
            )

        raise TypeError(f"Channel {channel_id} does not support thread creation.")

    async def _fetch_messageable_channel(self, channel_id: int) -> discord.abc.Messageable:
        channel = await self._client.fetch_channel(channel_id)
        if not isinstance(channel, discord.abc.Messageable):
            raise TypeError(f"Channel {channel_id} does not support messages.")
        return channel

    async def _create_text_channel_thread(
        self,
        channel: discord.TextChannel,
        *,
        name: str,
        message_id: int | None,
        auto_archive_duration: int | None,
        private: bool,
        invitable: bool,
        slowmode_delay: int | None,
        reason: str | None,
    ) -> ThreadSummary:
        if message_id is None and not private:
            raise ValueError("Text channel thread creation requires --message-id or --private.")
        if message_id is not None and private:
            raise ValueError("Use either --message-id for public thread or --private for private thread, not both.")

        thread_type = discord.ChannelType.private_thread if private else None
        message = await channel.fetch_message(message_id) if message_id is not None else None

        thread = await channel.create_thread(
            name=name,
            message=message,
            auto_archive_duration=auto_archive_duration if auto_archive_duration is not None else discord.utils.MISSING,
            type=thread_type,
            reason=reason,
            invitable=invitable,
            slowmode_delay=slowmode_delay,
        )
        return to_thread_summary(thread)

    async def _create_forum_thread(
        self,
        channel: discord.ForumChannel,
        *,
        name: str,
        content: str | None,
        auto_archive_duration: int | None,
        slowmode_delay: int | None,
        reason: str | None,
    ) -> ThreadSummary:
        if not content:
            raise ValueError("Forum thread creation requires --content.")

        thread_with_message = await channel.create_thread(
            name=name,
            content=content,
            auto_archive_duration=auto_archive_duration if auto_archive_duration is not None else discord.utils.MISSING,
            slowmode_delay=slowmode_delay,
            reason=reason,
        )
        return to_thread_summary(thread_with_message.thread)


def _channel_sort_key(channel: discord.abc.GuildChannel) -> tuple[int, int, int]:
    return (getattr(channel, "category_id", 0) or 0, getattr(channel, "position", 0), channel.id)
