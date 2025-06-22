import pygame
import random
import sys
import math

# Pygameの初期化
pygame.init()

# 画面設定
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("刺身たんぽぽゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 100)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)

# ゲーム設定
FPS = 60
BASE_CONVEYOR_SPEED = 2
BASE_TANPOPO_FALL_SPEED = 3
TANPOPO_DROP_X = SCREEN_WIDTH // 2

# 難易度調整設定
LEVEL_UP_SCORE_INTERVAL = 50  # 50ポイントごとにレベルアップ
MAX_SPEED_MULTIPLIER = 3.0    # 最大速度倍率
MIN_SPAWN_INTERVAL = 30       # 最小出現間隔（0.5秒）
BASE_SPAWN_INTERVAL = 120     # 基本出現間隔（2秒）

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
    
    def draw_tanpopo(self, screen, x, y):
        # たんぽぽの花（黄色い円）
        pygame.draw.circle(screen, YELLOW, (int(x), int(y)), 8)
        # たんぽぽの茎（緑の線）
        pygame.draw.line(screen, GREEN, (int(x), int(y)), (int(x), int(y + 15)), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class Tanpopo:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 8
        
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        # たんぽぽの花（黄色い円）
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        # たんぽぽの茎（緑の線）
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x), int(self.y + 15)), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.sashimi_packs = []
        self.tanpopos = []
        self.pack_spawn_timer = 0
        
        # レベルアップエフェクト用
        self.level_up_timer = 0
        self.level_up_effect = False
        
        # 難易度調整用の計算済み値
        self.current_conveyor_speed = BASE_CONVEYOR_SPEED
        self.current_tanpopo_speed = BASE_TANPOPO_FALL_SPEED
        self.current_spawn_interval = BASE_SPAWN_INTERVAL
        
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
        
    def spawn_sashimi_pack(self):
        pack = SashimiPack(self.current_conveyor_speed)
        self.sashimi_packs.append(pack)
    
    def handle_click(self, pos):
        # クリック位置に関係なく、特定の場所からたんぽぽを落とす
        tanpopo = Tanpopo(TANPOPO_DROP_X, 50, self.current_tanpopo_speed)
        self.tanpopos.append(tanpopo)
    
    def check_collisions(self):
        for tanpopo in self.tanpopos[:]:
            for pack in self.sashimi_packs:
                if (tanpopo.get_rect().colliderect(pack.get_rect()) and 
                    not pack.has_tanpopo):
                    # たんぽぽがパックに乗った
                    pack.has_tanpopo = True
                    pack.tanpopo_x = tanpopo.x
                    pack.tanpopo_y = pack.y - 10  # パックの上に配置
                    self.tanpopos.remove(tanpopo)
                    break
    
    def update(self):
        # 難易度調整
        self.calculate_difficulty()
        
        # レベルアップエフェクトタイマー更新
        if self.level_up_effect:
            self.level_up_timer -= 1
            if self.level_up_timer <= 0:
                self.level_up_effect = False
        
        # 刺身パックの生成
        self.pack_spawn_timer += 1
        if self.pack_spawn_timer >= self.current_spawn_interval:
            self.spawn_sashimi_pack()
            self.pack_spawn_timer = 0
        
        # 刺身パックの更新
        for pack in self.sashimi_packs[:]:
            pack.update()
            if pack.is_off_screen():
                if pack.has_tanpopo:
                    self.score += 10  # たんぽぽが乗った状態で左に消えるとポイント加算
                self.sashimi_packs.remove(pack)
        
        # たんぽぽの更新
        for tanpopo in self.tanpopos[:]:
            tanpopo.update()
            if tanpopo.is_off_screen():
                self.tanpopos.remove(tanpopo)
        
        # 衝突判定
        self.check_collisions()
    
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
    
    def draw(self, screen):
        screen.fill(WHITE)
        
        # ベルトコンベアの描画
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - 180, SCREEN_WIDTH, 60))
        
        # 刺身パックの描画
        for pack in self.sashimi_packs:
            pack.draw(screen)
        
        # 落下中のたんぽぽの描画
        for tanpopo in self.tanpopos:
            tanpopo.draw(screen)
        
        # たんぽぽドロップ位置の表示
        pygame.draw.line(screen, BLACK, (TANPOPO_DROP_X, 0), (TANPOPO_DROP_X, 100), 2)
        pygame.draw.circle(screen, GREEN, (TANPOPO_DROP_X, 30), 5)
        
        # UI情報の表示
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        screen.blit(level_text, (10, 50))
        
        speed_text = self.font.render(f"Speed: {self.current_conveyor_speed:.1f}x", True, BLACK)
        screen.blit(speed_text, (10, 90))
        
        # 次のレベルまでのポイント表示
        points_to_next = LEVEL_UP_SCORE_INTERVAL - (self.score % LEVEL_UP_SCORE_INTERVAL)
        next_level_text = self.font.render(f"Next Level: {points_to_next} pts", True, BLACK)
        screen.blit(next_level_text, (10, 130))
        
        # 操作説明の表示
        instruction_text = self.font.render("Click anywhere to drop tanpopo!", True, BLACK)
        screen.blit(instruction_text, (10, SCREEN_HEIGHT - 40))
        
        # レベルアップエフェクト
        self.draw_level_up_effect(screen)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        self.handle_click(event.pos)
            
            self.update()
            self.draw(screen)
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
