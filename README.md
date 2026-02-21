# VTuber Task Manager

Flaskで作成したシンプルなタスク管理Webアプリです。  
配信・動画・SNS投稿など、VTuber活動のタスクをまとめて管理できます。

## デモ
- 画面イメージ：`docs/demo.png`（スクショを置いて貼るのがおすすめ）

## ✨ 主な機能
- タスクの追加 / 編集 / 削除
- 完了チェック（完了・未完了の切り替え）
- JSONファイル（tasks.json）によるデータ保存

## 使用技術
- Python / Flask
- Jinja2
- HTML / CSS
- JSON（データ永続化）
- Git / GitHub

## セットアップ & 起動方法
```bash
git clone https://github.com/lvkfc1623-arch/vtuber-task-manager.git
cd vtuber-task-manager

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
flask run
