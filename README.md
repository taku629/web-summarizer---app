# Web Summarizer App

このリポジトリは、Webサイトの要約サービスのフルスタックアプリケーションです。

## 構成
- backend: FastAPI + Gemini API による要約API
- frontend: Next.js (React) によるUI


## 使い方

### 1. バックエンド（APIサーバー）を起動
1. ターミナルで `backend` フォルダに移動
2. 仮想環境を作成し、アクティベート
	- Windows: `python -m venv venv` → `venv\Scripts\activate`
	- Mac/Linux: `python3 -m venv venv` → `source venv/bin/activate`
3. 依存パッケージをインストール
	- `pip install -r requirements.txt`
4. サーバーを起動
	- `uvicorn main:app --reload`

### 2. フロントエンド（Web UI）を起動
1. ターミナルで `frontend` フォルダに移動
2. 依存パッケージをインストール
	- `npm install`
3. 開発サーバーを起動
	- `npm run dev`
4. ブラウザで `http://localhost:3000` を開く

### 3. 使い方
- 入力欄に要約したいWebページのURLを入力し、「要約する」ボタンを押すと、AIが本文を要約して表示します。

## 主な機能
- Webページの本文を自動で抽出し、Gemini APIで要約
- 最新のGeminiモデルに対応
- 入力UI・要約結果の表示が見やすいデザイン

## 注意
- backend/.env.example を参考にAPIキーを設定してください
- node_modulesやvenvなどはpush対象外です

---

ご質問・要望はIssueまたはPull Requestでどうぞ。
