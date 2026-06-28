# discord_cli 設計と CLI 仕様

## 目的

`discord.py` を利用し、Bot トークンで Discord API に接続して以下を CLI から実行できるようにします。

- ギルド一覧の取得
- 指定ギルドのチャンネル一覧の取得
- 指定チャンネル内メッセージの一覧取得
- 指定メッセージの詳細取得
- 指定チャンネルへの投稿
- ギルド ID、チャンネル ID、メッセージ ID の確認

## 設計方針

- 常駐 Bot ではなくワンショット CLI として実装する
- `discord.Client.login()` 後に `discord.py` の REST API を利用して処理し、即終了する
- Gateway キャッシュへの依存を避け、`fetch_guilds`、`fetch_guild`、`fetch_channel`、`fetch_message`、`history` を使う
- 既存の `~/discord-bot` を参考に、環境変数による設定管理と最小限の Intents 設定を採用する

## モジュール構成

- `src/discord_cli/config.py`
  - `.env` と環境変数を読み込み、CLI のデフォルト設定を解決する
- `src/discord_cli/models.py`
  - CLI 出力で扱うデータ構造を定義する
- `src/discord_cli/service.py`
  - `discord.py` をラップし、Discord との通信処理を集約する
- `src/discord_cli/formatters.py`
  - 取得データを人間が見やすいテキストに整形する
- `src/discord_cli/cli.py`
  - `argparse` によるコマンドライン定義とユースケース制御

## Intents

以下を有効化します。

- `guilds`
- `messages`
- `message_content`

メッセージ本文の閲覧には `MESSAGE CONTENT INTENT` が必要です。

## コマンド一覧

### `guilds`

Bot が参加しているギルド一覧を表示します。

```bash
discord-cli guilds
```

出力項目:

- guild_id
- guild_name
- owner_id
- member_count

### `channels`

指定ギルドのチャンネル一覧を表示します。

```bash
discord-cli channels --guild-id 123456789012345678
```

`--guild-id` を省略した場合は `DEFAULT_GUILD_ID` を使います。

出力項目:

- channel_id
- channel_name
- channel_type
- category_id
- position

### `messages`

指定チャンネルのメッセージ履歴を表示します。

```bash
discord-cli messages --channel-id 123456789012345678 --limit 20
```

オプション:

- `--channel-id`: 対象チャンネル ID。未指定時は `DEFAULT_CHANNEL_ID`
- `--limit`: 取得件数。未指定時は `MESSAGE_FETCH_LIMIT`

出力項目:

- message_id
- created_at
- author
- content

### `message`

指定メッセージの詳細を表示します。

```bash
discord-cli message \
  --channel-id 123456789012345678 \
  --message-id 234567890123456789
```

出力項目:

- message_id
- channel_id
- author_id
- author_name
- created_at
- edited_at
- content
- jump_url

### `post`

指定チャンネルへメッセージを投稿します。

```bash
discord-cli post --channel-id 123456789012345678 --message "hello"
```

オプション:

- `--channel-id`: 投稿先チャンネル ID。未指定時は `DEFAULT_CHANNEL_ID`
- `--message`: 投稿本文

投稿結果として、作成された `message_id` と `jump_url` を表示します。

## 環境変数

- `DISCORD_BOT_TOKEN`: 必須
- `DEFAULT_GUILD_ID`: 任意。`channels` の既定値
- `DEFAULT_CHANNEL_ID`: 任意。`messages` と `post` の既定値
- `MESSAGE_FETCH_LIMIT`: 任意。既定 20

## エラーハンドリング

- 必須の ID や Token が無い場合は CLI で明示的にエラーにする
- 投稿不可チャンネルや履歴取得不可チャンネルでは説明付き例外を返す
- Discord API 由来の失敗は `discord.py` の例外を捕捉して、CLI 向けに短く整形する

## 実装上の補足

- Guild と Channel の一覧取得はキャッシュではなく API ベース
- メッセージ一覧には添付ファイル URL は含めず、まずは本文と ID 確認を優先
- Bot 実運用の本体機能とは切り離し、運用確認や手作業オペレーション用の独立 CLI にする
