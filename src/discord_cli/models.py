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
class AuthorSummary:
    author_id: int | None
    author_name: str
    global_name: str | None
    bot: bool
    discriminator: str
    avatar_url: str | None


@dataclass(frozen=True)
class MessageSummary:
    message_id: int
    channel_id: int
    author: AuthorSummary
    created_at: str
    edited_at: str | None
    content: str
    jump_url: str


@dataclass(frozen=True)
class ThreadSummary:
    thread_id: int
    parent_channel_id: int
    name: str
    thread_type: str
    owner_id: int | None
    message_count: int | None
    member_count: int | None
    archived: bool
