#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坦克大战游戏 - qPython专用启动器
简化版本，直接启动tkinter游戏
"""

print("=" * 50)
print("坦克大战游戏启动中...")
print("=" * 50)

try:
    # 直接导入并运行tkinter版本
    print("正在启动游戏...")
    
    # 导入游戏模块
    import tkinter as tk
    from tkinter import messagebox
    import random
    import math
    
    print("✓ 依赖检查通过")
    
    # 游戏类定义
    class TankBattleGame:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("坦克大战")
            self.root.geometry("800x600")
            self.root.resizable(False, False)
            
            # 游戏变量
            self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
            self.canvas.pack()
            
            # 游戏状态
            self.game_running = True
            self.score = 0
            
            # 玩家坦克
            self.player = {
                'x': 100,
                'y': 300,
                'angle': 0,
                'health': 100,
                'bullets': []
            }
            
            # 敌方坦克
            self.enemies = []
            for i in range(3):
                self.enemies.append({
                    'x': random.randint(600, 750),
                    'y': random.randint(100, 500),
                    'angle': random.randint(0, 360),
                    'health': 100,
                    'bullets': []
                })
            
            # 障碍物
            self.obstacles = []
            for i in range(5):
                self.obstacles.append({
                    'x': random.randint(200, 600),
                    'y': random.randint(100, 500),
                    'width': random.randint(30, 80),
                    'height': random.randint(30, 80)
                })
            
            # 绑定按键
            self.root.bind('<KeyPress>', self.on_key_press)
            self.root.bind('<KeyRelease>', self.on_key_release)
            
            # 按键状态
            self.keys_pressed = set()
            
            # 开始游戏循环
            self.game_loop()
            
        def on_key_press(self, event):
            self.keys_pressed.add(event.keysym.lower())
            
        def on_key_release(self, event):
            self.keys_pressed.discard(event.keysym.lower())
            
        def move_player(self):
            speed = 5
            if 'w' in self.keys_pressed:
                self.player['y'] -= speed
            if 's' in self.keys_pressed:
                self.player['y'] += speed
            if 'a' in self.keys_pressed:
                self.player['x'] -= speed
            if 'd' in self.keys_pressed:
                self.player['x'] += speed
            if 'left' in self.keys_pressed:
                self.player['angle'] -= 5
            if 'right' in self.keys_pressed:
                self.player['angle'] += 5
            if 'space' in self.keys_pressed:
                self.shoot(self.player)
                
            # 边界检查
            self.player['x'] = max(20, min(780, self.player['x']))
            self.player['y'] = max(20, min(580, self.player['y']))
            
        def shoot(self, tank):
            if len(tank['bullets']) < 3:
                angle_rad = math.radians(tank['angle'])
                bullet = {
                    'x': tank['x'] + math.cos(angle_rad) * 30,
                    'y': tank['y'] - math.sin(angle_rad) * 30,
                    'dx': math.cos(angle_rad) * 10,
                    'dy': -math.sin(angle_rad) * 10
                }
                tank['bullets'].append(bullet)
                
        def update_bullets(self, tank):
            for bullet in tank['bullets'][:]:
                bullet['x'] += bullet['dx']
                bullet['y'] += bullet['dy']
                
                if (bullet['x'] < 0 or bullet['x'] > 800 or 
                    bullet['y'] < 0 or bullet['y'] > 600):
                    tank['bullets'].remove(bullet)
                    
        def check_collisions(self):
            # 检查玩家子弹与敌人碰撞
            for bullet in self.player['bullets'][:]:
                for enemy in self.enemies[:]:
                    if enemy['health'] > 0:
                        distance = math.sqrt((bullet['x'] - enemy['x'])**2 + 
                                           (bullet['y'] - enemy['y'])**2)
                        if distance < 25:
                            enemy['health'] -= 25
                            if bullet in self.player['bullets']:
                                self.player['bullets'].remove(bullet)
                            self.score += 10
                            if enemy['health'] <= 0:
                                self.enemies.remove(enemy)
                            break
                            
            # 检查敌人子弹与玩家碰撞
            for enemy in self.enemies:
                for bullet in enemy['bullets'][:]:
                    distance = math.sqrt((bullet['x'] - self.player['x'])**2 + 
                                       (bullet['y'] - self.player['y'])**2)
                    if distance < 25:
                        self.player['health'] -= 20
                        if bullet in enemy['bullets']:
                            enemy['bullets'].remove(bullet)
                        break
                        
        def update_enemies(self):
            for enemy in self.enemies:
                if enemy['health'] > 0:
                    if random.random() < 0.02:
                        enemy['angle'] = random.randint(0, 360)
                        
                    angle_rad = math.radians(enemy['angle'])
                    enemy['x'] += math.cos(angle_rad) * 2
                    enemy['y'] -= math.sin(angle_rad) * 2
                    
                    enemy['x'] = max(20, min(780, enemy['x']))
                    enemy['y'] = max(20, min(580, enemy['y']))
                    
                    if random.random() < 0.01:
                        self.shoot(enemy)
                        
        def draw_tank(self, tank, color):
            if tank['health'] <= 0:
                return
                
            self.canvas.create_oval(tank['x']-20, tank['y']-20, 
                                   tank['x']+20, tank['y']+20, 
                                   fill=color, outline='white')
            
            angle_rad = math.radians(tank['angle'])
            end_x = tank['x'] + math.cos(angle_rad) * 30
            end_y = tank['y'] - math.sin(angle_rad) * 30
            self.canvas.create_line(tank['x'], tank['y'], end_x, end_y, 
                                   fill=color, width=4)
            
            # 血条
            health_width = 40
            health_height = 5
            health_x = tank['x'] - health_width // 2
            health_y = tank['y'] - 35
            
            self.canvas.create_rectangle(health_x, health_y, 
                                        health_x + health_width, health_y + health_height,
                                        fill='red', outline='white')
            current_health_width = int((tank['health'] / 100) * health_width)
            self.canvas.create_rectangle(health_x, health_y,
                                        health_x + current_health_width, health_y + health_height,
                                        fill='green', outline='')
                                        
        def draw_bullets(self, tank):
            for bullet in tank['bullets']:
                self.canvas.create_oval(bullet['x']-3, bullet['y']-3,
                                       bullet['x']+3, bullet['y']+3,
                                       fill='white', outline='')
                                       
        def draw_obstacles(self):
            for obstacle in self.obstacles:
                self.canvas.create_rectangle(obstacle['x'], obstacle['y'],
                                            obstacle['x'] + obstacle['width'],
                                            obstacle['y'] + obstacle['height'],
                                            fill='brown', outline='white')
                                            
        def draw_ui(self):
            self.canvas.create_text(70, 30, text=f"分数: {self.score}", 
                                   fill='white', font=('Arial', 16))
            
            self.canvas.create_text(70, 60, text=f"血量: {self.player['health']}", 
                                   fill='white', font=('Arial', 16))
            
            alive_enemies = sum(1 for enemy in self.enemies if enemy['health'] > 0)
            self.canvas.create_text(70, 90, text=f"敌人: {alive_enemies}", 
                                   fill='white', font=('Arial', 16))
            
            controls = [
                "控制说明:",
                "WASD - 移动",
                "方向键 - 旋转",
                "空格 - 射击"
            ]
            
            for i, control in enumerate(controls):
                self.canvas.create_text(650, 30 + i * 20, text=control,
                                       fill='gray', font=('Arial', 12), anchor='w')
                                       
        def check_game_over(self):
            if self.player['health'] <= 0:
                self.game_running = False
                messagebox.showinfo("游戏结束", f"游戏失败！\n最终分数: {self.score}")
                self.root.quit()
            elif all(enemy['health'] <= 0 for enemy in self.enemies):
                self.game_running = False
                messagebox.showinfo("游戏结束", f"胜利！\n最终分数: {self.score}")
                self.root.quit()
                
        def game_loop(self):
            if not self.game_running:
                return
                
            self.canvas.delete('all')
            
            self.move_player()
            self.update_bullets(self.player)
            
            for enemy in self.enemies:
                self.update_bullets(enemy)
                
            self.update_enemies()
            self.check_collisions()
            self.check_game_over()
            
            self.draw_obstacles()
            self.draw_tank(self.player, 'blue')
            self.draw_bullets(self.player)
            
            for enemy in self.enemies:
                self.draw_tank(enemy, 'red')
                self.draw_bullets(enemy)
                
            self.draw_ui()
            
            self.root.after(50, self.game_loop)
            
        def run(self):
            self.root.mainloop()
    
    # 启动游戏
    print("✓ 游戏初始化完成")
    print("游戏控制:")
    print("- WASD: 移动坦克")
    print("- 方向键: 旋转炮管")
    print("- 空格: 发射子弹")
    print("=" * 50)
    
    game = TankBattleGame()
    game.run()
    
except ImportError as e:
    print(f"✗ 导入错误: {e}")
    print("请确保qPython支持tkinter")
    
except Exception as e:
    print(f"✗ 游戏启动失败: {e}")
    print("请检查qPython环境配置")

print("游戏结束")