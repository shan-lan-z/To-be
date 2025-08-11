#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坦克大战游戏快速启动脚本
自动检测环境并选择合适的版本运行
"""

import sys
import subprocess

def check_pygame():
    """检查pygame是否可用"""
    try:
        import pygame
        pygame.init()
        pygame.quit()
        return True
    except:
        return False

def check_tkinter():
    """检查tkinter是否可用"""
    try:
        import tkinter
        return True
    except:
        return False

def run_game():
    """运行游戏"""
    print("=" * 50)
    print("坦克大战游戏启动器")
    print("=" * 50)
    
    print("检测游戏环境...")
    
    pygame_available = check_pygame()
    tkinter_available = check_tkinter()
    
    print(f"pygame可用: {'✓' if pygame_available else '✗'}")
    print(f"tkinter可用: {'✓' if tkinter_available else '✗'}")
    
    if pygame_available:
        print("\n启动pygame版本游戏...")
        try:
            subprocess.run([sys.executable, "tank_battle.py"])
        except FileNotFoundError:
            print("错误: 找不到 tank_battle.py 文件")
        except Exception as e:
            print(f"启动pygame版本失败: {e}")
            if tkinter_available:
                print("尝试启动tkinter版本...")
                run_tkinter_version()
    elif tkinter_available:
        print("\n启动tkinter版本游戏...")
        run_tkinter_version()
    else:
        print("\n错误: 没有可用的图形库")
        print("请先安装依赖:")
        print("python install_dependencies.py")
        
def run_tkinter_version():
    """运行tkinter版本游戏"""
    try:
        subprocess.run([sys.executable, "tank_battle_simple.py"])
    except FileNotFoundError:
        print("错误: 找不到 tank_battle_simple.py 文件")
    except Exception as e:
        print(f"启动tkinter版本失败: {e}")

if __name__ == "__main__":
    run_game()