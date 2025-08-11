#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qPython环境测试文件
"""

print("=" * 50)
print("qPython环境测试")
print("=" * 50)

# 测试基本Python功能
print("1. 测试基本Python功能...")
try:
    import math
    import random
    print("✓ 基本模块导入成功")
except Exception as e:
    print(f"✗ 基本模块导入失败: {e}")

# 测试tkinter
print("\n2. 测试tkinter...")
try:
    import tkinter as tk
    print("✓ tkinter导入成功")
    
    # 创建简单窗口测试
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口
    root.destroy()
    print("✓ tkinter窗口创建成功")
    
except Exception as e:
    print(f"✗ tkinter测试失败: {e}")

# 测试数学计算
print("\n3. 测试数学计算...")
try:
    result = math.sqrt(16)
    print(f"✓ 数学计算成功: √16 = {result}")
except Exception as e:
    print(f"✗ 数学计算失败: {e}")

# 测试随机数
print("\n4. 测试随机数...")
try:
    rand_num = random.randint(1, 100)
    print(f"✓ 随机数生成成功: {rand_num}")
except Exception as e:
    print(f"✗ 随机数生成失败: {e}")

print("\n" + "=" * 50)
print("测试完成！")
print("如果所有测试都通过，可以运行坦克大战游戏")
print("运行命令: python start_game.py")
print("=" * 50)