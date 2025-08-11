import pygame
import random
import math
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)

class Tank:
    def __init__(self, x, y, color, is_player=True):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0
        self.speed = 3
        self.size = 20
        self.health = 100
        self.is_player = is_player
        self.bullets = []
        self.reload_time = 0
        self.max_reload_time = 20
        
    def draw(self, screen):
        # 绘制坦克主体
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # 绘制坦克炮管
        end_x = self.x + math.cos(math.radians(self.angle)) * (self.size + 10)
        end_y = self.y - math.sin(math.radians(self.angle)) * (self.size + 10)
        pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 4)
        
        # 绘制血条
        health_width = 40
        health_height = 5
        health_x = self.x - health_width // 2
        health_y = self.y - self.size - 15
        
        # 血条背景
        pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
        # 当前血量
        current_health_width = int((self.health / 100) * health_width)
        pygame.draw.rect(screen, GREEN, (health_x, health_y, current_health_width, health_height))
        
    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 边界检查
        if new_x >= self.size and new_x <= SCREEN_WIDTH - self.size:
            self.x = new_x
        if new_y >= self.size and new_y <= SCREEN_HEIGHT - self.size:
            self.y = new_y
            
    def rotate(self, angle_change):
        self.angle += angle_change
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
            
    def shoot(self):
        if self.reload_time <= 0:
            # 计算子弹起始位置
            bullet_x = self.x + math.cos(math.radians(self.angle)) * (self.size + 15)
            bullet_y = self.y - math.sin(math.radians(self.angle)) * (self.size + 15)
            
            # 计算子弹速度
            bullet_dx = math.cos(math.radians(self.angle)) * 8
            bullet_dy = -math.sin(math.radians(self.angle)) * 8
            
            self.bullets.append(Bullet(bullet_x, bullet_y, bullet_dx, bullet_dy))
            self.reload_time = self.max_reload_time
            
    def update(self):
        if self.reload_time > 0:
            self.reload_time -= 1
            
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            
    def is_alive(self):
        return self.health > 0

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = 3
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
                
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("坦克大战")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 创建玩家坦克
        self.player = Tank(100, SCREEN_HEIGHT // 2, BLUE, True)
        
        # 创建敌方坦克
        self.enemies = []
        for i in range(3):
            enemy = Tank(random.randint(600, 750), 
                        random.randint(50, SCREEN_HEIGHT - 50), 
                        RED, False)
            self.enemies.append(enemy)
            
        # 创建障碍物
        self.obstacles = []
        for i in range(5):
            x = random.randint(200, 600)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            width = random.randint(30, 80)
            height = random.randint(30, 80)
            self.obstacles.append(Obstacle(x, y, width, height))
            
        # 游戏状态
        self.score = 0
        self.game_over = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
                    
    def update(self):
        if self.game_over:
            return
            
        # 玩家输入处理
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(0, -1)
        if keys[pygame.K_s]:
            self.player.move(0, 1)
        if keys[pygame.K_a]:
            self.player.move(-1, 0)
        if keys[pygame.K_d]:
            self.player.move(1, 0)
        if keys[pygame.K_LEFT]:
            self.player.rotate(-3)
        if keys[pygame.K_RIGHT]:
            self.player.rotate(3)
            
        # 更新玩家
        self.player.update()
        
        # 更新敌方坦克
        for enemy in self.enemies:
            if enemy.is_alive():
                self.update_enemy(enemy)
                enemy.update()
                
        # 检测碰撞
        self.check_collisions()
        
        # 检查游戏结束条件
        if not self.player.is_alive():
            self.game_over = True
        elif all(not enemy.is_alive() for enemy in self.enemies):
            self.game_over = True
            
    def update_enemy(self, enemy):
        # 简单的AI：随机移动和射击
        if random.random() < 0.02:  # 2%概率改变方向
            enemy.angle = random.randint(0, 360)
            
        # 移动
        dx = math.cos(math.radians(enemy.angle))
        dy = -math.sin(math.radians(enemy.angle))
        enemy.move(dx, dy)
        
        # 射击
        if random.random() < 0.01:  # 1%概率射击
            enemy.shoot()
            
    def check_collisions(self):
        # 检查玩家子弹与敌人的碰撞
        for bullet in self.player.bullets[:]:
            bullet_rect = bullet.get_rect()
            
            # 与障碍物碰撞
            for obstacle in self.obstacles:
                if bullet_rect.colliderect(obstacle.rect):
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    break
                    
            # 与敌人碰撞
            for enemy in self.enemies:
                if enemy.is_alive():
                    enemy_rect = pygame.Rect(enemy.x - enemy.size, enemy.y - enemy.size,
                                           enemy.size * 2, enemy.size * 2)
                    if bullet_rect.colliderect(enemy_rect):
                        enemy.take_damage(25)
                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)
                        self.score += 10
                        break
                        
        # 检查敌人子弹与玩家的碰撞
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                bullet_rect = bullet.get_rect()
                
                # 与障碍物碰撞
                for obstacle in self.obstacles:
                    if bullet_rect.colliderect(obstacle.rect):
                        if bullet in enemy.bullets:
                            enemy.bullets.remove(bullet)
                        break
                        
                # 与玩家碰撞
                player_rect = pygame.Rect(self.player.x - self.player.size, 
                                        self.player.y - self.player.size,
                                        self.player.size * 2, self.player.size * 2)
                if bullet_rect.colliderect(player_rect):
                    self.player.take_damage(20)
                    if bullet in enemy.bullets:
                        enemy.bullets.remove(bullet)
                    break
                    
    def draw(self):
        self.screen.fill(BLACK)
        
        # 绘制障碍物
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # 绘制玩家
        if self.player.is_alive():
            self.player.draw(self.screen)
            for bullet in self.player.bullets:
                bullet.draw(self.screen)
                
        # 绘制敌人
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.draw(self.screen)
                for bullet in enemy.bullets:
                    bullet.draw(self.screen)
                    
        # 绘制UI
        self.draw_ui()
        
        pygame.display.flip()
        
    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        
        # 显示分数
        score_text = font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 显示玩家血量
        health_text = font.render(f"血量: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (10, 50))
        
        # 显示存活敌人数量
        alive_enemies = sum(1 for enemy in self.enemies if enemy.is_alive())
        enemies_text = font.render(f"敌人: {alive_enemies}", True, WHITE)
        self.screen.blit(enemies_text, (10, 90))
        
        # 游戏结束显示
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            if self.player.is_alive():
                game_over_text = game_over_font.render("胜利!", True, GREEN)
            else:
                game_over_text = game_over_font.render("失败!", True, RED)
                
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("按R键重新开始", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        # 显示控制说明
        controls_font = pygame.font.Font(None, 24)
        controls = [
            "控制说明:",
            "WASD - 移动",
            "方向键 - 旋转",
            "空格 - 射击",
            "R - 重新开始"
        ]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, GRAY)
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, 10 + i * 25))
            
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()