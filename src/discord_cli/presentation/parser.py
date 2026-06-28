from __future__ import annotations

import argparse


class DiscordCliParser:
    def build(self) -> argparse.ArgumentParser:
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

        create_channel_parser = subparsers.add_parser("create-channel", help="Create a text channel in a guild")
        create_channel_parser.add_argument("--guild-id", type=int, help="Guild ID where the channel will be created")
        create_channel_parser.add_argument("--name", required=True, help="Channel name")
        create_channel_parser.add_argument("--category-id", type=int, help="Category channel ID")
        create_channel_parser.add_argument("--topic", help="Channel topic")
        create_channel_parser.add_argument("--position", type=int, help="Channel position")
        create_channel_parser.add_argument("--nsfw", action="store_true", help="Create as NSFW channel")
        create_channel_parser.add_argument("--reason", help="Audit log reason")

        create_thread_parser = subparsers.add_parser("create-thread", help="Create a thread in a text/forum channel")
        create_thread_parser.add_argument("--channel-id", type=int, help="Parent channel ID")
        create_thread_parser.add_argument("--name", required=True, help="Thread name")
        create_thread_parser.add_argument("--message-id", type=int, help="Starter message ID for text channel thread")
        create_thread_parser.add_argument("--content", help="Starter message content for forum thread")
        create_thread_parser.add_argument(
            "--auto-archive-duration",
            type=int,
            choices=[60, 1440, 4320, 10080],
            help="Auto archive duration in minutes",
        )
        create_thread_parser.add_argument("--private", action="store_true", help="Create a private thread in text channel")
        create_thread_parser.add_argument(
            "--invitable",
            action=argparse.BooleanOptionalAction,
            default=True,
            help="Whether non-moderators can invite others to a private thread",
        )
        create_thread_parser.add_argument("--slowmode-delay", type=int, help="Thread slowmode in seconds")
        create_thread_parser.add_argument("--reason", help="Audit log reason")

        return parser

    def parse_args(self) -> argparse.Namespace:
        return self.build().parse_args()
