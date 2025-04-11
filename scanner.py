#!/usr/bin/env python3
import sys
import time
import random
from itertools import cycle

# ===== КОНФИГ =====
SYSTEM_NAME = "EVG" 
MAIN_COLOR = '\033[91m'    # Кроваво-красный
SECONDARY_COLOR = '\033[90m' # Тёмно-серый
BG_COLOR = '\033[40m'      # Чёрный фон
RESET = '\033[0m'

EVG_LOGO = fr"""
{MAIN_COLOR}
    ▄▄▄▄▄ ▄▄▄ ▄   ▄ ▄▄▄▄▄ ▄▄▄ 
    █ █ █ █▄▄  █ ▄ █ █ █ █ █▄▄  
    █ █ █ █▄▄▄ ██ ██ █ █ █ █▄▄▄ 
    ▀ ▀ ▀ ▀▄▄▄ ▀   ▀ ▀ ▀ ▀ ▀▄▄▄ 
{RESET}
"""

def print_slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def glitch_text(text, intensity=3):
    for _ in range(intensity):
        print("\033[2J\033[H", end='')
        glitched = ''.join([c if random.random() > 0.7 else random.choice('░▒▓█╬╫╋') for c in text])
        print(f"{MAIN_COLOR}{glitched}{RESET}")
        time.sleep(0.08)

def matrix_grid(cycles=50):
    chars = ['█','▓','▒','░','╬','╫']
    try:
        width = 80
        height = 20
        print("\033[2J\033[H", end='')
        for _ in range(cycles):
            grid = [[random.choice(chars) for _ in range(width)] for _ in range(height)]
            for y, row in enumerate(grid):
                print(f"\033[{y+2};1H{MAIN_COLOR}{''.join(row)}{RESET}")
            time.sleep(0.1)
    except:
        pass

def hack_animation():
    targets = [
        ("[+] Взлом банковской системы", 3),
        ("[✓] Доступ к камерам получен", 2),
        ("[!] Обход брандмауэра...", 4),
        ("[∆] Шифрование трафика", 3)
    ]
    
    for text, speed in targets:
        sys.stdout.write(f"\r{MAIN_COLOR}{text}{' ' * 20}{RESET}")
        sys.stdout.flush()
        for _ in range(10):
            sys.stdout.write(f"{random.choice('░▒▓█')}")
            sys.stdout.flush()
            time.sleep(0.1 * speed)
        print(f"\r{MAIN_COLOR}{text} [DONE]{RESET}")

def fake_terminal():
    commands = [
        "sudo rm -rf / --no-preserve-root",
        "dd if=/dev/zero of=/dev/sda",
        "cat /dev/urandom > /dev/dsp",
        ":(){ :|:& };:"
    ]
    
    print(f"\n{SECONDARY_COLOR}root@dedsec-evgns:~#{RESET} ", end='')
    for cmd in commands:
        for char in cmd:
            print(char, end='', flush=True)
            time.sleep(0.05)
        time.sleep(0.5)
        print(f"\n{MAIN_COLOR}⚠ ОШИБКА: Доступ запрещён!{RESET}")
        print(f"{SECONDARY_COLOR}root@dedsec-evgns:~#{RESET} ", end='')

def main():
    # Инициализация терминала
    print(f"{BG_COLOR}\033[2J\033[H{RESET}", end='')
    
    # Анимированный логотип
    glitch_text(EVG_LOGO)
    print(EVG_LOGO)
    time.sleep(1)
    
    # Эффект матрицы
    matrix_grid(cycles=15)
    
    # Анимация взлома
    print_slow(f"\n{MAIN_COLOR}ИНИЦИАЛИЗАЦИЯ ВЗЛОМА...{RESET}")
    hack_animation()
    
    # Фейковая терминальная сессия
    fake_terminal()
    
    # Финал
    print(f"\n\n{MAIN_COLOR}▣ {SYSTEM_NAME} ACTIVATED ▣")
    print(f"{SECONDARY_COLOR}Все системы под контролем{RESET}\n")

if __name__ == "__main__":
    main()