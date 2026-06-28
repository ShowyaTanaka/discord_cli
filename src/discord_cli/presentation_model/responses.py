from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuildPresentation:
    guild_id: int
    name: str
    owner_id: int | None
    member_count: int | None


@dataclass(frozen=True)
class ChannelPresentation:
    channel_id: int
    name: str
    channel_type: str
    category_id: int | None
    position: int | None


@dataclass(frozen=True)
class ThreadPresentation:
    thread_id: int
    parent_channel_id: int
    name: str
    thread_type: str
    owner_id: int | None
    message_count: int | None
    member_count: int | None
    archived: bool


@dataclass(frozen=True)
class AuthorPresentation:
    author_id: int | None
    author_name: str
    global_name: str | None
    bot: bool
    discriminator: str
    avatar_url: str | None


@dataclass(frozen=True)
class MessagePresentation:
    message_id: int
    channel_id: int
    author: AuthorPresentation
    created_at: str
    edited_at: str | None
    content: str
    jump_url: str


@dataclass(frozen=True)
class GuildListResponse:
    guilds: list[GuildPresentation]


@dataclass(frozen=True)
class ChannelListResponse:
    guild_id: int
    channels: list[ChannelPresentation]


@dataclass(frozen=True)
class MessageListResponse:
    channel_id: int
    messages: list[MessagePresentation]


@dataclass(frozen=True)
class MessageResponse:
    message: MessagePresentation


@dataclass(frozen=True)
class ChannelResponse:
    channel: ChannelPresentation


@dataclass(frozen=True)
class ThreadResponse:
    thread: ThreadPresentation
