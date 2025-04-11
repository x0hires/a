#!/usr/bin/env python3
import os
import sys
import time
import random
import webbrowser
from itertools import cycle

# ===== КОНФИГ =====
EVG_ART = [r"""
 ███████╗██╗   ██╗ ██████╗ 
 ██╔════╝██║   ██║██╔════╝ 
 █████╗  ██║   ██║██║      
 ██╔══╝  ╚██╗ ██╔╝██║      
 ███████╗ ╚████╔╝ ╚██████╗ 
 ╚══════╝  ╚═══╝   ╚═════╝""",
 
r"""
╔═╗╦  ╦╔═╗╔═╗
║  ║  ║║ ║║╣ 
╚═╝╩═╝╩╚═╝╚═╝""",

r"""
▄▄▄▄▄ ▄▄▄ ▄   ▄ ▄▄▄▄▄ ▄▄▄ 
█ █ █ █▄▄  █ ▄ █ █ █ █ █▄▄  
█ █ █ █▄▄▄ ██ ██ █ █ █ █▄▄▄ 
▀ ▀ ▀ ▀▄▄▄ ▀   ▀ ▀ ▀ ▀ ▀▄▄▄"""]

COLORS = {'RED':'\033[91m', 'CYAN':'\033[96m', 'GREEN':'\033[92m'}
RESET = '\033[0m'

def print_rainbow(text):
    colors = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']
    for i, char in enumerate(text):
        print(f"{colors[i%6]}{char}{RESET}", end='', flush=True)
        time.sleep(0.02)
    print()

def matrix_invasion():
    chars = 'EVGevg01█▓▒░'
    try:
        for _ in range(100):
            print(f"{COLORS['GREEN]}{''.join(random.choice(chars) for _ in range(120))}{RESET}")
            time.sleep(0.03)
    except: pass

def animate_evg():
    for art in EVG_ART:
        print("\033[2J\033[H", end='')
        for line in art.split('\n'):
            print_rainbow(line)
            time.sleep(0.1)
        time.sleep(0.5)

def create_chaos():
    os.makedirs("EVG_HAX", exist_ok=True)
    for i in range(3):
        with open(f"EVG_HAX/secret_{i}.txt", "w") as f:
            f.write("EVG WAS HERE\n"*100)

def fake_hack():
    targets = cycle([
        "Взлом пентагона...",
        "Деактивация камер...",
        "Кража биткоинов...",
        "Взлом всех соцсетей..."
    ])
    
    for _ in range(4):
        target = next(targets)
        sys.stdout.write(f"\r{COLORS['RED']}{target}")
        sys.stdout.flush()
        for __ in range(10):
            sys.stdout.write(f" {random.choice('✓✗☠⚠⚡')}")
            sys.stdout.flush()
            time.sleep(0.2)
        print()

def surprise_ending():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    webbrowser.open("https://evg.su")
    print("\n" + COLORS['CYAN'] + "Сюрприз в браузере! 😈" + RESET)

def main():
    print("\033[2J\033[H", end='')  # Очистка экрана
    
    # Мега-анимация
    animate_evg()
    matrix_invasion()
    
    # Хакерский интерфейс
    print_rainbow("\n=== АКТИВАЦИЯ СИСТЕМЫ EVG ===")
    fake_hack()
    
    # Создание артефактов
    print(COLORS['GREEN'] + "\nСоздание файлов взлома..." + RESET)
    create_chaos()
    
    # Финальный аккорд
    time.sleep(1)
    print("\n" + COLORS['RED'] + "✔ ВСЁ ВЗЛОМАНО!")
    time.sleep(2)
    
    # ASCII-маска
    print(r"""
    ╔═╗╔╗╔╔═╗╔╦╗
    ║ ║║║║╠═╣║║║
    ╚═╝╝╚╝╩ ╩╩ ╩
    """)
    
    # Сюрприз
    surprise_ending(https://avatars.mds.yandex.net/i?id=9edd4e89971c26713a9175456d2f91f5_sr-4274912-images-thumbs&n=13)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + COLORS['RED'] + "HACK STOPPED!" + RESET)
