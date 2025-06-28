# 刺身たんぽぽゲーム 🍣🌼

[![Build and Deploy](https://github.com/sasuke9410/sashimi_tanpopo/actions/workflows/pygbag.yml/badge.svg)](https://github.com/sasuke9410/sashimi_tanpopo/actions/workflows/pygbag.yml)

ベルトコンベアで流れる刺身パックにたんぽぽを落として乗せるユニークなアクションゲーム！

## 🎮 ゲームプレイ

- **目標**: ベルトコンベアで流れる刺身パックにたんぽぽを乗せよう
- **操作**: 画面をクリックしてたんぽぽを落下させる
- **得点**: たんぽぽが乗った刺身パックが左端に到達すると10ポイント獲得
- **難易度**: スコアが上がるにつれてベルトコンベアの速度が上昇

## 🌟 特徴

- **動的難易度調整**: レベルアップに応じて速度と出現間隔が変化
- **レベルシステム**: 50ポイントごとにレベルアップ
- **視覚エフェクト**: レベルアップ時の金色エフェクト
- **リアルタイム情報**: スコア、レベル、速度、次レベルまでのポイントを表示

## 🚀 プレイ方法

### オンラインでプレイ
GitHub Pagesでブラウザから直接プレイできます：
**[🎮 ゲームをプレイする](https://sasuke9410.github.io/sashimi_tanpopo/)**

### ローカルでプレイ
```bash
# リポジトリをクローン
git clone https://github.com/sasuke9410/sashimi_tanpopo.git
cd sashimi_tanpopo

# 依存関係をインストール
pip install pygame

# ゲームを実行
python sashimi_tanpopo_game.py
```

## 🛠️ 技術仕様

- **言語**: Python 3.11+
- **ライブラリ**: Pygame
- **Web版**: pygbag (Pygame Web Assembly)
- **デプロイ**: GitHub Pages + GitHub Actions

## 📁 プロジェクト構成

```
sashimi_tanpopo/
├── main.py                    # Web版メインファイル (pygbag対応)
├── sashimi_tanpopo_game.py   # デスクトップ版
├── game_improvements.md      # ゲーム改善案
├── dev-log.md               # 開発ログ
├── blog.md                  # 開発体験記
├── .github/workflows/       # GitHub Actions設定
│   └── pygbag.yml
└── README.md               # このファイル
```

## 🎯 今後の実装予定

- [ ] コンボシステム（連続成功ボーナス）
- [ ] メニューシステム（タイトル画面・ゲームオーバー画面）
- [ ] 多様な刺身パック（サイズ・種類のバリエーション）
- [ ] サウンド効果（和風BGM・効果音）
- [ ] ハイスコアシステム
- [ ] 特別モード（チャレンジモード）

## 🤝 開発について

このゲームはAIとの協働開発プロジェクトとして作成されました。開発プロセスの詳細は[blog.md](blog.md)をご覧ください。

## 📄 ライセンス

MIT License

---

**楽しいゲームプレイをお楽しみください！** 🎮✨
