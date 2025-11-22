# Paradigm Shift Classifier

スタートアップ企業をパラダイムシフト6階層モデルで分析・分類するフルスタックWebアプリケーション

## 概要

このアプリケーションは、1990年以降に創業されたスタートアップ企業を入力すると、パラダイムシフト6階層モデル（Layer 0〜5）のどの階層に位置するかを分析し、その理由と共に表示します。

### パラダイムシフト6階層モデル

- **Layer 0: Pre-Shift (未形成)** - PMF未達、事業構造未確立
- **Layer 1: Minimal Shift (最小変化)** - 既存産業の改善・効率化
- **Layer 2: Emerging Shift (変化萌芽)** - 新しい市場構造・顧客行動の観測開始
- **Layer 3: Structural Shift (構造変化)** - 産業構造・商流・取引形態の書き換え
- **Layer 4: Systemic Shift (制度変換)** - 制度・政策・社会システムへの組み込み
- **Layer 5: Paradigm Shift (規範転換)** - 社会規範・文化・生活様式の塗り替え

## 技術スタック

### バックエンド
- **FastAPI** - Python Webフレームワーク
- **Poetry** - 依存関係管理
- **OpenAI API** - AI分析（オプション）
- **python-dotenv** - 環境変数管理

### フロントエンド
- **React** - UIライブラリ
- **TypeScript** - 型安全性
- **Vite** - ビルドツール
- **Tailwind CSS** - スタイリング
- **shadcn/ui** - UIコンポーネント

## 機能

### 1. ルールベース分析
知識ベースに登録された有名企業（OpenAI、Amazon、Google、Airbnb、Uber、メルカリ、Sansan等）については、事前に定義された分析結果を即座に表示します。

### 2. AI分析（オプション）
OpenAI APIキーを設定すると、知識ベースにない企業もAIが自動的に分析・分類します。

### 3. スコープ検証
1990年以前に創業された企業（Apple、Microsoft等）は「対象外」として明確に区別されます。

### 4. 分析モード表示
- **AIモード**: OpenAI APIによる分析
- **ルールベース**: 知識ベースによる分析

## セットアップ

### バックエンド

```bash
cd backend
poetry install
poetry run fastapi dev app/main.py
```

バックエンドは http://localhost:8000 で起動します。

#### 環境変数（オプション）

`.env` ファイルを作成してOpenAI APIキーを設定すると、AI分析モードが有効になります：

```
OPENAI_API_KEY=your_api_key_here
```

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

フロントエンドは http://localhost:5173 で起動します。

#### 環境変数

`frontend/.env` ファイルでバックエンドAPIのURLを設定：

```
VITE_API_URL=http://localhost:8000
```

## デプロイ

### バックエンド
- Fly.io にデプロイ済み: https://app-wgsxojfz.fly.dev

### フロントエンド
- devinapps.com にデプロイ済み: https://startup-paradigm-app-nnayun42.devinapps.com

## プロジェクト構造

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI アプリケーション
│   │   ├── analyzer.py          # 分析ロジック
│   │   ├── paradigm_framework.py # 6階層モデル定義
│   │   └── knowledge_base.py    # 企業知識ベース
│   ├── pyproject.toml           # Poetry 依存関係
│   └── poetry.lock
└── frontend/
    ├── src/
    │   ├── App.tsx              # メインアプリケーション
    │   └── components/          # UIコンポーネント
    ├── package.json
    └── vite.config.ts
```

## API エンドポイント

### POST /api/analyze

スタートアップ企業を分析します。

**リクエスト:**
```json
{
  "startup_name": "OpenAI"
}
```

**レスポンス:**
```json
{
  "startup_name": "OpenAI",
  "layer_id": 5,
  "layer_name": "Paradigm Shift",
  "jp_name": "規範転換",
  "definition": "社会規範・文化・生活様式そのものを塗り替えた段階。",
  "reasoning": "OpenAIは2015年創業のAI研究企業で...",
  "criteria_met": {
    "revenue": "推定年間売上20億ドル超（約3000億円）",
    "behavior_change": "世界中で「ChatGPTで調べる」という行動が定着",
    ...
  },
  "criteria": {...},
  "mode": "rule_based"
}
```

## 知識ベースに登録されている企業

### Layer 5 (Paradigm Shift)
- OpenAI
- Amazon
- Google
- Airbnb
- Uber

### Layer 4 (Systemic Shift)
- Stripe
- メルカリ

### Layer 3 (Structural Shift)
- Sansan
- SmartHR

### Layer 2 (Emerging Shift)
- ココナラ

## ライセンス

MIT

## 作成者

清水輝幸 (teruyuki04@gmail.com)

## 開発支援

このプロジェクトは Devin (Cognition AI) の支援により開発されました。
Devin run: https://app.devin.ai/sessions/6407f880f2194d2cbb80b6c2f0de0f1a
