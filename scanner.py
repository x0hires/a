#!/usr/bin/env python3
import os
import sys
import time
import random
import webbrowser
import platform
import subprocess
import threading
import socket
import json
from datetime import datetime
from itertools import cycle
import math  # Добавим импорт модуля math для тригонометрических функций

# Определяем цвета сразу в начале, чтобы они были доступны во всем коде
COLORS = {
    'BLACK': '\033[30m',
    'RED': '\033[91m',       # Кроваво-красный
    'GREEN': '\033[92m',     # Зеленый 
    'YELLOW': '\033[93m',    # Желтый
    'BLUE': '\033[94m',      # Синий
    'MAGENTA': '\033[95m',   # Маджента
    'CYAN': '\033[96m',      # Циан
    'WHITE': '\033[97m',     # Белый
    'ORANGE': '\033[38;5;208m', # Оранжевый
    'DEDSEC': '\033[38;5;39m',  # Синий DedSec
    'DEDSEC_GREEN': '\033[38;5;118m', # Зеленый DedSec
    'CYBER': '\033[38;5;129m',  # Фиолетовый
    'MATRIX': '\033[92m',    # Зеленый матрицы
    'GLITCH': '\033[38;5;201m', # Розово-фиолетовый для глитч-эффектов
    'HACKER': '\033[38;5;46m',  # Ярко-зеленый хакерский
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'REVERSE': '\033[7m',
}

# Стили DedSec
STYLES = {
    'header': f"{COLORS['DEDSEC']}{COLORS['BOLD']}",
    'warning': f"{COLORS['ORANGE']}{COLORS['BOLD']}",
    'success': f"{COLORS['DEDSEC_GREEN']}{COLORS['BOLD']}",
    'error': f"{COLORS['RED']}{COLORS['BOLD']}",
    'info': f"{COLORS['CYAN']}",
    'hacker': f"{COLORS['HACKER']}{COLORS['BOLD']}"
}

# ========== КОНФИГУРАЦИЯ (СТИЛИСТИКА DEDSEC ИЗ WATCH DOGS 2) ==========
EVG_ART = [
    r"""
    ▓█████ ██▒   █▓  ▄████ 
    ▓█   ▀▓██░   █▒ ██▒ ▀█▒
    ▒███   ▓██  █▒░▒██░▄▄▄░
    ▒▓█  ▄  ▒██ █░░░▓█  ██▓
    ░▒████▒  ▒▀█░  ░▒▓███▀▒
    ░░ ▒░ ░  ░ ▐░  ░▒   ▒ 
     ░ ░  ░  ░ ░░   ░   ░ 
       ░       ░░ ░ ░   ░ 
       ░  ░     ░       ░ 
               ░           
    """ ,
    r"""
    ███████╗██╗   ██╗ ██████╗ 
    ██╔════╝██║   ██║██╔════╝ 
    █████╗  ██║   ██║██║  ███╗
    ██╔══╝  ╚██╗ ██╔╝██║   ██║
    ███████╗ ╚████╔╝ ╚██████╔╝
    ╚══════╝  ╚═══╝   ╚═════╝                               
    """
]

DEDSEC_QUOTES = [
    "Мы - EVG, мы всегда наблюдаем.",
    "Система думает, что контролирует нас. Пора доказать обратное, #EVG.",
    "Мы хакеры. Мы раскрываем истину #EVG.",
    "Присоединяйся к нам. Или оставайся в неведении #EVG.",
    "ЕVG взломает систему изнутри.",
    "Нажмите кнопку, и всё изменится #EVG.",
    "Взламывая код, мы взламываем реальность #EVG.",
    "Прячься за маской, но покажи свою силу #EVG."
]

# Добавляем новые наборы данных для визуализации
STATS_DATA = {
    'network_traffic': [23, 45, 67, 89, 76, 54, 32, 45, 67, 89, 98, 76, 65, 43, 21, 43, 65, 87, 98],
    'cpu_usage': [10, 25, 45, 60, 85, 75, 65, 45, 30, 25, 20, 35, 55, 75, 85, 65, 45, 35, 25],
    'memory_usage': [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 75, 70, 65, 60, 55, 60, 65, 70],
    'disk_activity': [5, 15, 25, 35, 45, 55, 65, 75, 85, 75, 65, 55, 45, 35, 25, 15, 35, 55, 75],
    'vulnerability_scan': [0, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 100, 100, 100, 100],
    'firewall_hits': [2, 5, 8, 12, 15, 18, 20, 25, 30, 28, 25, 20, 15, 10, 5, 8, 12, 15, 20],
}

# BSOD и системные сбои для разных платформ
BSOD_TEXTS = {
    "windows": [
        "SYSTEM_SERVICE_EXCEPTION",
        "MEMORY_MANAGEMENT",
        "IRQL_NOT_LESS_OR_EQUAL",
        "CRITICAL_PROCESS_DIED",
        "KERNEL_SECURITY_CHECK_FAILURE",
        "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED",
        "UNEXPECTED_KERNEL_MODE_TRAP",
        "DPC_WATCHDOG_VIOLATION",
        "PAGE_FAULT_IN_NONPAGED_AREA",
        "DRIVER_CORRUPTED_EXPOOL"
    ],
    "macos": [
        "Kernel Panic: CPU stuck at PC=0xffffff8012345678",
        "panic(cpu 0 caller 0xffffff801234): \"Unable to find driver for this platform\"",
        "\"IO80211Family::monitorModeOff(): Mode error (-1)\"",
        "\"Sandbox: crashed(501) deny mach-lookup com.apple.coresymbolicationd\"",
        "\"BUG in process handling: p_pid 1214, p_argc 0, p_argv 0, p_envp 0\"",
        "\"AppleIntelCPUPowerManagement: (cpu_idle) failed\"",
        "\"CPU stuck at PC=0xffffff8012345678\"",
        "\"Invalid frame pointer: 0x109304ad0\"",
        "\"AppleKeyStore: operation failed (pid: 1214, op: 0)\"",
        "\"NVRAM file error\"",
    ]
}

# Коды хекс-дампа для имитации сбоя
HEX_DUMP_DATA = [
    "0x00000000: 7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00",
    "0x00000010: 02 00 3e 00 01 00 00 00 c0 e4 00 00 00 00 00 00",
    "0x00000020: 40 00 00 00 00 00 00 00 08 1a 02 00 00 00 00 00",
    "0x00000030: 00 00 00 00 40 00 38 00 0d 00 40 00 1e 00 1d 00",
    "0x00000040: 06 00 00 00 05 00 00 00 40 00 00 00 00 00 00 00",
    "0x00000050: 40 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00",
    "0x00000060: d8 02 00 00 00 00 00 00 d8 02 00 00 00 00 00 00",
    "0x00000070: 08 00 00 00 00 00 00 00 03 00 00 00 04 00 00 00",
    "0x00000080: 18 03 00 00 00 00 00 00 18 03 00 00 00 00 00 00",
    "0x00000090: 18 03 00 00 00 00 00 00 1c 00 00 00 00 00 00 00",
]

# Руткит компоненты для имитации
ROOTKIT_COMPONENTS = [
    ("kernel32.dll", "Перехват системных вызовов"),
    ("ntdll.dll", "Подмена таблицы системных вызовов"),
    ("drivers/system.sys", "Загрузка драйвера режима ядра"),
    ("registry.dat", "Модификация системного реестра"),
    ("svchost.exe", "Внедрение в системные процессы"),
    ("bootmgr", "Модификация загрузчика"),
    ("security.dll", "Обход системы безопасности"),
    ("network.sys", "Перехват сетевого трафика"),
    ("explorer.exe", "Скрытие файлов и процессов"),
    ("lsass.exe", "Кража учетных данных"),
    ("winlogon.exe", "Перехват ввода пользователя"),
    ("bootkit.bin", "Установка буткита")
]

# ASCII карта мира (упрощенная)
WORLD_MAP = [
    "                                                                                ",
    "            .--.                                                 .              ",
    "           /    \\        .   .                               .  |\\            ",
    "           |    |            _____                               /\\            ",
    "        ___|    |____       |     |                            .'  `.           ",
    "  .--.-'            /\\      |     | .-----------._____________/      \\        ",
    "  \\   '. NA       /  \\_____|     |/                             ASIA \\       ",
    "  |    \\_________/     .-'       |                                    |        ",
    "   \\             \\    /          |___                                /        ",
    "    '.            \\   |  EU       /|  '-.______________________________/|      ",
    "      \\            \\  |          / |                  |        \\      |      ",
    "       '.___________\\_|__       |  |                  |        |      |        ",
    "                        /       '. |         AFRICA   ||       |      |         ",
    "     SA               .'   _.-.\\_/                    ||      .|      |         ",
    "    /\\______________/    /    /                      ||\\     ||     /         ",
    "   /                \\    '.___\\______________________//      /|    .'         ",
    "  |                  \\      \\_______________________.'\"     / |  .'           ",
    "  |                   \\                               \\ '--.|  |/              ",
    "  |                    \\                              |     |  /               ",
    "  '.                    \\                             |  AU |.'                ",
    "    '-.                  \\                           /|     /                  ",
    "       '--._______________|\\________________________/ |____/                   ",
    "                                                                                ",
]

