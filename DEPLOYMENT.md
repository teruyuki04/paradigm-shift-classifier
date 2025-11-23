# Fly.io デプロイガイド

このガイドでは、パラダイムシフト分類アプリケーションをFly.ioにデプロイする手順を説明します。

## 前提条件

- Fly.io アカウント（https://fly.io/signup で作成）
- Fly.io CLI がインストール済み
- OpenAI API キー

## 1. Fly.io CLI のインストール

```bash
# macOS / Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

インストール後、PATHに追加:
```bash
export FLYCTL_INSTALL="$HOME/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
```

## 2. Fly.io にログイン

```bash
flyctl auth login
```

ブラウザが開き、Fly.ioアカウントでログインします。

## 3. バックエンドのデプロイ

### 3.1 バックエンドディレクトリに移動

```bash
cd backend
```

### 3.2 Fly.io アプリを作成（初回のみ）

```bash
# 既存のアプリ名を使用する場合
flyctl apps create app-fpxysssf

# または新しいアプリ名で作成
flyctl launch --no-deploy
```

`fly.toml` ファイルが既に存在するため、設定は自動的に読み込まれます。

### 3.3 OpenAI API キーを設定

```bash
flyctl secrets set OpenAI_API_KEY="your-openai-api-key-here" -a app-fpxysssf
```

**重要**: `your-openai-api-key-here` を実際のOpenAI APIキーに置き換えてください。

### 3.4 バックエンドをデプロイ

```bash
flyctl deploy -a app-fpxysssf
```

デプロイが完了すると、バックエンドURLが表示されます:
```
https://app-fpxysssf.fly.dev
```

### 3.5 バックエンドの動作確認

```bash
# ヘルスチェック
curl https://app-fpxysssf.fly.dev/healthz

# OpenAI統合のテスト
curl -X POST https://app-fpxysssf.fly.dev/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"startup_name": "Preferred Networks"}'
```

## 4. フロントエンドのデプロイ

### 4.1 フロントエンドディレクトリに移動

```bash
cd ../frontend
```

### 4.2 環境変数を確認

`fly.toml` ファイルの `[env]` セクションで、バックエンドURLが正しく設定されていることを確認:

```toml
[env]
  VITE_API_URL = "https://app-fpxysssf.fly.dev"
```

### 4.3 Fly.io アプリを作成（初回のみ）

```bash
flyctl launch --no-deploy
```

アプリ名を入力（例: `paradigm-shift-classifier-frontend`）

### 4.4 フロントエンドをデプロイ

```bash
flyctl deploy
```

デプロイが完了すると、フロントエンドURLが表示されます:
```
https://paradigm-shift-classifier-frontend.fly.dev
```

### 4.5 フロントエンドの動作確認

ブラウザでフロントエンドURLにアクセスし、以下を確認:
1. ページが正常に表示される
2. スタートアップ名を入力して検索できる
3. 分析結果が表示される
4. データソース（EDINET、Wikipedia、ChatGPT）が表示される

## 5. デプロイ後の管理

### ログの確認

```bash
# バックエンドのログ
flyctl logs -a app-fpxysssf

# フロントエンドのログ
flyctl logs -a paradigm-shift-classifier-frontend
```

### アプリの状態確認

```bash
# バックエンドの状態
flyctl status -a app-fpxysssf

# フロントエンドの状態
flyctl status -a paradigm-shift-classifier-frontend
```

### スケーリング

```bash
# マシンを追加
flyctl scale count 2 -a app-fpxysssf

# メモリを増やす
flyctl scale memory 2048 -a app-fpxysssf
```

### シークレットの管理

```bash
# シークレットの一覧表示
flyctl secrets list -a app-fpxysssf

# シークレットの削除
flyctl secrets unset OpenAI_API_KEY -a app-fpxysssf

# シークレットの更新
flyctl secrets set OpenAI_API_KEY="new-api-key" -a app-fpxysssf
```

## 6. 再デプロイ

コードを更新した後、再デプロイする手順:

### バックエンドの再デプロイ

```bash
cd backend
git pull origin main
flyctl deploy -a app-fpxysssf
```

### フロントエンドの再デプロイ

```bash
cd frontend
git pull origin main
flyctl deploy
```

## 7. トラブルシューティング

### デプロイが失敗する場合

```bash
# ログを確認
flyctl logs -a app-fpxysssf

# マシンを再起動
flyctl machine restart -a app-fpxysssf
```

### OpenAI APIが動作しない場合

1. シークレットが正しく設定されているか確認:
   ```bash
   flyctl secrets list -a app-fpxysssf
   ```

2. バックエンドのログでエラーを確認:
   ```bash
   flyctl logs -a app-fpxysssf
   ```

3. OpenAI APIキーが有効か確認

### フロントエンドがバックエンドに接続できない場合

1. `fly.toml` の `VITE_API_URL` が正しいか確認
2. バックエンドが起動しているか確認:
   ```bash
   curl https://app-fpxysssf.fly.dev/healthz
   ```
3. CORSエラーがないかブラウザのコンソールを確認

## 8. コスト最適化

Fly.ioは使用量に応じて課金されます。コストを最適化するには:

1. **自動停止を有効化**（既に設定済み）:
   ```toml
   auto_stop_machines = "stop"
   auto_start_machines = true
   min_machines_running = 0
   ```

2. **不要なマシンを削除**:
   ```bash
   flyctl machine list -a app-fpxysssf
   flyctl machine destroy <machine-id> -a app-fpxysssf
   ```

3. **リソースを最小限に**:
   - バックエンド: 1GB RAM, 1 CPU
   - フロントエンド: 512MB RAM, 1 CPU

## 9. セキュリティ

1. **シークレットの管理**: OpenAI APIキーは必ずFly.ioのシークレット機能を使用
2. **HTTPS**: Fly.ioは自動的にHTTPSを有効化
3. **環境変数**: `.env` ファイルはGitにコミットしない（`.gitignore` に追加済み）

## 10. サポート

問題が発生した場合:
- Fly.io ドキュメント: https://fly.io/docs/
- Fly.io コミュニティ: https://community.fly.io/
- GitHub Issues: https://github.com/teruyuki04/paradigm-shift-classifier/issues
