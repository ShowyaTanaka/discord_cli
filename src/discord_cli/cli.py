from __future__ import annotations

import argparse
import asyncio

import discord

from discord_cli.config import Settings, load_settings
from discord_cli.formatters import (
    format_channels,
    format_guilds,
    format_message_detail,
    format_messages,
)
from discord_cli.service import DiscordService


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        settings = load_settings()
        output = asyncio.run(run_command(args=args, settings=settings))
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except (ValueError, TypeError, discord.DiscordException) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI tool for Discord operations using discord.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("guilds", help="List guilds visible to the bot")

    channels_parser = subparsers.add_parser("channels", help="List channels in a guild")
    channels_parser.add_argument("--guild-id", type=int, help="Guild ID to inspect")

    messages_parser = subparsers.add_parser("messages", help="List messages in a channel")
    messages_parser.add_argument("--channel-id", type=int, help="Channel ID to inspect")
    messages_parser.add_argument("--limit", type=int, help="Number of messages to fetch")

    message_parser = subparsers.add_parser("message", help="Fetch a single message by ID")
    message_parser.add_argument("--channel-id", type=int, help="Channel ID to inspect")
    message_parser.add_argument("--message-id", type=int, required=True, help="Message ID to fetch")

    post_parser = subparsers.add_parser("post", help="Post a message to a channel")
    post_parser.add_argument("--channel-id", type=int, help="Channel ID to post to")
    post_parser.add_argument("--message", required=True, help="Message content to post")

    return parser


async def run_command(args: argparse.Namespace, settings: Settings) -> str:
    async with DiscordService() as service:
        await service.login(settings.token)

        if args.command == "guilds":
            guilds = await service.list_guilds()
            return format_guilds(guilds)

        if args.command == "channels":
            guild_id = _resolve_id(args.guild_id, settings.default_guild_id, env_name="DEFAULT_GUILD_ID")
            channels = await service.list_channels(guild_id)
            return format_channels(channels)

        if args.command == "messages":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            limit = args.limit or settings.message_fetch_limit
            if limit <= 0:
                raise ValueError("--limit must be a positive integer.")
            messages = await service.list_messages(channel_id, limit)
            return format_messages(messages)

        if args.command == "message":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            message = await service.get_message(channel_id, args.message_id)
            return format_message_detail(message)

        if args.command == "post":
            channel_id = _resolve_id(args.channel_id, settings.default_channel_id, env_name="DEFAULT_CHANNEL_ID")
            message = await service.post_message(channel_id, args.message)
            return format_message_detail(message)

    raise ValueError(f"Unsupported command: {args.command}")


def _resolve_id(cli_value: int | None, default_value: int | None, env_name: str) -> int:
    if cli_value is not None:
        return cli_value
    if default_value is not None:
        return default_value
    raise ValueError(f"Missing required ID. Pass the CLI option or set {env_name}.")
