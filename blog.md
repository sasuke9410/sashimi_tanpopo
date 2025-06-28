# AIと共に作る刺身たんぽぽゲーム開発記

## 選んだゲームとその理由

- **ゲーム名**: 刺身たんぽぽゲーム
- **ゲームコンセプト**: ベルトコンベアで流れる刺身パックにたんぽぽを落として乗せるアクションゲーム
- **選択理由**:
  - ユニークで日本的な発想（刺身×たんぽぽの組み合わせ）
  - シンプルなゲームプレイで実装しやすい
  - 段階的に機能を追加できる拡張性
  - 物理演算や複雑なグラフィックが不要
  - プレイヤーのタイミング感覚を試すゲーム性
  - 和風の世界観で視覚的にも面白い

## 効果的なプロンプトテクニック

- **段階的な機能実装**: 基本機能から始めて徐々に複雑な機能を追加
- **具体的な仕様指定**: 画面サイズ、色定義、ゲーム定数を明確に指定
- **日本語でのコミュニケーション**: 自然言語での要求仕様の伝達
- **コード分析の依頼**: 既存コードの機能確認と改善点の特定
- **文書化の自動化**: 実装済み機能の整理と今後の計画策定
- **プロジェクト管理**: ファイル整理、Git操作、開発ログの作成

## AIが古典的なプログラミング課題をどのように処理したか

- **ゲームループの実装**: 
  - イベント処理、更新、描画の基本パターンを適切に構築
  - 60FPSでの安定したフレームレート制御
- **衝突判定システム**: 
  - Pygameの`Rect.colliderect()`を使用した効率的な当たり判定
  - オブジェクト間の相互作用の管理
- **動的難易度調整**: 
  - スコアベースでの段階的な速度上昇システム
  - レベルシステムと連動した複数パラメータの同時調整
- **メモリ管理**: 
  - 画面外オブジェクトの自動削除によるメモリリーク防止
  - リスト内包表記を使った効率的なオブジェクト管理

## 時間を節約した開発自動化の例

- **プロジェクト初期化**: 
  - Gitリポジトリの自動作成とファイル追加
  - 適切な日本語コミットメッセージの生成
- **ファイル管理の自動化**: 
  - 重複ファイルの検出と削除
  - ディレクトリ構造の整理
- **ドキュメント生成**: 
  - 実装済み機能の自動識別とマークアップ
  - 改善案ドキュメントの構造化
- **開発ログの自動作成**: 
  - 作業履歴の整理と記録
  - 次のステップの明確化

## AIが生成した興味深いソリューションのコード例

### 動的難易度調整システム
```python
def calculate_difficulty(self):
    """現在のスコアに基づいて難易度を計算"""
    # レベル計算
    new_level = (self.score // LEVEL_UP_SCORE_INTERVAL) + 1
    
    # レベルアップ検出
    if new_level > self.level:
        self.level = new_level
        self.level_up_effect = True
        self.level_up_timer = 60  # 1秒間エフェクト表示
    
    # 速度倍率計算（レベルに応じて段階的に上昇）
    speed_multiplier = min(1.0 + (self.level - 1) * 0.2, MAX_SPEED_MULTIPLIER)
    
    # 各パラメータの更新
    self.current_conveyor_speed = BASE_CONVEYOR_SPEED * speed_multiplier
    self.current_tanpopo_speed = BASE_TANPOPO_FALL_SPEED * speed_multiplier
    
    # 出現間隔の短縮（レベルが上がるほど短く）
    interval_reduction = (self.level - 1) * 10
    self.current_spawn_interval = max(MIN_SPAWN_INTERVAL, BASE_SPAWN_INTERVAL - interval_reduction)
```

### レベルアップエフェクトシステム
```python
def draw_level_up_effect(self, screen):
    """レベルアップエフェクトを描画"""
    if self.level_up_effect:
        # 背景を少し暗くする
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # レベルアップテキスト
        level_text = self.big_font.render(f"LEVEL {self.level}!", True, GOLD)
        text_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(level_text, text_rect)
        
        # キラキラエフェクト（簡単な星形）
        for i in range(10):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            size = random.randint(3, 8)
            pygame.draw.circle(screen, GOLD, (x, y), size)
```

### オブジェクト指向設計
```python
class SashimiPack:
    def __init__(self, speed):
        self.width = 80
        self.height = 40
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - 150
        self.speed = speed
        self.has_tanpopo = False
        self.tanpopo_x = 0
        self.tanpopo_y = 0
        
    def update(self):
        self.x -= self.speed
        if self.has_tanpopo:
            self.tanpopo_x -= self.speed
    
    def draw(self, screen):
        # 刺身パックを描画
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # たんぽぽが乗っている場合は描画
        if self.has_tanpopo:
            self.draw_tanpopo(screen, self.tanpopo_x, self.tanpopo_y)
```

## 最終作品のスクリーンショットまたはゲームプレイ映像

### 現在の実装状況
- **基本ゲームプレイ**: ✅ 完成
- **ベルトコンベアシステム**: ✅ 完成
- **難易度調整システム**: ✅ 完成
- **レベルアップエフェクト**: ✅ 完成
- **UI表示**: ✅ 完成

### ゲーム画面の構成
```
┌─────────────────────────────────────────────────────────┐
│ Score: 120  Level: 3  Speed: 1.4x  Next Level: 30 pts │
│                                                         │
│                    │ ← たんぽぽ投下位置                    │
│                    ●                                   │
│                                                         │
│                                                         │
│              🌼                                         │
│                                                         │
│ ████████████████████████████████████████████████████████ │ ← ベルトコンベア
│     [刺身🌼]      [刺身]         [刺身]                │
│ ████████████████████████████████████████████████████████ │
│                                                         │
│ Click anywhere to drop tanpopo!                        │
└─────────────────────────────────────────────────────────┘
```

### 今後の実装予定
- **コンボシステム**: 連続成功でボーナス倍率
- **メニューシステム**: タイトル画面とゲームオーバー画面
- **多様な刺身パック**: サイズや種類のバリエーション
- **サウンド効果**: 和風BGMと効果音
- **特別モード**: チャレンジモードとエンドレスモード

---

*このブログ記事は、AIとの協働によるゲーム開発の実体験を記録したものです。技術的な実装だけでなく、プロジェクト管理や文書化まで含めた包括的な開発プロセスを紹介しています。*
