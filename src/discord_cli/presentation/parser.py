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

        return parser

    def parse_args(self) -> argparse.Namespace:
        return self.build().parse_args()
