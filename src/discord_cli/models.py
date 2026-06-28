from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuildSummary:
    guild_id: int
    name: str
    owner_id: int | None
    member_count: int | None


@dataclass(frozen=True)
class ChannelSummary:
    channel_id: int
    name: str
    channel_type: str
    category_id: int | None
    position: int | None


@dataclass(frozen=True)
class MessageSummary:
    message_id: int
    channel_id: int
    author_id: int | None
    author_name: str
    created_at: str
    edited_at: str | None
    content: str
    jump_url: str