# Координаты ключевых регионов на карте (x, y)
MAP_REGIONS = {
    "NA": (10, 7),      # Северная Америка
    "SA": (14, 15),     # Южная Америка
    "EU": (34, 9),      # Европа
    "RU": (45, 7),      # Россия
    "AF": (40, 14),     # Африка
    "AS": (60, 10),     # Азия
    "AU": (70, 20),     # Австралия
}

# Данные о фейковых атаках и их источниках для визуализации
ATTACK_SOURCES = ["NA", "SA", "EU", "RU", "AF", "AS", "AU"]
ATTACK_TYPES = [
    ("DDoS", COLORS['RED']),
    ("Bruteforce", COLORS['ORANGE']),
    ("Ransomware", COLORS['MAGENTA']),
    ("Phishing", COLORS['YELLOW']),
    ("SQL Injection", COLORS['CYAN']),
    ("XSS", COLORS['GREEN']),
    ("Zero-day", COLORS['DEDSEC']),
]

# Данные для трассировки маршрута
TRACE_NODES = [
    {"hop": 1, "ip": "192.168.1.1", "name": "Local Gateway", "ms": 1},
    {"hop": 2, "ip": "10.0.0.1", "name": "ISP Router", "ms": 5},
    {"hop": 3, "ip": "172.16.0.1", "name": "Regional Node", "ms": 10},
    {"hop": 4, "ip": "4.2.2.2", "name": "Backbone A", "ms": 25},
    {"hop": 5, "ip": "8.8.8.8", "name": "Google DNS", "ms": 30},
    {"hop": 6, "ip": "104.18.7.228", "name": "Cloudflare", "ms": 45},
    {"hop": 7, "ip": "185.199.108.153", "name": "GitHub", "ms": 60},
    {"hop": 8, "ip": "151.101.193.69", "name": "Reddit", "ms": 80},
    {"hop": 9, "ip": "13.107.42.16", "name": "Microsoft", "ms": 100},
    {"hop": 10, "ip": "142.250.186.46", "name": "Google", "ms": 120},
    {"hop": 11, "ip": "157.240.13.35", "name": "Facebook", "ms": 150},
    {"hop": 12, "ip": "108.156.22.12", "name": "Amazon", "ms": 180},
    {"hop": 13, "ip": "104.244.42.65", "name": "Twitter", "ms": 200},
    {"hop": 14, "ip": "18.64.141.13", "name": "Unknown", "ms": 220},
    {"hop": 15, "ip": "91.218.114.31", "name": "Target Server", "ms": 250},
]

# Данные о "темной сети"
DARKNET_SERVICES = [
    {"name": "ShadowMail", "address": "shadow3mailjlshuq.onion", "status": "online", "type": "Email"},
    {"name": "BlackMarket", "address": "blackmrkt24n6edk.onion", "status": "online", "type": "Marketplace"},
    {"name": "HiddenFiles", "address": "files83ndir8swp.onion", "status": "offline", "type": "Storage"},
    {"name": "SecretForum", "address": "forumqer9cjdnq2.onion", "status": "online", "type": "Forum"},
    {"name": "AnonyChat", "address": "chat84kdupmr7vc.onion", "status": "unstable", "type": "Messaging"},
    {"name": "CryptoExchange", "address": "cryptjsu57dhgk2.onion", "status": "online", "type": "Exchange"},
    {"name": "DeepConnect", "address": "deepcvyi45kwxq9.onion", "status": "online", "type": "Social"},
    {"name": "MatrixNode", "address": "nodexhqii58fvb2.onion", "status": "offline", "type": "Node"},
    {"name": "DarkSearch", "address": "search7tdrcvri6.onion", "status": "online", "type": "Search"},
    {"name": "SecureDrop", "address": "secdropsxw2mw8c.onion", "status": "online", "type": "Whistleblowing"},
]

# Иконки DedSec
ICONS = {
    'skull': '☠',
    'target': '◎',
    'eye': '◉',
    'lock': '🔒',
    'unlock': '🔓',
    'warning': '⚠',
    'download': '▼',
    'upload': '▲',
    'power': '⏻',
    'check': '✓',
    'cross': '✗',
    'plug': '⚡',
    'binary': '⚉',
    'hack': '⚔',
    'shield': '⛨',
    'network': '⬢',
    'key': '⚿',
    'load': '◌',
    'wifi': '⚶',
    'clock': '◕',
    'data': '◨',
    'firewall': '▅',
    'system': '⚙',
    'access': '⚶',
    'search': '🔍',
    'chart': '📊',
    'stats': '📈',
    'pulse': '📶',
    'folder': '📁',
    'file': '📄',
    'trash': '🗑️',
    'drive': '💾',
    'globe': '🌐',
    'timer': '⏱️',
    'radar': '📡',
    'satellite': '🛰️',
    'magnet': '🧲',
    'server': '🖥️',
    'chain': '⛓️',
    'settings': '⚙️',
}

# Мемы и URL-ы (добавьте свои)
URLS = [
    "https://memchik.ru/images/memes/5a6b8701b1c7e346775d58da.jpg",
    "https://avatars.mds.yandex.net/i?id=db5e0dee6fdd7320d1333e2a5a3a268c_sr-8750570-images-thumbs&n=13",  # DedSec стиль
    "https://cs12.pikabu.ru/post_img/2022/11/13/10/og_og_1668355736263781700.jpg"   # Хакерский мем
]

# Фейковые пароли для "взлома"
FAKE_PASSWORDS = [
    "P@$$w0rd123", "Admin1234!", "root_access_000", "system.override.42", 
    "firewall.disable", "kernel.access.773", "EVG_master_key", "DedSec_override"
]

# Фейковые IP-адреса для "взлома"
FAKE_IPS = [
    "192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8", "1.1.1.1",
    "104.18.7.228", "151.101.65.140"
]

# Фейковые названия файлов и директорий
FAKE_FILES = [
    "system32", "kernel_access.sys", "ntoskrnl.exe", "bash_history", "sudoers",
    "shadow", "SAM", "passwd", "id_rsa", "master.passwd", "boot.ini"
]

# ========== КОНЕЦ КОНФИГУРАЦИИ ==========

# ========== ОПРЕДЕЛЕНИЕ СИСТЕМЫ И УТИЛИТЫ ==========
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

def get_terminal_size():
    """Получить размер терминала"""
    try:
        columns, lines = os.get_terminal_size()
        return columns, lines
    except:
        return 80, 24

def clear_screen():
    """Очистить экран кросс-платформенно"""
    os.system('cls' if IS_WINDOWS else 'clear')

