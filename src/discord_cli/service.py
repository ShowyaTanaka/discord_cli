from __future__ import annotations

from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary, ThreadSummary
from discord_cli.repository import DiscordRepository


class DiscordService:
    def __init__(self, repository: DiscordRepository | None = None) -> None:
        self._repository = repository or DiscordRepository()

    async def __aenter__(self) -> "DiscordService":
        await self._repository.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._repository.__aexit__(exc_type, exc, tb)

    async def login(self, token: str) -> None:
        await self._repository.login(token)

    async def list_guilds(self) -> list[GuildSummary]:
        return await self._repository.list_guilds()

    async def list_channels(self, guild_id: int) -> list[ChannelSummary]:
        return await self._repository.list_channels(guild_id)

    async def list_messages(self, channel_id: int, limit: int) -> list[MessageSummary]:
        return await self._repository.list_messages(channel_id, limit)

    async def get_message(self, channel_id: int, message_id: int) -> MessageSummary:
        return await self._repository.get_message(channel_id, message_id)

    async def post_message(self, channel_id: int, content: str) -> MessageSummary:
        if not content.strip():
            raise ValueError("Message content must not be empty.")
        return await self._repository.post_message(channel_id, content)

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
        if not name.strip():
            raise ValueError("Channel name must not be empty.")
        return await self._repository.create_text_channel(
            guild_id,
            name,
            category_id=category_id,
            topic=topic,
            position=position,
            nsfw=nsfw,
            reason=reason,
        )

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
        if not name.strip():
            raise ValueError("Thread name must not be empty.")
        return await self._repository.create_thread(
            channel_id,
            name,
            message_id=message_id,
            content=content,
            auto_archive_duration=auto_archive_duration,
            private=private,
            invitable=invitable,
            slowmode_delay=slowmode_delay,
            reason=reason,
        )
