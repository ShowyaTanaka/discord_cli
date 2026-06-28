# discord_cli 設計と CLI 仕様

## 目的

`discord.py` を利用し、Bot トークンで Discord API に接続して以下を CLI から実行できるようにします。

- ギルド一覧の取得
- 指定ギルドのチャンネル一覧の取得
- 指定チャンネル内メッセージの一覧取得
- 指定メッセージの詳細取得
- 指定チャンネルへの投稿
- 指定ギルドへのテキストチャンネル作成
- 指定チャンネルへのスレッド作成
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
  - Service と Repository 間で扱うドメインデータ構造を定義する
- `src/discord_cli/repository.py`
  - `discord.py` と Bot 接続、Discord API 通信の技術詳細を閉じ込める
- `src/discord_cli/mapper.py`
  - `discord.py` のオブジェクトを entity へ変換する
- `src/discord_cli/service.py`
  - CLI のユースケースを調停し、Repository を呼び出す
- `src/discord_cli/presentation/`
  - `argparse` によるコマンドライン入力定義を持つ
- `src/discord_cli/presentation_model/`
  - JSON 出力形式を決める dataclass 群と serializer を置く
- `src/discord_cli/cli.py`
  - エントリポイントとユースケース制御を持つ

## Intents

以下を有効化します。

- `guilds`
- `messages`
- `message_content`

メッセージ本文の閲覧には `MESSAGE CONTENT INTENT` が必要です。

## コマンド一覧

### `guilds`

Bot が参加しているギルド一覧を JSON で表示します。

```bash
discord-cli guilds
```

JSON 項目:

- guild_id
- guild_name
- owner_id
- member_count

### `channels`

指定ギルドのチャンネル一覧を JSON で表示します。

```bash
discord-cli channels --guild-id 123456789012345678
```

`--guild-id` を省略した場合は `DEFAULT_GUILD_ID` を使います。

JSON 項目:

- channel_id
- channel_name
- channel_type
- category_id
- position

### `messages`

指定チャンネルのメッセージ履歴を JSON で表示します。

```bash
discord-cli messages --channel-id 123456789012345678 --limit 20
```

オプション:

- `--channel-id`: 対象チャンネル ID。未指定時は `DEFAULT_CHANNEL_ID`
- `--limit`: 取得件数。未指定時は `MESSAGE_FETCH_LIMIT`

JSON 項目:

- message_id
- created_at
- author
- content

### `message`

指定メッセージの詳細を JSON で表示します。

```bash
discord-cli message \
  --channel-id 123456789012345678 \
  --message-id 234567890123456789
```

JSON 項目:

- message_id
- channel_id
- author
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

投稿結果として、作成されたメッセージ情報を JSON で表示します。

### `create-channel`

指定ギルドに text channel を作成します。

```bash
discord-cli create-channel --guild-id 123456789012345678 --name "ops-log"
```

主なオプション:

- `--guild-id`: 作成先 guild ID。未指定時は `DEFAULT_GUILD_ID`
- `--name`: チャンネル名
- `--category-id`: 配下に置く category channel ID
- `--topic`: トピック
- `--position`: 表示位置
- `--nsfw`: NSFW チャンネルとして作成
- `--reason`: 監査ログ用理由

### `create-thread`

指定チャンネルに thread を作成します。

```bash
discord-cli create-thread --channel-id 123456789012345678 --name "incident-20260628" --private
```

text channel の場合:

- `--message-id` を渡すと既存メッセージから public thread を作成
- `--private` を渡すと private thread を作成

forum channel の場合:

- `--content` を渡して初期投稿付き thread を作成

主なオプション:

- `--channel-id`: 親チャンネル ID。未指定時は `DEFAULT_CHANNEL_ID`
- `--name`: thread 名
- `--message-id`: text channel 用の起点 message ID
- `--content`: forum channel 用の初期投稿本文
- `--auto-archive-duration`: `60`, `1440`, `4320`, `10080`
- `--private`: text channel で private thread を作成
- `--invitable` / `--no-invitable`: private thread への招待可否
- `--slowmode-delay`: slowmode 秒数
- `--reason`: 監査ログ用理由

## 環境変数

- `DISCORD_BOT_TOKEN`: 必須
- `DEFAULT_GUILD_ID`: 任意。`channels` の既定値
- `DEFAULT_CHANNEL_ID`: 任意。`messages` と `post` の既定値
- `MESSAGE_FETCH_LIMIT`: 任意。既定 20

## エラーハンドリング

- 必須の ID や Token が無い場合は CLI で明示的にエラーにする
- 投稿不可チャンネルや履歴取得不可チャンネルでは説明付き例外を返す
- Discord API 由来の失敗は `discord.py` の例外を捕捉して、CLI 向けに短く整形する

## JSON 出力方針

- CLI は domain model を直接 `json.dumps` しない
- `presentation_model` 配下の dataclass に変換してから `dataclasses.asdict` で JSON 化する
- これにより、出力契約を Service/Repository の内部データ構造から分離する

## 実装上の補足

- Guild と Channel の一覧取得はキャッシュではなく API ベース
- メッセージ一覧には添付ファイル URL は含めず、まずは本文と ID 確認を優先
- Bot 実運用の本体機能とは切り離し、運用確認や手作業オペレーション用の独立 CLI にする
