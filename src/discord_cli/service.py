from __future__ import annotations

from discord_cli.models import ChannelSummary, GuildSummary, MessageSummary
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

    async def close(self) -> None:
        await self._repository.close()

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
