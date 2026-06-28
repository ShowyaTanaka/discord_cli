# discord_cli

`discord.py` を使って Discord へ投稿、ギルド取得、チャンネル取得、チャンネル内メッセージ閲覧、各種 ID 確認を行う CLI ツールです。

詳細設計とコマンド仕様は [docs/design.md](/Users/noellight/discord_cli/docs/design.md) にまとめています。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

`.env` に最低限 `DISCORD_BOT_TOKEN` を設定してください。

## 使い方

```bash
discord-cli guilds
discord-cli channels --guild-id 123456789012345678
discord-cli messages --channel-id 123456789012345678 --limit 30
discord-cli message --channel-id 123456789012345678 --message-id 123456789012345678
discord-cli post --channel-id 123456789012345678 --message "hello from discord.py"
```

`python -m discord_cli ...` でも同じように実行できます。

## 注意点

- メッセージ内容を読むには Bot 側で `MESSAGE CONTENT INTENT` が必要です。
- Bot を対象ギルドへ招待し、対象チャンネルを閲覧・送信できる権限を付与してください。
- この CLI は常駐せず、実行ごとにログインして 1 操作だけ行って終了します。
