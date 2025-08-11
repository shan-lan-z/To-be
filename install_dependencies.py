#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坦克大战游戏依赖安装脚本
适用于qPython环境
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ {package} 安装失败")
        return False

def check_package(package):
    """检查包是否已安装"""
    try:
        __import__(package)
        print(f"✓ {package} 已安装")
        return True
    except ImportError:
        print(f"✗ {package} 未安装")
        return False

def main():
    print("=" * 50)
    print("坦克大战游戏依赖安装程序")
    print("=" * 50)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 需要安装的包
    packages = [
        ("pygame", "pygame==2.5.2"),
        ("tkinter", "tkinter")  # tkinter通常是Python内置的
    ]
    
    success_count = 0
    
    for package_name, package_install in packages:
        print(f"\n检查 {package_name}...")
        
        if check_package(package_name):
            success_count += 1
        else:
            if package_name != "tkinter":  # tkinter是内置的，不需要pip安装
                if install_package(package_install):
                    success_count += 1
            else:
                print("tkinter是Python内置模块，如果无法导入，请检查Python安装")
    
    print("\n" + "=" * 50)
    print("安装结果:")
    print(f"成功安装: {success_count}/{len(packages)} 个包")
    
    if success_count == len(packages):
        print("✓ 所有依赖安装完成！")
        print("\n现在可以运行游戏了:")
        print("1. 运行 pygame版本: python tank_battle.py")
        print("2. 运行 tkinter版本: python tank_battle_simple.py")
    else:
        print("⚠ 部分依赖安装失败")
        print("建议尝试运行 tkinter版本的游戏")
    
    print("=" * 50)

if __name__ == "__main__":
    main()