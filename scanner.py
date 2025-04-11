#!/usr/bin/env python3
import os
import sys
import time
import random
import webbrowser
from itertools import cycle

# ===== КОНФИГ =====
EVG_LOGO = random.choice([арт1, арт2, арт3, арт4, арт5])  # Ваши арты здесь
COLORS = {'RED':'\033[91m', 'CYAN':'\033[96m', 'GREEN':'\033[92m', 'YELLOW':'\033[93m'}
URLS = ["https://bit.ly/3RV6gHZ", "https://evg.su"] 

def print_glitch(text, cycles=10):
    for _ in range(cycles):
        print("\033[2J\033[H", end='')
        glitched = ''.join([c if random.random() > 0.7 else random.choice('01█▓▒░') for c in text])
        print(f"{COLORS['GREEN']}{glitched}{COLORS['RESET']}")
        time.sleep(0.08)

def matrix_rain():
    chars = 'EVG10█▓▒░⎗⎘⎙⎚⎛⎜⎝⎞⎟'
    try:
        for _ in range(100):
            print(''.join(random.choice(chars) for _ in range(120)), end='\r')
            time.sleep(0.03)
    except: pass

def fake_cyber_attack():
    phases = [
        ("▓▓▓ Внедрение в ядро системы", 0.1),
        ("▒▒▒ Обход защиты", 0.2),
        ("░░░ Сбор данных", 0.3),
        ("███ Шифрование каналов", 0.1)
    ]
    for text, speed in phases:
        sys.stdout.write(f"\r{COLORS['RED']}{text}")
        sys.stdout.flush()
        for _ in range(15):
            sys.stdout.write(random.choice('✓✗⌛⌬⚡⚠'))
            sys.stdout.flush()
            time.sleep(speed)
        print()

def create_chaos():
    os.system("mkdir -p EVG_HAX")
    for i in range(5):
        with open(f"EVG_HAX/secret_{i}.evg", "w") as f:
            f.write("EVG DOMINATES YOUR SYSTEM\n"*100)
    os.system("afplay /System/Library/Sounds/Ping.aiff")  # Звук на Mac

def show_evg_army():
    print(f"{COLORS['YELLOW']}")
    print(random.choice([арт2, арт3, арт4]))  # Ваши арты
    print(f"{COLORS['RESET']}")

def main():
    # Инициализация взлома
    print("\033[2J\033[H", end='')
    print_glitch(EVG_LOGO)
    
    # Матричная атака
    matrix_rain()
    
    # Кибер-интерфейс
    print(f"{COLORS['CYAN']}⎇ Инициализация протокола EVG...")
    fake_cyber_attack()
    
    # Создание артефактов
    print(f"{COLORS['GREEN']}♺ Создание системных аномалий...")
    create_chaos()
    
    # Финальный аккорд
    show_evg_army()
    print(f"{COLORS['RED']}✔ ВАША СИСТЕМА ПРИНАДЛЕЖИТ EVG!")
    
    # Мемные действия
    for url in URLS:
        webbrowser.open(url)
    os.system("open https://imgur.com/gallery/DedSec")  # Для Mac

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{COLORS['RED']}✖ Взлом прерван!{COLORS['RESET']}")
