# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際にClaude Code (claude.ai/code)にガイダンスを提供します。

## 開発用コマンド

### ゲームの実行
```bash
# デスクトップ版の実行
python sashimi_tanpopo_game.py

# Web版の実行（開発時）
python main.py
```

### 依存関係のインストール
```bash
# 基本的なゲーム依存関係
pip install pygame

# Web版ビルドに必要な依存関係
pip install pygame-ce pygbag black
```

### Web版ビルド
```bash
# pygbagを使用したWeb版ビルド
python -m pygbag --width 1000 --height 600 --no_opt main.py
```

## プロジェクト構造とアーキテクチャ

### コアファイル
- `main.py` - Web版メインファイル（pygbag対応、asyncio使用）
- `sashimi_tanpopo_game.py` - デスクトップ版（同期実行）
- `.github/workflows/pygbag.yml` - GitHub ActionsでのWeb版自動ビルド・デプロイ

### ゲームアーキテクチャ
このゲームはPygameベースのアクションゲームで、以下のクラス構造を持ちます：

#### 主要クラス
- `Game` - ゲームの全体制御、状態管理、難易度調整
- `SashimiPack` - ベルトコンベアで流れる刺身パック
- `Tanpopo` - プレイヤーが落下させるたんぽぽ

#### ゲームループ
- Web版: `main.py`の`async def main()`でasyncio対応
- デスクトップ版: `sashimi_tanpopo_game.py`の`Game.run()`で同期実行

#### 難易度システム
- `Game.calculate_difficulty()` - スコアベースの動的難易度調整
- レベルアップごとに速度上昇、出現間隔短縮
- レベルアップエフェクト表示機能

### 重要な設定値
- 画面サイズ: 1000x600px
- FPS: 60
- レベルアップ: 50ポイント間隔
- 最大速度倍率: 3.0倍

### Web版とデスクトップ版の違い
- Web版（main.py）: pygbag対応のため非同期処理、グローバルゲームインスタンス
- デスクトップ版（sashimi_tanpopo_game.py）: 同期処理、ローカルゲームインスタンス

## デプロイメント

### GitHub Pages自動デプロイ
- mainブランチとfeature/github-pages-playブランチへのプッシュで自動的にGitHub Pagesにデプロイ
- pygbagによるWeb Assembly変換
- ubuntu-latest（4 vCPU, 16 GiB）でビルド実行
- 20分タイムアウト設定でハング問題を回避

### ビルドプロセス
1. Python 3.11環境の準備
2. pygame-ce、pygbag、blackのインストール
3. pygbagによるWeb版ビルド（--no_opt --verboseフラグ使用）
4. distディレクトリの成果物をGitHub Pagesにアップロード

### GitHub Actionsの問題解決
- **タイムアウト問題**: pygbagビルドが異常に時間がかかる問題を解決
  - **根本原因**: pygbagのWASM変換プロセスが30分以上かかる
  - **対策**: タイムアウト時間を60分に延長（ステップ側55分）
  - **キャッシュ**: pip/pygbagキャッシュで2回目以降の高速化
  - **キープアライブ**: 10秒ごとの出力で無出力タイムアウト防止
  - **バッファリング無効化**: python -u フラグでリアルタイム出力

### パフォーマンス最適化
- **現在のスペック**: ubuntu-latestで4 vCPU, 16 GiBが標準提供
- **pygbagの特性**: バージョンに関係なく30分以上のビルド時間が必要
- **キャッシュ効果**: 初回ビルド後は依存関係のキャッシュで高速化
- **追加オプション**: さらなる高速化が必要な場合は8コア版/16コア版も検討可能

## 開発時の注意事項

### Web版開発時
- 非同期処理（asyncio）必須
- グローバルなゲームインスタンスの使用
- pygame.quit()後のasyncio.sleep(0)呼び出し

### コード品質
- black フォーマッターの使用
- Pythonの型ヒントは使用していない
- 日本語コメントとUI表示

### ゲームバランス調整
- BASE_CONVEYOR_SPEED, BASE_TANPOPO_FALL_SPEED等の定数で基本速度調整
- LEVEL_UP_SCORE_INTERVAL, MAX_SPEED_MULTIPLIER等で難易度カーブ調整

### Git操作時の注意
- **プッシュ前に必ず確認**: リモートリポジトリへのプッシュ前にユーザーに確認を求める
- **除外ファイル**: __pycache__/, build/等のローカルビルドファイルはコミット対象から除外