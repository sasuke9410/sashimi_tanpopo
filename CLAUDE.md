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
- mainブランチへのプッシュで自動的にGitHub Pagesにデプロイ
- pygbagによるWeb Assembly変換
- 30分タイムアウト設定でハング問題を回避

### ビルドプロセス
1. Python 3.11環境の準備
2. pygame-ce、pygbag、blackのインストール
3. pygbagによるWeb版ビルド（--no_optフラグ使用）
4. distディレクトリの成果物をGitHub Pagesにアップロード

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