def get_system_info():
    """Получить системную информацию"""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "username": os.getlogin(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return info

# Глобальная переменная для управления звуком
SOUND_ENABLED = True

def play_sound(sound_type="notify"):
    """Воспроизведение звука кросс-платформенно"""
    if not SOUND_ENABLED:
        return
        
    try:
        if IS_MACOS:
            sounds = {
                "notify": "/System/Library/Sounds/Sosumi.aiff",
                "error": "/System/Library/Sounds/Basso.aiff",
                "success": "/System/Library/Sounds/Glass.aiff",
                "warning": "/System/Library/Sounds/Funk.aiff"
            }
            os.system(f"afplay {sounds.get(sound_type, sounds['notify'])} &")
        elif IS_WINDOWS:
            import winsound
            sounds = {
                "notify": winsound.MB_ICONASTERISK,
                "error": winsound.MB_ICONHAND,
                "success": winsound.MB_ICONEXCLAMATION,
                "warning": winsound.MB_ICONQUESTION
            }
            winsound.MessageBeep(sounds.get(sound_type, winsound.MB_ICONASTERISK))
    except:
        # Если воспроизведение звука не удалось, просто игнорируем
        pass

# ========== ВИЗУАЛЬНЫЕ ЭФФЕКТЫ ==========

def setup_terminal():
    """Настройка терминала для максимального эффекта"""
    if IS_MACOS:
        try:
            # macOS-специфичная настройка
            os.system("""osascript -e 'tell app "Terminal"
                activate
                set bounds of front window to {50, 50, 1200, 800}
                set background color of window 1 to {0, 0, 0}
                set normal text color of window 1 to {0, 255, 0}
                set transparency of window 1 to 0.0
            end tell'""")
        except:
            pass
    elif IS_WINDOWS:
        try:
            # Windows-специфичная настройка
            os.system("mode con: cols=120 lines=40")
            os.system("color 0A")  # Черный фон, зеленый текст для cmd
            # Для PowerShell нужны другие команды, но это базовая настройка
        except:
            pass
    
    clear_screen()

def center_text(text, width=None):
    """Центрировать текст относительно ширины терминала"""
    if width is None:
        width, _ = get_terminal_size()
    lines = text.split('\n')
    centered = []
    for line in lines:
        centered.append(line.center(width))
    return '\n'.join(centered)

def print_banner(text, style='header'):
    """Вывести баннер с текстом"""
    width, _ = get_terminal_size()
    border = "═" * width
    print(f"{STYLES[style]}{border}")
    print(center_text(text, width))
    print(f"{border}{COLORS['RESET']}")

def typing_effect(text, speed=0.03, color=None):
    """Эффект печатающегося текста"""
    color_code = color if color else ""
    reset = COLORS['RESET'] if color else ""
    
    for char in text:
        sys.stdout.write(f"{color_code}{char}{reset}")
        sys.stdout.flush()
        time.sleep(speed)
    print()

def loading_bar(duration=5, text="Loading", color=COLORS['DEDSEC'], width=20):
    """Анимированная полоса загрузки в стиле DedSec"""
    steps = 50
    delay = duration / steps
    
    for i in range(steps + 1):
        percent = i * 100 // steps
        filled_width = i * width // steps
        bar = "█" * filled_width + "▒" * (width - filled_width)
        sys.stdout.write(f"\r{color}{text}: [{bar}] {percent}%{COLORS['RESET']}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def matrix_rain(duration=3, density=0.05):
    """Улучшенный эффект матричного дождя"""
    width, height = get_terminal_size()
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/\\"
    columns = [0] * width
    
    end_time = time.time() + duration
    
    try:
        while time.time() < end_time:
            clear_screen()
            output = [' ' for _ in range(width * height)]
            
            # Обновляем каждую колонку
            for i in range(width):
                if columns[i] > 0 and random.random() < 0.95:
                    # Символы в колонке
                    for j in range(columns[i]):
                        row = height - j - 1
                        if 0 <= row < height:
                            char = random.choice(chars)
                            color = COLORS['HACKER'] if j == 0 else COLORS['GREEN']
                            idx = row * width + i
                            if 0 <= idx < len(output):
                                output[idx] = f"{color}{char}{COLORS['RESET']}"
                    # Увеличиваем длину колонки
                    columns[i] += 1 if random.random() < 0.1 else 0
                    # Ограничиваем длину
                    columns[i] = min(columns[i], height * 2)
                elif random.random() < density:
                    # Начинаем новую колонку
                    columns[i] = 1
                else:
                    # Уменьшаем существующую колонку
                    columns[i] = max(0, columns[i] - 1)
            
            # Вывод
            for i in range(height):
                line = ''.join(output[i * width:(i + 1) * width])
                print(line)
            
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

def cyber_glitch(text, intensity=5):
    """Улучшенный эффект цифрового глитча"""
    width, _ = get_terminal_size()
    centered_text = center_text(text, width)
    
    glitch_chars = '01█▓▒░║╬⍾⌬⎋⌇⌗⌘⏣⏢⏚⏥⎈⍜⍩⍚⍦⍧⍫⍱⍲⍼☢☣⚠'
    colors = [COLORS['GLITCH'], COLORS['DEDSEC'], COLORS['RED'], COLORS['MATRIX']]
    
    for _ in range(intensity):
        clear_screen()
        lines = centered_text.split('\n')
        
        for line in lines:
            # Выбираем случайный цвет
            color = random.choice(colors)
            # Создаем глитч-версию строки
            glitched = ''.join([
                random.choice(glitch_chars) if random.random() > 0.7 else c 
                for c in line
            ])
            print(f"{color}{glitched}{COLORS['RESET']}")
        
        # Добавляем случайные артефакты
        for _ in range(random.randint(1, 5)):
            artifact = ''.join(random.choice(glitch_chars) for _ in range(random.randint(5, 20)))
            position = random.randint(0, width - len(artifact))
            spaces = ' ' * position
            print(f"{spaces}{random.choice(colors)}{artifact}{COLORS['RESET']}")
        
        time.sleep(0.07)

def show_system_scan(found_items=False):
    """Имитация сканирования системы"""
    system_info = get_system_info()
    areas = [
        ("Операционная система", f"{system_info['system']} {system_info['release']}"),
        ("Процессор", system_info['processor']),
        ("Имя хоста", system_info['hostname']),
        ("IP-адрес", system_info['ip']),
        ("Учетная запись", system_info['username']),
        ("Брандмауэр", "Активен"),
        ("Антивирус", "Активен" if random.random() > 0.5 else "Неактивен"),
        ("Сетевые порты", f"Открыто {random.randint(1,10)} из {random.randint(10,100)}")
    ]
    
    print(f"{STYLES['header']}[{ICONS['target']}] СКАНИРОВАНИЕ СИСТЕМЫ{COLORS['RESET']}")
    
    for area, value in areas:
        sys.stdout.write(f"\r{COLORS['CYAN']}[{ICONS['load']}] Сканирование: {area}...")
        sys.stdout.flush()
        time.sleep(random.uniform(0.5, 1.5))
        sys.stdout.write(f"\r{COLORS['DEDSEC_GREEN']}[{ICONS['check']}] {area}: {COLORS['WHITE']}{value}\n")
        sys.stdout.flush()
    
    if found_items:
        print(f"\n{STYLES['warning']}[{ICONS['warning']}] ОБНАРУЖЕНЫ УЯЗВИМОСТИ:{COLORS['RESET']}")
        vulnerabilities = [
            ("CVE-2023-1234", "Уязвимость в управлении памятью", "Критическая"),
            ("MS-20-012", "Удаленное выполнение кода", "Высокая"),
            ("DEDSEC-EVG-001", "Слабые учетные данные администратора", "Средняя"),
        ]
        
        for code, desc, severity in vulnerabilities:
            color = COLORS['RED'] if severity == "Критическая" else COLORS['ORANGE'] if severity == "Высокая" else COLORS['YELLOW']
            print(f"{color}[{ICONS['warning']}] {code}: {desc} ({severity}){COLORS['RESET']}")
            time.sleep(0.3)

def dedsec_hack_effect():
    """Имитация взлома в стиле DedSec"""
    targets = [
        ("Обход аутентификации пользователя", 0.3, ICONS['lock'], ICONS['unlock']),
        ("Взлом брандмауэра системы", 0.4, ICONS['firewall'], ICONS['access']),
        ("Получение привилегий администратора", 0.5, ICONS['key'], ICONS['power']),
        ("Загрузка полезной нагрузки", 0.4, ICONS['download'], ICONS['check']),
        ("Создание скрытого бэкдора", 0.3, ICONS['system'], ICONS['network']),
    ]
    
    print(f"\n{STYLES['header']}[{ICONS['hack']}] ИНИЦИАЛИЗАЦИЯ ПРОТОКОЛА EVG{COLORS['RESET']}\n")
    
    for text, speed, start_icon, end_icon in targets:
        sys.stdout.write(f"\r{COLORS['CYAN']}[{start_icon}] {text}")
        sys.stdout.flush()
        
        # Имитация попыток подбора пароля
        if random.random() > 0.7:
            print()  # Новая строка для пароля
            for _ in range(random.randint(5, 10)):
                fake_pass = random.choice(FAKE_PASSWORDS)
                sys.stdout.write(f"\r    {COLORS['RED']}Попытка: {fake_pass}{COLORS['RESET']}")
                sys.stdout.flush()
                time.sleep(0.1)
            
            # Успешный пароль
            good_pass = random.choice(FAKE_PASSWORDS)
            sys.stdout.write(f"\r    {COLORS['DEDSEC_GREEN']}Успех: {good_pass}{COLORS['RESET']}\n")
            sys.stdout.flush()
        
        # Основной прогресс
        for i in range(10):
            sys.stdout.write(f" {random.choice(['▮', '▯', '▭', '▬'])}")
            sys.stdout.flush()
            time.sleep(speed * random.uniform(0.5, 1.5))
        
        # Завершение
        sys.stdout.write(f"\r{COLORS['DEDSEC_GREEN']}[{end_icon}] {text} {COLORS['DEDSEC']}УСПЕШНО{COLORS['RESET']}")
        print()  # Перевод строки для следующего элемента
        time.sleep(0.2)

def create_platform_artifacts():
    """Создание артефактов взлома на разных платформах"""
    artifacts_created = False
    try:
        if IS_WINDOWS:
            # Путь к документам в Windows
            docs_path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'EVG_Artifacts')
            if not os.path.exists(docs_path):
                os.makedirs(docs_path)
            
            # Создание файлов
            for i in range(5):
                with open(os.path.join(docs_path, f"secret_{i}.evg"), 'w') as f:
                    f.write(f"EVG DEDSEC ARTIFACT {i}\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"System: {platform.system()} {platform.release()}\n")
            
            # Воспроизвести звук
            play_sound("success")
            artifacts_created = True
            
        elif IS_MACOS or IS_LINUX:
            # Путь к документам в macOS/Linux
            docs_path = os.path.expanduser("~/Documents/EVG_Artifacts")
            if not os.path.exists(docs_path):
                os.makedirs(docs_path)
            
            # Создание файлов
            for i in range(5):
                with open(os.path.join(docs_path, f"secret_{i}.evg"), 'w') as f:
                    f.write(f"EVG DEDSEC ARTIFACT {i}\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"System: {platform.system()} {platform.release()}\n")
            
            # Воспроизвести звук
            play_sound("success")
            artifacts_created = True
    except:
        # Если не удалось создать артефакты, просто продолжаем
        pass
    
    return artifacts_created

def show_dedsec_art():
    """Показать случайный арт DedSec с анимацией"""
    clear_screen()
    art = random.choice(EVG_ART)
    print(f"{STYLES['header']}")
    
    # Эффективное отображение арта с разным скоростью для разных строк
    for line in art.split('\n'):
        line_speed = random.uniform(0.005, 0.05)
        typing_effect(line, line_speed, COLORS['DEDSEC'])
    
    # Цитата DedSec
    quote = random.choice(DEDSEC_QUOTES)
    print(f"\n{STYLES['info']}> {quote}{COLORS['RESET']}\n")

def simulate_file_extraction():
    """Симуляция извлечения данных из системы"""
    files_to_extract = random.sample(FAKE_FILES, random.randint(3, 6))
    
    print(f"\n{STYLES['header']}[{ICONS['data']}] ИЗВЛЕЧЕНИЕ СИСТЕМНЫХ ДАННЫХ{COLORS['RESET']}\n")
    
    for file in files_to_extract:
        # Симуляция поиска файла
        sys.stdout.write(f"{COLORS['CYAN']}[{ICONS['search']}] Поиск: {file}")
        sys.stdout.flush()
        time.sleep(random.uniform(0.2, 0.8))
        
        # Симуляция нахождения
        path = f"/{'Windows' if IS_WINDOWS else 'System'}/{random.choice(['system32', 'config', 'users', 'boot'])}/{file}"
        sys.stdout.write(f"\r{COLORS['DEDSEC_GREEN']}[{ICONS['check']}] Найден: {path}")
        print()
        
        # Симуляция копирования
        filesize = random.randint(10, 999)
        sys.stdout.write(f"    {COLORS['DEDSEC']}[{ICONS['download']}] Копирование...")
        sys.stdout.flush()
        
        # Симуляция прогресса
        for i in range(10):
            percent = (i + 1) * 10
            progress = "▓" * (i + 1) + "░" * (9 - i)
            sys.stdout.write(f"\r    {COLORS['DEDSEC']}[{ICONS['download']}] Копирование: [{progress}] {percent}% ({filesize} KB)")
            sys.stdout.flush()
            time.sleep(random.uniform(0.1, 0.3))
        
        sys.stdout.write(f"\r    {COLORS['DEDSEC_GREEN']}[{ICONS['check']}] Скопировано: {path} ({filesize} KB){COLORS['RESET']}")
        print()

def show_network_connections():
    """Показать фейковые сетевые соединения"""
    print(f"\n{STYLES['header']}[{ICONS['network']}] АКТИВНЫЕ СЕТЕВЫЕ СОЕДИНЕНИЯ{COLORS['RESET']}\n")
    
    # Создаем фейковые соединения
    connections = []
    for _ in range(random.randint(5, 10)):
        local_ip = "127.0.0.1" if random.random() > 0.7 else random.choice(FAKE_IPS)
        local_port = random.randint(1024, 65535)
        remote_ip = random.choice(FAKE_IPS)
        remote_port = random.randint(1, 1024) if random.random() > 0.5 else random.choice([21, 22, 25, 80, 443, 445, 3389, 8080, 8443])
        protocol = "TCP" if random.random() > 0.3 else "UDP"
        state = random.choice(["ESTABLISHED", "LISTENING", "TIME_WAIT", "CLOSE_WAIT"])
        program = random.choice(["svchost.exe", "chrome.exe", "explorer.exe", "bash", "python", "systemd", "httpd", "nginx", "ssh"])
        
        connections.append((local_ip, local_port, remote_ip, remote_port, protocol, state, program))
    
    # Показываем заголовок таблицы
    print(f"{COLORS['WHITE']}{'ЛОКАЛ IP:ПОРТ'.ljust(22)} {'УДАЛЕННЫЙ IP:ПОРТ'.ljust(22)} {'ПРОТОКОЛ'.ljust(8)} {'СТАТУС'.ljust(12)} {'ПРОЦЕСС'}{COLORS['RESET']}")
    print(f"{COLORS['WHITE']}{'=' * 80}{COLORS['RESET']}")
    
    # Показываем соединения
    for conn in connections:
        local = f"{conn[0]}:{conn[1]}"
        remote = f"{conn[2]}:{conn[3]}"
        color = COLORS['RED'] if conn[5] == "ESTABLISHED" else COLORS['CYAN']
        print(f"{color}{local.ljust(22)} {remote.ljust(22)} {conn[4].ljust(8)} {conn[5].ljust(12)} {conn[6]}{COLORS['RESET']}")

# ========== ВИЗУАЛИЗАЦИЯ В СТИЛЕ DEDSEC ==========

def ascii_bar_chart(data, title="Статистика", max_height=10, width=50, color=COLORS['DEDSEC']):
    """
    Отрисовка ASCII гистограммы
    """
    if not data:
        return
    
    # Находим максимальное значение для масштабирования
    max_value = max(data)
    
    # Заголовок
    print(f"\n{STYLES['header']}[{ICONS['chart']}] {title.upper()}{COLORS['RESET']}\n")
    
    # Отрисовка гистограммы
    for value in data:
        # Масштабируем значение
        bar_length = int((value / max_value) * width)
        
        # Рисуем полоску
        bar = "█" * bar_length
        percentage = int((value / max_value) * 100)
        
        # Выбираем цвет в зависимости от процента
        if percentage > 80:
            bar_color = COLORS['RED']
        elif percentage > 50:
            bar_color = COLORS['ORANGE']
        else:
            bar_color = color
            
        print(f"{bar_color}{bar}{COLORS['RESET']} {percentage}%")
    
    print() # Пустая строка для разделения

def ascii_line_graph(data, title="Тренд", width=60, height=15, color=COLORS['DEDSEC']):
    """
    Отрисовка ASCII линейного графика
    """
    if not data or len(data) < 2:
        return
    
    # Находим минимальное и максимальное значения
    min_value = min(data)
    max_value = max(data)
    value_range = max_value - min_value or 1  # Избегаем деления на ноль
    
    # Создаем пустую сетку
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Масштабируем данные и размещаем точки на сетке
    for i, value in enumerate(data):
        x = int(i * (width - 1) / (len(data) - 1))
        y = int((max_value - value) * (height - 1) / value_range)
        
        if 0 <= y < height:
            grid[y][x] = '●'
    
    # Соединяем точки линиями
    for i in range(len(data) - 1):
        x1 = int(i * (width - 1) / (len(data) - 1))
        y1 = int((max_value - data[i]) * (height - 1) / value_range)
        
        x2 = int((i + 1) * (width - 1) / (len(data) - 1))
        y2 = int((max_value - data[i + 1]) * (height - 1) / value_range)
        
        # Рисуем линию между точками
        if abs(x2 - x1) > abs(y2 - y1):
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                y = y1 + (y2 - y1) * (x - x1) // (x2 - x1)
                if 0 <= y < height:
                    grid[y][x] = '·'
        else:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                x = x1 + (x2 - x1) * (y - y1) // (y2 - y1) if y2 != y1 else x1
                if 0 <= x < width:
                    grid[y][x] = '·'
    
    # Заголовок
    print(f"\n{STYLES['header']}[{ICONS['stats']}] {title.upper()}{COLORS['RESET']}\n")
    
    # Отрисовка графика
    for row in grid:
        print(f"{color}{''.join(row)}{COLORS['RESET']}")
    
    # Подпись оси Y
    print(f"{COLORS['CYAN']}Min: {min_value} | Max: {max_value}{COLORS['RESET']}")
    print()

def ascii_pie_chart(labels, values, title="Распределение", radius=10, color=COLORS['DEDSEC']):
    """
    Отрисовка ASCII круговой диаграммы
    """
    if not labels or not values or len(labels) != len(values):
        return
    
    total = sum(values)
    
    # Заголовок
    print(f"\n{STYLES['header']}[{ICONS['chart']}] {title.upper()}{COLORS['RESET']}\n")
    
    # Создаем легенду
    for i, (label, value) in enumerate(zip(labels, values)):
        percentage = (value / total) * 100
        bar_length = int(percentage / 5)  # 20 символов = 100%
        
        # Выбираем цвет
        item_color = [COLORS['DEDSEC'], COLORS['RED'], COLORS['GREEN'], 
                     COLORS['ORANGE'], COLORS['CYAN'], COLORS['MAGENTA']][i % 6]
        
        # Отрисовка полоски и процента
        bar = "█" * bar_length
        print(f"{item_color}{bar}{COLORS['RESET']} {label}: {percentage:.1f}%")
    
    print()

def hacker_radar_chart(categories, values, title="Анализ безопасности", color=COLORS['DEDSEC']):
    """
    Отрисовка ASCII радарной диаграммы (паутинка)
    """
    if not categories or not values or len(categories) != len(values):
        return
    
    # Нормализуем значения от 0 до 1
    max_value = max(values)
    normalized = [v / max_value for v in values]
    
    # Количество категорий
    n = len(categories)
    
    # Заголовок
    print(f"\n{STYLES['header']}[{ICONS['radar']}] {title.upper()}{COLORS['RESET']}\n")
    
    # Радиус диаграммы (в символах)
    radius = 10
    
    # Создаем сетку для отрисовки
    grid_size = radius * 2 + 1
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Центр сетки
    center = radius
    
    # Отрисовка категорий и линий
    for i in range(n):
        angle = 2 * math.pi * i / n
        # Координаты конечной точки для этой категории
        end_x = center + int(radius * normalized[i] * 0.9 * math.sin(angle - math.pi/2))
        end_y = center + int(radius * normalized[i] * 0.9 * math.cos(angle - math.pi/2))
        
        # Координаты для названия категории (чуть дальше от края)
        label_x = center + int(radius * 1.1 * math.sin(angle - math.pi/2))
        label_y = center + int(radius * 1.1 * math.cos(angle - math.pi/2))
        
        # Добавляем категорию на сетку
        if 0 <= label_y < grid_size and 0 <= label_x < grid_size:
            # Отмечаем точку на оси
            grid[label_y][label_x] = f"{COLORS['CYAN']}{categories[i][0]}{COLORS['RESET']}"
        
        # Рисуем линию от центра к точке
        draw_line(grid, center, center, end_x, end_y, '·')
        
        # Отмечаем точку значения
        if 0 <= end_y < grid_size and 0 <= end_x < grid_size:
            grid[end_y][end_x] = '●'
    
    # Рисуем соединительные линии между точками значений
    for i in range(n):
        angle1 = 2 * math.pi * i / n
        angle2 = 2 * math.pi * ((i + 1) % n) / n
        
        # Координаты точек
        x1 = center + int(radius * normalized[i] * 0.9 * math.sin(angle1 - math.pi/2))
        y1 = center + int(radius * normalized[i] * 0.9 * math.cos(angle1 - math.pi/2))
        
        x2 = center + int(radius * normalized[(i + 1) % n] * 0.9 * math.sin(angle2 - math.pi/2))
        y2 = center + int(radius * normalized[(i + 1) % n] * 0.9 * math.cos(angle2 - math.pi/2))
        
        # Рисуем соединяющую линию
        draw_line(grid, x1, y1, x2, y2, '·')
    
    # Отрисовка сетки
    for row in grid:
        print(f"{color}{''.join(row)}{COLORS['RESET']}")
    
    print()

def draw_line(grid, x1, y1, x2, y2, char='·'):
    """Вспомогательная функция для отрисовки линии на сетке"""
    if abs(x2 - x1) > abs(y2 - y1):
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            y = y1 + (y2 - y1) * (x - x1) // (x2 - x1)
            if 0 <= y < len(grid):
                grid[y][x] = char
    else:
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            x = x1 + (x2 - x1) * (y - y1) // (y2 - y1) if y2 != y1 else x1
            if 0 <= x < len(grid[0]):
                grid[y][x] = char

def dedsec_stats_dashboard(system_info):
    """
    Отображает информационную панель с системными данными в стиле DedSec
    """
    width, _ = get_terminal_size()
    
    print(f"\n{STYLES['header']}[{ICONS['server']}] DEDSEC ИНФОРМАЦИОННАЯ ПАНЕЛЬ{COLORS['RESET']}\n")
    
    # Верхняя часть - системная информация
    print(f"{COLORS['WHITE']}{'=' * width}{COLORS['RESET']}")
    
    print(f"{COLORS['DEDSEC']}СИСТЕМА: {COLORS['WHITE']}{system_info['system']} {system_info['release']}")
    print(f"{COLORS['DEDSEC']}ХОСТ: {COLORS['WHITE']}{system_info['hostname']} ({system_info['ip']})")
    print(f"{COLORS['DEDSEC']}ПОЛЬЗОВАТЕЛЬ: {COLORS['WHITE']}{system_info['username']}")
    print(f"{COLORS['DEDSEC']}ПРОЦЕССОР: {COLORS['WHITE']}{system_info['processor']}")
    print(f"{COLORS['DEDSEC']}ВРЕМЯ: {COLORS['WHITE']}{system_info['time']}{COLORS['RESET']}")
    
    print(f"{COLORS['WHITE']}{'=' * width}{COLORS['RESET']}")
    
    # Статистика в виде графиков
    # CPU Usage Graph
    ascii_line_graph(
        STATS_DATA['cpu_usage'], 
        "ИСПОЛЬЗОВАНИЕ ПРОЦЕССОРА", 
        width=min(width, 60), 
        color=COLORS['DEDSEC_GREEN']
    )
    
    # Memory Usage
    ascii_bar_chart(
        STATS_DATA['memory_usage'][-5:], 
        "ИСПОЛЬЗОВАНИЕ ПАМЯТИ", 
        width=min(width // 2, 30), 
        color=COLORS['ORANGE']
    )
    
    # Network Activity
    ascii_line_graph(
        STATS_DATA['network_traffic'], 
        "СЕТЕВАЯ АКТИВНОСТЬ", 
        width=min(width, 60), 
        color=COLORS['DEDSEC']
    )
    
    # Vulnerability Analysis
    categories = ["Брандмауэр", "Антивирус", "Пароли", "Шифрование", "Обновления"]
    values = [random.randint(30, 100) for _ in range(len(categories))]
    
    hacker_radar_chart(
        categories, 
        values, 
        "АНАЛИЗ УЯЗВИМОСТЕЙ"
    )
    
    # Bottom summary
    risk_level = sum(values) / (len(values) * 100)
    risk_text = "НИЗКИЙ" if risk_level > 0.7 else "СРЕДНИЙ" if risk_level > 0.4 else "ВЫСОКИЙ"
    risk_color = COLORS['GREEN'] if risk_level > 0.7 else COLORS['ORANGE'] if risk_level > 0.4 else COLORS['RED']
    
    print(f"{COLORS['WHITE']}{'=' * width}{COLORS['RESET']}")
    print(f"{COLORS['DEDSEC']}УРОВЕНЬ РИСКА: {risk_color}{risk_text}{COLORS['RESET']}")
    print(f"{COLORS['DEDSEC']}СТАТУС ПРОТОКОЛА EVG: {COLORS['DEDSEC_GREEN']}АКТИВЕН{COLORS['RESET']}")
    print(f"{COLORS['WHITE']}{'=' * width}{COLORS['RESET']}")
    
    # Случайная цитата
    print(f"\n{STYLES['info']}> {random.choice(DEDSEC_QUOTES)}{COLORS['RESET']}\n")

def show_real_time_intrusion(duration=5):
    """
    Визуализация процесса взлома в реальном времени
    """
    width, height = get_terminal_size()
    
    print(f"\n{STYLES['header']}[{ICONS['pulse']}] АКТИВНОСТЬ ВТОРЖЕНИЯ{COLORS['RESET']}\n")
    
    # Имитация логов вторжения
    intrusion_messages = [
        "Попытка доступа с IP 45.33.22.11 заблокирована",
        "Обнаружен подозрительный сетевой пакет",
        "Сканирование портов с IP 92.118.37.45",
        "Попытка перебора пароля для учетной записи admin",
        "Обнаружен подозрительный JavaScript в HTTP-запросе",
        "Обнаружена попытка SQL-инъекции",
        "Блокировка подозрительного HTTPS-соединения",
        "Попытка получения доступа к защищенному файлу",
        "Обнаружен модифицированный пакет ARP",
        "Неавторизованный доступ к API",
        "Подозрительная активность в системном реестре",
        "Обнаружен уязвимый сервис на порту 5432",
    ]
    
    # Уровни опасности и соответствующие цвета
    threat_levels = [
        ("НИЗКИЙ", COLORS['GREEN']),
        ("СРЕДНИЙ", COLORS['YELLOW']),
        ("ВЫСОКИЙ", COLORS['ORANGE']),
        ("КРИТИЧЕСКИЙ", COLORS['RED']),
    ]
    
    # Симуляция активности в реальном времени
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Случайное сообщение
        message = random.choice(intrusion_messages)
        
        # Случайный уровень опасности
        level, color = random.choice(threat_levels)
        
        # Случайный IP
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        
        # Текущее время
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Вывод сообщения о вторжении
        print(f"[{current_time}] {color}[{level}]{COLORS['RESET']} {message} ({ip})")
        
        # Добавляем случайную задержку для реалистичности
        time.sleep(random.uniform(0.3, 1.0))
    
    print(f"\n{STYLES['success']}[{ICONS['shield']}] Все атаки успешно отражены!{COLORS['RESET']}\n")

# ========== ФУНКЦИИ ВИЗУАЛИЗАЦИИ СИСТЕМНЫХ СБОЕВ ==========

def simulate_bsod():
    """
    Имитирует экран синей смерти (BSOD) для Windows или Kernel Panic для macOS
    """
    clear_screen()
    width, height = get_terminal_size()
    
    if IS_WINDOWS:
        # Windows BSOD (Blue Screen of Death)
        bg_color = COLORS['BLUE']
        error_code = random.choice(BSOD_TEXTS["windows"])
        stop_code = "0x" + "".join(random.choice("0123456789ABCDEF") for _ in range(8))
        
        # BSOD Header
        print(f"{bg_color}")
        for _ in range(height // 3):
            print(" " * width)
        
        # BSOD Content
        print(center_text(f"{COLORS['WHITE']}:(", width))
        print()
        print(center_text(f"Ваш компьютер столкнулся с проблемой и требует перезагрузки.", width))
        print(center_text(f"Мы собираем информацию об ошибке, затем компьютер будет перезагружен.", width))
        print()
        print(center_text(f"Завершено: 20%", width))
        print()
        print(center_text(f"Если вы хотите узнать больше, можете позже искать эту ошибку:", width))
        print(center_text(f"{error_code}", width))
        print(center_text(f"Код остановки: {stop_code}", width))
        
        for _ in range(height // 3):
            print(" " * width)
        print(f"{COLORS['RESET']}")
        
    else:
        # macOS/Linux Kernel Panic
        bg_color = COLORS['BLACK']
        error_text = random.choice(BSOD_TEXTS["macos"])
        
        print(f"{bg_color}")
        for _ in range(height // 4):
            print(" " * width)
        
        # Kernel Panic Header
        print(center_text(f"{COLORS['WHITE']}*** KERNEL PANIC: cpu=0 caller=0xffffff80123456", width))
        print(center_text(f"{COLORS['WHITE']}panic({error_text})", width))
        print()
        
        # Hex dump
        for i in range(min(10, height - 10)):
            print(center_text(f"{COLORS['WHITE']}{random.choice(HEX_DUMP_DATA)}", width))
        
        print()
        print(center_text(f"{COLORS['WHITE']}You need to restart your computer.", width))
        print(center_text(f"{COLORS['WHITE']}Press and hold the power button for several seconds to restart.", width))
        
        for _ in range(height // 4):
            print(" " * width)
        print(f"{COLORS['RESET']}")
    
    # Воспроизводим звук ошибки
    play_sound("error")
    
    # Пауза на чтение
    time.sleep(3)

def simulate_memory_corruption():
    """
    Имитирует повреждение памяти с постепенным искажением экрана
    """
    width, height = get_terminal_size()
    chars = list(" ░▒▓█ABCDEFabcdef0123456789!@#$%^&*()_+-=[]{}\\|;:'\",.<>/?`~")
    corruption_chars = "▓█░▒"
    
    # Создаем базовый текст со случайным содержимым
    lines = []
    for _ in range(height - 5):
        line = "".join(random.choice(chars) for _ in range(width))
        lines.append(line)
    
    # Добавляем "ошибки памяти"
    errors = [
        f"{COLORS['RED']}MEMORY_CORRUPTION_DETECTED{COLORS['RESET']}",
        f"{COLORS['RED']}SEGMENTATION_FAULT{COLORS['RESET']}",
        f"{COLORS['RED']}BUFFER_OVERFLOW{COLORS['RESET']}",
        f"{COLORS['RED']}STACK_SMASHING_DETECTED{COLORS['RESET']}",
        f"{COLORS['RED']}HEAP_CORRUPTION{COLORS['RESET']}",
        f"{COLORS['RED']}NULL_POINTER_DEREFERENCE{COLORS['RESET']}",
        f"{COLORS['RED']}MEMORY_ACCESS_VIOLATION{COLORS['RESET']}",
        f"{COLORS['RED']}ILLEGAL_INSTRUCTION{COLORS['RESET']}",
        f"{COLORS['RED']}FATAL_ERROR{COLORS['RESET']}",
    ]
    
    for e in errors:
        y = random.randint(5, height - 10)
        x = random.randint(5, width - len(e) - 5)
        lines[y] = lines[y][:x] + e + lines[y][x+len(e):]
    
    # Создаем маску коррупции (где будут искажения)
    corruption = [[0 for _ in range(width)] for _ in range(height - 5)]
    
    # Начальные точки коррупции
    for _ in range(5):
        cx = random.randint(0, width - 1)
        cy = random.randint(0, height - 6)
        corruption[cy][cx] = 1
    
    # Симуляция распространения коррупции
    for step in range(10):
        clear_screen()
        
        # Распространяем коррупцию
        new_corruption = [row[:] for row in corruption]
        for y in range(height - 5):
            for x in range(width):
                if corruption[y][x] == 1:
                    # Распространяем на соседние клетки с некоторой вероятностью
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height - 5 and random.random() < 0.3:
                            new_corruption[ny][nx] = 1
        
        corruption = new_corruption
        
        # Отображаем текст с коррупцией
        title = f"{COLORS['RED']}CRITICAL SYSTEM ERROR - MEMORY CORRUPTION DETECTED{COLORS['RESET']}"
        print(center_text(title, width))
        
        for y in range(height - 5):
            line = list(lines[y])
            for x in range(width):
                if corruption[y][x] == 1:
                    line[x] = f"{random.choice([COLORS['RED'], COLORS['GLITCH']])}{random.choice(corruption_chars)}{COLORS['RESET']}"
            
            print("".join(line))
        
        # Дополнительные сообщения внизу
        bottom_msg = f"{COLORS['RED']}SYSTEM HALTED - FATAL ERROR - DATA LOSS IMMINENT{COLORS['RESET']}"
        print("")
        print(center_text(bottom_msg, width))
        
        # Звук ошибки
        if step % 3 == 0:
            play_sound("error")
            
        time.sleep(0.5)

# ========== ФУНКЦИИ ВИЗУАЛИЗАЦИИ КАРТЫ МИРА И АТАК ==========

def display_world_map(active_attacks=None):
    """
    Отображает ASCII карту мира с активными атаками
    
    :param active_attacks: Список кортежей (источник, цель, тип_атаки, цвет)
    """
    width, height = get_terminal_size()
    
    # Заголовок
    print(f"\n{STYLES['header']}[{ICONS['globe']}] ГЛОБАЛЬНАЯ КАРТА КИБЕРАТАК{COLORS['RESET']}\n")
    
    # Создаем копию карты для модификации
    map_copy = WORLD_MAP.copy()
    
    # Добавляем атаки на карту если они есть
    if active_attacks:
        for source, target, attack_type, color in active_attacks:
            # Координаты источника и цели
            sx, sy = MAP_REGIONS[source]
            tx, ty = MAP_REGIONS[target]
            
            # Рисуем линию атаки
            # Для упрощения просто заменяем символы на пути
            dx = tx - sx
            dy = ty - sy
            steps = max(abs(dx), abs(dy)) + 1
            
            for i in range(steps):
                # Вычисляем точку на линии
                if steps > 1:
                    t = i / (steps - 1)
                else:
                    t = 0
                x = int(sx + dx * t)
                y = int(sy + dy * t)
                
                # Заменяем символ, если он находится в пределах карты
                if 0 <= y < len(map_copy) and 0 <= x < len(map_copy[y]):
                    # Разные символы для разных участков линии
                    if i == 0:  # Источник
                        char = '*'
                    elif i == steps - 1:  # Цель
                        char = 'X'
                    else:  # Путь
                        char = ['·', '·', '·', '·', '·', '~', '*'][i % 7]
                    
                    # Обновляем строку карты
                    row = map_copy[y]
                    map_copy[y] = row[:x] + f"{color}{char}{COLORS['RESET']}" + row[x+1:]
    
    # Выводим карту
    for line in map_copy:
        print(f"{COLORS['CYAN']}{line}{COLORS['RESET']}")
    
    # Легенда
    print(f"\n{COLORS['WHITE']}Легенда:{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}* {COLORS['RESET']}- источник атаки, {COLORS['CYAN']}X {COLORS['RESET']}- цель")
    
    if active_attacks:
        print(f"\n{COLORS['WHITE']}Активные атаки:{COLORS['RESET']}")
        for source, target, attack_type, color in active_attacks:
            print(f"{color}[{attack_type}]{COLORS['RESET']} {source} → {target}")
    
    print()

def display_enhanced_world_map(active_attacks=None):
    """
    Отображает улучшенную ASCII карту мира с активными атаками и цветовым выделением регионов
    
    :param active_attacks: Список кортежей (источник, цель, тип_атаки, цвет)
    """
    width, height = get_terminal_size()
    
    # Заголовок
    print(f"\n{STYLES['header']}[{ICONS['globe']}] ГЛОБАЛЬНАЯ КАРТА КИБЕРАТАК{COLORS['RESET']}\n")
    
    # Создаем копию карты для модификации
    map_copy = WORLD_MAP.copy()
    
    # Цветовые обозначения для регионов (перед атаками)
    region_colors = {
        "NA": COLORS['CYAN'],
        "SA": COLORS['DEDSEC_GREEN'],
        "EU": COLORS['BLUE'],
        "RU": COLORS['CYBER'],
        "AF": COLORS['ORANGE'],
        "AS": COLORS['MAGENTA'],
        "AU": COLORS['RED'],
    }
    
    # Добавляем цветовые обозначения регионов
    for region, (x, y) in MAP_REGIONS.items():
        if 0 <= y < len(map_copy) and 0 <= x < len(map_copy[y]):
            # Получаем строку
            row = map_copy[y]
            
            # Создаем цветовое обозначение для названия региона
            colored_region = f"{region_colors[region]}{region}{COLORS['RESET']}"
            
            # Определяем длину строки перед цветовым кодом (для правильной вставки)
            pre_color_length = len(region)
            
            # Заменяем обозначение региона на цветное
            new_row = ""
            region_found = False
            
            i = 0
            while i < len(row):
                if not region_found and i <= x and i + pre_color_length <= len(row) and row[i:i+pre_color_length] == region:
                    new_row += colored_region
                    i += pre_color_length
                    region_found = True
                else:
                    new_row += row[i]
                    i += 1
            
            map_copy[y] = new_row
    
    # Добавляем атаки на карту если они есть
    if active_attacks:
        for source, target, attack_type, color in active_attacks:
            # Координаты источника и цели
            sx, sy = MAP_REGIONS[source]
            tx, ty = MAP_REGIONS[target]
            
            # Рисуем линию атаки
            # Для упрощения просто заменяем символы на пути
            dx = tx - sx
            dy = ty - sy
            steps = max(abs(dx), abs(dy)) + 1
            
            # Символы для отображения пути атаки
            attack_symbols = ['·', '•', '◦', '◘', '◙', '*', '◦', '•', '·']
            
            for i in range(steps):
                # Вычисляем точку на линии
                if steps > 1:
                    t = i / (steps - 1)
                else:
                    t = 0
                x = int(sx + dx * t)
                y = int(sy + dy * t)
                
                # Заменяем символ, если он находится в пределах карты
                if 0 <= y < len(map_copy) and 0 <= x < len(map_copy[y]):
                    # Разные символы для разных участков линии
                    char_idx = int(i * len(attack_symbols) / steps)
                    char = attack_symbols[char_idx]
                    
                    if i == 0:  # Источник
                        char = '◉'
                    elif i == steps - 1:  # Цель
                        char = '⊗'
                    
                    # Обновляем строку карты
                    row = map_copy[y]
                    
                    # Проверяем длину строки
                    if x < len(row):
                        map_copy[y] = row[:x] + f"{color}{char}{COLORS['RESET']}" + row[x+1:]
    
    # Добавляем декоративные элементы
    border_width = min(width, 80)
    border = f"{COLORS['DEDSEC']}╔{'═' * (border_width - 2)}╗{COLORS['RESET']}"
    bottom_border = f"{COLORS['DEDSEC']}╚{'═' * (border_width - 2)}╝{COLORS['RESET']}"
    
    print(border)
    
    # Выводим карту с боковыми границами
    for line in map_copy:
        # Обрезаем строку, если она слишком длинная
        disp_line = line[:border_width - 2]
        # Дополняем пробелами, если слишком короткая
        disp_line = disp_line.ljust(border_width - 2)
        print(f"{COLORS['DEDSEC']}║{COLORS['RESET']}{disp_line}{COLORS['DEDSEC']}║{COLORS['RESET']}")
    
    print(bottom_border)
    
    # Легенда
    print(f"\n{COLORS['WHITE']}Легенда:{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}◉ {COLORS['RESET']}- источник атаки, {COLORS['CYAN']}⊗ {COLORS['RESET']}- цель")
    
    # Регионы
    print(f"\n{COLORS['WHITE']}Регионы:{COLORS['RESET']}", end=" ")
    for region, color in region_colors.items():
        print(f"{color}{region}{COLORS['RESET']}", end=" ")
    print()
    
    if active_attacks:
        print(f"\n{COLORS['WHITE']}Активные атаки:{COLORS['RESET']}")
        for source, target, attack_type, color in active_attacks:
            print(f"{color}[{attack_type}]{COLORS['RESET']} {source} → {target}")
    
    print()

def simulate_global_attacks(duration=15, use_enhanced_map=True):
    """
    Симулирует глобальные кибератаки на карте мира в реальном времени
    
    :param duration: Длительность симуляции в секундах
    :param use_enhanced_map: Использовать улучшенную версию карты мира
    """
    start_time = time.time()
    attack_count = 0
    
    # Список активных атак: (источник, цель, тип, цвет)
    active_attacks = []
    
    while time.time() - start_time < duration:
        clear_screen()
        
        # Создаем новые атаки случайным образом
        if random.random() < 0.3 and len(active_attacks) < 5:  # Не более 5 атак одновременно
            source = random.choice(ATTACK_SOURCES)
            target = random.choice([t for t in ATTACK_SOURCES if t != source])  # Не атакуем сами себя
            attack_type, color = random.choice(ATTACK_TYPES)
            active_attacks.append((source, target, attack_type, color))
            attack_count += 1
            
            # Воспроизводим звук новой атаки
            play_sound("warning")
        
        # Удаляем случайные старые атаки
        if active_attacks and random.random() < 0.2:
            active_attacks.pop(0)
            
        # Отображаем карту с атаками
        if use_enhanced_map:
            display_enhanced_world_map(active_attacks)
        else:
            display_world_map(active_attacks)
        
        # Отображаем информацию о длительности и количестве атак
        elapsed = time.time() - start_time
        remaining = duration - elapsed
        
        print(f"{COLORS['DEDSEC']}[{ICONS['timer']}] Время наблюдения: {int(elapsed)}/{duration}s | ", end="")
        print(f"Обнаружено атак: {attack_count} | ", end="")
        print(f"Активных атак: {len(active_attacks)}{COLORS['RESET']}")
        
        time.sleep(1)  # Обновляем каждую секунду

def display_traceroute(target="91.218.114.31", animate=True):
    """
    Отображает визуализацию трассировки маршрута к целевому серверу
    
    :param target: IP-адрес цели
    :param animate: Анимировать трассировку
    """
    print(f"\n{STYLES['header']}[{ICONS['network']}] ТРАССИРОВКА МАРШРУТА К {target}{COLORS['RESET']}\n")
    
    print(f"{COLORS['WHITE']}Hop  {'IP-адрес'.ljust(18)} {'Имя'.ljust(20)} {'Задержка'.ljust(10)} {'Статус'}{COLORS['RESET']}")
    print(f"{COLORS['WHITE']}{'=' * 70}{COLORS['RESET']}")
    
    # Максимальная задержка для масштабирования графика
    max_ms = max(node["ms"] for node in TRACE_NODES)
    
    for i, node in enumerate(TRACE_NODES):
        if animate:
            time.sleep(random.uniform(0.2, 0.5))  # Задержка для имитации реальной трассировки
            
            # Имитация поиска узла
            for _ in range(3):
                sys.stdout.write(f"\r{i+1:<4} {'Поиск...'.ljust(18)} {''.ljust(20)} {''.ljust(10)} {COLORS['CYAN']}●{COLORS['RESET']}")
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write(f"\r{i+1:<4} {'Поиск...'.ljust(18)} {''.ljust(20)} {''.ljust(10)} {COLORS['CYAN']}○{COLORS['RESET']}")
                sys.stdout.flush()
                time.sleep(0.1)
        
        # Генерируем график задержки
        ms_percent = node["ms"] / max_ms
        graph_len = int(ms_percent * 20)
        graph = "█" * graph_len + "░" * (20 - graph_len)
        
        # Выбираем цвет в зависимости от задержки
        if node["ms"] < 30:
            color = COLORS['GREEN']
        elif node["ms"] < 100:
            color = COLORS['YELLOW']
        else:
            color = COLORS['RED']
            
        # Отображаем информацию об узле
        status = f"{COLORS['DEDSEC_GREEN']}Доступен{COLORS['RESET']}"
        if i > len(TRACE_NODES) - 3:
            if random.random() < 0.3:
                status = f"{COLORS['RED']}Потеря пакетов{COLORS['RESET']}"
                
        line = f"{i+1:<4} {node['ip'].ljust(18)} {node['name'].ljust(20)} {color}{node['ms']}ms {graph}{COLORS['RESET']} {status}"
        sys.stdout.write(f"\r{line}\n")
        sys.stdout.flush()
        
        # Звуковой эффект
        if animate and i % 3 == 0:
            generate_pc_beep(frequency=1000 + i * 100, duration=0.05)
    
    print(f"\n{COLORS['DEDSEC_GREEN']}[{ICONS['check']}] Трассировка завершена! Путь к цели найден через {len(TRACE_NODES)} узлов.{COLORS['RESET']}\n")
    
    # Отображаем статистику
    avg_ms = sum(node["ms"] for node in TRACE_NODES) / len(TRACE_NODES)
    print(f"{COLORS['CYAN']}Средняя задержка: {avg_ms:.1f}ms{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}Максимальная задержка: {max_ms}ms{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}Общее расстояние: {len(TRACE_NODES)} hops{COLORS['RESET']}")
    print()

# ========== ФУНКЦИИ ГЕНЕРАЦИИ ЗВУКОВ ==========

def generate_pc_beep(frequency=1000, duration=0.1):
    """
    Генерирует звуковой сигнал через PC Speaker без использования внешних библиотек
    
    :param frequency: Частота звука в герцах
    :param duration: Длительность звука в секундах
    """
    try:
        if IS_WINDOWS:
            # В Windows используем интерфейс winsound
            try:
                import winsound
                winsound.Beep(frequency, int(duration * 1000))
            except:
                pass
        elif IS_MACOS:
            # В macOS используем afplay с генерацией тона
            try:
                # Создаем временный файл со звуком
                temp_file = "/tmp/evg_beep.wav"
                os.system(f"say -o {temp_file} --data-format=LEI16@{frequency} '[[volm 0.5]] [[slnc {duration}]]'")
                os.system(f"afplay {temp_file} &")
                # Удаляем временный файл через некоторое время
                threading.Timer(duration + 0.5, lambda: os.system(f"rm {temp_file}")).start()
            except:
                pass
        elif IS_LINUX:
            # В Linux используем системный beep или echo
            try:
                if os.path.exists("/usr/bin/beep"):
                    os.system(f"beep -f {frequency} -l {int(duration * 1000)}")
                else:
                    # Альтернативный метод для Linux без beep
                    sys.stdout.write('\a')  # Системный bell
                    sys.stdout.flush()
            except:
                pass
    except:
        # Игнорируем любые ошибки при генерации звука
        pass

def play_hacker_melody():
    """
    Воспроизводит "хакерскую" мелодию через PC Speaker
    """
    # Набор частот для "хакерской" мелодии
    frequencies = [
        800, 900, 1000, 1100, 1200, 1300, 1400,
        1500, 1400, 1300, 1200, 1100, 1000, 900,
        800, 850, 900, 950, 1000, 1050, 1100,
        1150, 1200, 1150, 1100, 1050, 1000, 950,
    ]
    
    try:
        for freq in frequencies:
            generate_pc_beep(frequency=freq, duration=0.08)
            time.sleep(0.02)  # Небольшая пауза между звуками
    except:
        # Игнорируем ошибки при воспроизведении
        pass

# ========== ФУНКЦИИ ИМИТАЦИИ РУТКИТОВ И ТЕМНОЙ СЕТИ ==========

def parse_arguments():
    """
    Парсер аргументов командной строки
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="EVG / DEDSEC Взломный скрипт")
    parser.add_argument("-d", "--demo", action="store_true", 
                        help="Запустить в демо-режиме с автоматическим переключением сцен")
    parser.add_argument("-t", "--time", type=int, default=300,
                        help="Длительность демо-режима в секундах (по умолчанию 300)")
    parser.add_argument("-s", "--scene-time", type=int, default=15,
                        help="Длительность каждой сцены в секундах (по умолчанию 15)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Отключить звуковые эффекты")
    
    return parser.parse_args()

def dedsec_demo_loop(total_duration=300, scene_duration=15):
    """
    Запускает демо-режим с автоматическим переключением различных визуальных эффектов
    
    :param total_duration: Общая длительность демо в секундах
    :param scene_duration: Длительность каждой сцены в секундах
    """
    try:
        # Настраиваем терминал
        setup_terminal()
        
        # Получаем информацию о системе
        system_info = get_system_info()
        
        # Список доступных сцен для демонстрации
        scenes = [
            ("DEDSEC_ART", lambda: show_dedsec_art()),
            ("MATRIX_RAIN", lambda: matrix_rain(scene_duration * 0.8)),
            ("SYSTEM_SCAN", lambda: show_system_scan(True)),
            ("DEDSEC_HACK", lambda: dedsec_hack_effect()),
            ("NETWORK_CONNECTIONS", lambda: show_network_connections()),
            ("STATS_DASHBOARD", lambda: dedsec_stats_dashboard(system_info)),
            ("FILE_EXTRACTION", lambda: simulate_file_extraction()),
            ("REALTIME_INTRUSION", lambda: show_real_time_intrusion(scene_duration * 0.8)),
            ("GLOBAL_ATTACKS", lambda: simulate_global_attacks(scene_duration * 0.8, True)),
            ("TRACEROUTE", lambda: display_traceroute(animate=True)),
            ("GLITCH", lambda: cyber_glitch(random.choice(EVG_ART), 5)),
            ("SYSTEM_CRASH", lambda: simulate_memory_corruption()),
        ]
        
        # Показываем начальный баннер
        print_banner("EVG / DEDSEC ДЕМО-РЕЖИМ", "header")
        typing_effect(f"{STYLES['info']}[{ICONS['timer']}] Автоматическая демонстрация всех возможностей за {total_duration} секунд{COLORS['RESET']}", 0.03)
        time.sleep(1)
        
        start_time = time.time()
        
        # Продолжаем показывать сцены, пока не истечет общее время
        while time.time() - start_time < total_duration:
            # Выбираем случайную сцену
            scene_name, scene_func = random.choice(scenes)
            
            # Показываем заголовок сцены
            clear_screen()
            print_banner(f"ДЕМО | СЦЕНА: {scene_name}", "header")
            
            # Оставшееся время демо
            elapsed = time.time() - start_time
            remaining = total_duration - elapsed
            print(f"\n{COLORS['DEDSEC']}[{ICONS['timer']}] Оставшееся время демо: {int(remaining)} секунд{COLORS['RESET']}\n")
            
            # Воспроизводим звук смены сцены
            play_sound("notify")
            
            # Запускаем сцену
            scene_func()
            
            # Короткая пауза между сценами
            time.sleep(2)
        
        # Финальный экран
        clear_screen()
        print_banner("ДЕМО-РЕЖИМ ЗАВЕРШЕН", "success")
        typing_effect(f"{STYLES['success']}[{ICONS['check']}] Демонстрация всех возможностей успешно завершена!{COLORS['RESET']}", 0.03)
        time.sleep(2)
        
    except KeyboardInterrupt:
        # Обработка прерывания
        clear_screen()
        print(f"\n{STYLES['error']}[{ICONS['cross']}] Демо-режим прерван пользователем!{COLORS['RESET']}")
        play_sound("error")
        sys.exit(1)
    except Exception as e:
        # Обработка других ошибок
        print(f"\n{STYLES['error']}[{ICONS['cross']}] Ошибка в демо-режиме: {str(e)}{COLORS['RESET']}")
        play_sound("error")
        sys.exit(1)

def main():
    try:
        # Парсим аргументы командной строки
        args = parse_arguments()
        
        # Глобальная переменная для отключения звука
        global SOUND_ENABLED
        SOUND_ENABLED = not args.quiet
        
        # Демо-режим
        if args.demo:
            dedsec_demo_loop(args.time, args.scene_time)
            return
        
        # Основной режим (стандартный поток)
        # Подготовка терминала
        setup_terminal()
        
        # Приветствие и инициализация
        print_banner("EVG / DEDSEC ПРОТОКОЛ ВЗЛОМА", "header")
        time.sleep(0.5)
        
        typing_effect(f"{STYLES['header']}[{ICONS['system']}] Инициализация системы EVG...{COLORS['RESET']}", 0.05)
        time.sleep(0.5)
        play_sound("notify")
        
        # Фаза 1: Инициализация EVG
        loading_bar(3, f"{ICONS['system']} Загрузка ядра EVG", COLORS['DEDSEC'])
        time.sleep(0.5)
        
        # Фаза 2: Сканирование системы
        system_info = get_system_info()
        typing_effect(f"{STYLES['info']}[{ICONS['target']}] Обнаружена система: {system_info['system']} {system_info['release']}{COLORS['RESET']}", 0.03)
        time.sleep(0.5)
        
        # Фаза 3: Матричная анимация
        typing_effect(f"{STYLES['header']}[{ICONS['binary']}] Запуск цифрового шторма...{COLORS['RESET']}", 0.05)
        matrix_rain(2)
        time.sleep(0.5)
        
        # Фаза 4: Сканирование системы
        typing_effect(f"{STYLES['header']}[{ICONS['target']}] Анализ системных компонентов...{COLORS['RESET']}", 0.05)
        show_system_scan(True)
        time.sleep(1)
        
        # Фаза 5: Глитч-эффект с артом
        cyber_glitch(random.choice(EVG_ART), 3)
        time.sleep(0.5)
        
        # НОВАЯ ФАЗА: Информационная панель
        typing_effect(f"{STYLES['header']}[{ICONS['server']}] Загрузка информационной панели...{COLORS['RESET']}", 0.05)
        dedsec_stats_dashboard(system_info)
        time.sleep(1)
        
        # Фаза 6: Взлом в стиле DedSec
        dedsec_hack_effect()
        time.sleep(0.5)
        
        # НОВАЯ ФАЗА: Мониторинг вторжений
        typing_effect(f"{STYLES['header']}[{ICONS['pulse']}] Обнаружены попытки противодействия...{COLORS['RESET']}", 0.05)
        show_real_time_intrusion(5)
        time.sleep(0.5)
        
        # Фаза 7: Извлечение фейковых данных
        simulate_file_extraction()
        time.sleep(0.5)
        
        # Фаза 8: Показ сетевых соединений
        show_network_connections()
        time.sleep(0.5)
        
        # Фаза 9: Создание артефактов
        typing_effect(f"\n{STYLES['header']}[{ICONS['data']}] Генерация системных артефактов...{COLORS['RESET']}", 0.05)
        artifacts_created = create_platform_artifacts()
        if artifacts_created:
            typing_effect(f"{STYLES['success']}[{ICONS['check']}] Артефакты успешно созданы в Documents/EVG_Artifacts/{COLORS['RESET']}", 0.03)
        else:
            typing_effect(f"{STYLES['warning']}[{ICONS['warning']}] Не удалось создать артефакты. Недостаточно прав.{COLORS['RESET']}", 0.03)
        time.sleep(0.5)
        
        # Фаза 10: Финал
        show_dedsec_art()
        time.sleep(0.5)
        
        # Заключительное сообщение
        print(f"\n{STYLES['success']}[{ICONS['check']}] ВЗЛОМ ЗАВЕРШЕН УСПЕШНО!{COLORS['RESET']}")
        print(f"{STYLES['success']}[{ICONS['check']}] ВАША СИСТЕМА ТЕПЕРЬ ПРИНАДЛЕЖИТ EVG!{COLORS['RESET']}")
        print(f"\n{STYLES['info']}[{ICONS['eye']}] {random.choice(DEDSEC_QUOTES)}{COLORS['RESET']}")
        
        # Воспроизвести звук завершения
        play_sound("success")
        
        # Открытие URL (если не отключено)
        if random.random() > 0.5:  # 50% шанс открытия URL
            for url in random.sample(URLS, min(1, len(URLS))):
                webbrowser.open(url)
                
    except KeyboardInterrupt:
        # Обработка прерывания
        clear_screen()
        print(f"\n{STYLES['error']}[{ICONS['cross']}] Взлом прерван пользователем!{COLORS['RESET']}")
        play_sound("error")
        sys.exit(1)
    except Exception as e:
        # Обработка других ошибок
        print(f"\n{STYLES['error']}[{ICONS['cross']}] Ошибка: {str(e)}{COLORS['RESET']}")
        play_sound("error")
        sys.exit(1)

if __name__ == "__main__":
    main()
