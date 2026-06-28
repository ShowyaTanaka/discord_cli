from __future__ import annotations

import asyncio

import discord

from discord_cli.config import Settings, load_settings
from discord_cli.presentation.parser import DiscordCliParser
from discord_cli.presentation_model.factory import (
    build_channel_response,
    build_channel_list_response,
    build_guild_list_response,
    build_message_list_response,
    build_message_response,
    build_thread_response,
)
from discord_cli.presentation_model.serializer import to_json
from discord_cli.service import DiscordService


def main() -> None:
    args = DiscordCliParser().parse_args()

    try:
        settings = load_settings()
        output = asyncio.run(run_command(args=args, settings=settings))
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except (ValueError, TypeError, discord.DiscordException) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print(output)


async def run_command(args, settings: Settings) -> str:
    async with DiscordService() as service:
        await service.login(settings.token)

        if args.command == "guilds":
            guilds = await service.list_guilds()
            return to_json(build_guild_list_response(guilds))

        if args.command == "channels":
            guild_id = _resolve_id(args.guild_id, settings.default_guild_id, env_name="DEFAULT_GUILD_ID")
            channels = await service.list_channels(guild_id)
            return to_json(build_channel_list_response(guild_id, channels))

        if args.command == "messages":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            limit = args.limit or settings.message_fetch_limit
            if limit <= 0:
                raise ValueError("--limit must be a positive integer.")
            messages = await service.list_messages(channel_id, limit)
            return to_json(build_message_list_response(channel_id, messages))

        if args.command == "message":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            message = await service.get_message(channel_id, args.message_id)
            return to_json(build_message_response(message))

        if args.command == "post":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            message = await service.post_message(channel_id, args.message)
            return to_json(build_message_response(message))

        if args.command == "create-channel":
            guild_id = _resolve_id(args.guild_id, settings.default_guild_id, env_name="DEFAULT_GUILD_ID")
            channel = await service.create_text_channel(
                guild_id,
                args.name,
                category_id=args.category_id,
                topic=args.topic,
                position=args.position,
                nsfw=args.nsfw,
                reason=args.reason,
            )
            return to_json(build_channel_response(channel))

        if args.command == "create-thread":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            thread = await service.create_thread(
                channel_id,
                args.name,
                message_id=args.message_id,
                content=args.content,
                auto_archive_duration=args.auto_archive_duration,
                private=args.private,
                invitable=args.invitable,
                slowmode_delay=args.slowmode_delay,
                reason=args.reason,
            )
            return to_json(build_thread_response(thread))

    raise ValueError(f"Unsupported command: {args.command}")


def _resolve_id(cli_value: int | None, default_value: int | None, env_name: str) -> int:
    if cli_value is not None:
        return cli_value
    if default_value is not None:
        return default_value
    raise ValueError(f"Missing required ID. Pass the CLI option or set {env_name}.")
