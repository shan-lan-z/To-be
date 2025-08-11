import tkinter as tk
from tkinter import messagebox
import random
import math

print("Starting Tank Battle Game...")

class TankGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tank Battle")
        self.root.geometry("600x400")
        
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='black')
        self.canvas.pack()
        
        # Player tank
        self.player_x = 100
        self.player_y = 200
        self.player_angle = 0
        self.player_health = 100
        self.player_bullets = []
        
        # Enemy tank
        self.enemy_x = 500
        self.enemy_y = 200
        self.enemy_health = 100
        self.enemy_bullets = []
        
        # Game state
        self.score = 0
        self.game_running = True
        
        # Bind keys
        self.root.bind('<KeyPress>', self.on_key_press)
        self.keys_pressed = set()
        
        # Start game loop
        self.game_loop()
        
    def on_key_press(self, event):
        self.keys_pressed.add(event.keysym.lower())
        
    def move_player(self):
        speed = 3
        if 'w' in self.keys_pressed:
            self.player_y -= speed
        if 's' in self.keys_pressed:
            self.player_y += speed
        if 'a' in self.keys_pressed:
            self.player_x -= speed
        if 'd' in self.keys_pressed:
            self.player_x += speed
        if 'left' in self.keys_pressed:
            self.player_angle -= 5
        if 'right' in self.keys_pressed:
            self.player_angle += 5
        if 'space' in self.keys_pressed:
            self.shoot_player()
            
        # Keep player in bounds
        self.player_x = max(20, min(580, self.player_x))
        self.player_y = max(20, min(380, self.player_y))
        
    def shoot_player(self):
        if len(self.player_bullets) < 2:
            angle_rad = math.radians(self.player_angle)
            bullet = {
                'x': self.player_x + math.cos(angle_rad) * 25,
                'y': self.player_y - math.sin(angle_rad) * 25,
                'dx': math.cos(angle_rad) * 8,
                'dy': -math.sin(angle_rad) * 8
            }
            self.player_bullets.append(bullet)
            
    def update_bullets(self):
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            if bullet['x'] < 0 or bullet['x'] > 600 or bullet['y'] < 0 or bullet['y'] > 400:
                self.player_bullets.remove(bullet)
                
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            if bullet['x'] < 0 or bullet['x'] > 600 or bullet['y'] < 0 or bullet['y'] > 400:
                self.enemy_bullets.remove(bullet)
                
    def check_collisions(self):
        # Check player bullets hitting enemy
        for bullet in self.player_bullets[:]:
            distance = math.sqrt((bullet['x'] - self.enemy_x)**2 + (bullet['y'] - self.enemy_y)**2)
            if distance < 20:
                self.enemy_health -= 25
                self.player_bullets.remove(bullet)
                self.score += 10
                
        # Check enemy bullets hitting player
        for bullet in self.enemy_bullets[:]:
            distance = math.sqrt((bullet['x'] - self.player_x)**2 + (bullet['y'] - self.player_y)**2)
            if distance < 20:
                self.player_health -= 20
                self.enemy_bullets.remove(bullet)
                
    def update_enemy(self):
        if self.enemy_health > 0:
            # Simple enemy AI
            if random.random() < 0.02:
                # Shoot at player
                dx = self.player_x - self.enemy_x
                dy = self.player_y - self.enemy_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance > 0:
                    bullet = {
                        'x': self.enemy_x,
                        'y': self.enemy_y,
                        'dx': (dx/distance) * 5,
                        'dy': (dy/distance) * 5
                    }
                    self.enemy_bullets.append(bullet)
                    
    def draw_tank(self, x, y, color, health):
        # Draw tank body
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, outline='white')
        
        # Draw health bar
        health_width = 30
        health_height = 4
        health_x = x - health_width//2
        health_y = y - 25
        
        self.canvas.create_rectangle(health_x, health_y, health_x + health_width, health_y + health_height, fill='red')
        current_health = int((health/100) * health_width)
        self.canvas.create_rectangle(health_x, health_y, health_x + current_health, health_y + health_height, fill='green')
        
    def draw_bullets(self, bullets):
        for bullet in bullets:
            self.canvas.create_oval(bullet['x']-2, bullet['y']-2, bullet['x']+2, bullet['y']+2, fill='white')
            
    def draw_ui(self):
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill='white', font=('Arial', 12))
        self.canvas.create_text(50, 40, text=f"Health: {self.player_health}", fill='white', font=('Arial', 12))
        
        # Controls
        self.canvas.create_text(500, 20, text="WASD: Move", fill='gray', font=('Arial', 10))
        self.canvas.create_text(500, 35, text="Arrows: Rotate", fill='gray', font=('Arial', 10))
        self.canvas.create_text(500, 50, text="Space: Shoot", fill='gray', font=('Arial', 10))
        
    def check_game_over(self):
        if self.player_health <= 0:
            self.game_running = False
            messagebox.showinfo("Game Over", f"You Lost! Score: {self.score}")
            self.root.quit()
        elif self.enemy_health <= 0:
            self.game_running = False
            messagebox.showinfo("Game Over", f"You Won! Score: {self.score}")
            self.root.quit()
            
    def game_loop(self):
        if not self.game_running:
            return
            
        self.canvas.delete('all')
        
        self.move_player()
        self.update_bullets()
        self.update_enemy()
        self.check_collisions()
        self.check_game_over()
        
        # Draw everything
        if self.player_health > 0:
            self.draw_tank(self.player_x, self.player_y, 'blue', self.player_health)
        if self.enemy_health > 0:
            self.draw_tank(self.enemy_x, self.enemy_y, 'red', self.enemy_health)
            
        self.draw_bullets(self.player_bullets)
        self.draw_bullets(self.enemy_bullets)
        self.draw_ui()
        
        self.root.after(50, self.game_loop)
        
    def run(self):
        self.root.mainloop()

print("Creating game...")
game = TankGame()
print("Starting game...")
game.run()