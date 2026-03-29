#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор красивого README.md для VPN репозитория
Создает структурированный документ со всеми ссылками и информацией
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

METADATA_FILE = Path("VPNMIRRORS/metadata.json")
README_FILE = Path("README.md")

# Информация о VPN приложениях
APPS_INFO = {
    "nekobox": {
        "name": "Nekoray / Nekobox",
        "icon": "📦",
        "badge": "![Nekobox](https://img.shields.io/badge/Nekobox-0099FF?style=flat&logo=android&logoColor=white)",
        "platforms": ["Windows", "Android"],
        "download_url": "https://nekobox.one",
        "description": "Продвинутый клиент с поддержкой VLESS, VMess, Reality, White Lists и CIDR",
        "color": "0099FF"
    },
    "v2ray": {
        "name": "V2RayNG / V2RayN",
        "icon": "🚀",
        "badge": "![V2Ray](https://img.shields.io/badge/V2Ray-00A4E4?style=flat&logo=android&logoColor=white)",
        "platforms": ["Android", "Windows", "iOS"],
        "download_url": "https://getv2rayng.com",
        "description": "Популярный клиент для VLESS, VMess, Trojan, Shadowsocks",
        "color": "00A4E4"
    },
    "happ": {
        "name": "Happ VPN",
        "icon": "🔒",
        "badge": "![Happ](https://img.shields.io/badge/Happ%20VPN-FF6B6B?style=flat&logo=android&logoColor=white)",
        "platforms": ["Android", "iOS"],
        "download_url": "https://happ.su",
        "description": "Простой VPN с поддержкой VLESS, Trojan и TOR Bridges",
        "color": "FF6B6B"
    },
    "singbox": {
        "name": "Sing-box",
        "icon": "📱",
        "badge": "![Sing-box](https://img.shields.io/badge/Sing--box-8B5CF6?style=flat&logo=linux&logoColor=white)",
        "platforms": ["Android", "iOS", "Windows", "macOS", "Linux"],
        "download_url": "https://sing-box.sagernet.org",
        "description": "Универсальная платформа проксирования",
        "color": "8B5CF6"
    },
    "clash": {
        "name": "Clash / ClashMeta",
        "icon": "⚔️",
        "badge": "![Clash](https://img.shields.io/badge/Clash-FD7E14?style=flat&logo=windows&logoColor=white)",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "download_url": "https://github.com/MetaCubeX/Clash.Meta",
        "description": "Rule-based tunnel с продвинутой маршрутизацией",
        "color": "FD7E14"
    },
    "tor": {
        "name": "TOR Browser",
        "icon": "🧅",
        "badge": "![TOR](https://img.shields.io/badge/TOR-7D4698?style=flat&logo=tor-browser&logoColor=white)",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "download_url": "https://torproject.org",
        "description": "TOR Bridges и Snowflake для обхода блокировок",
        "color": "7D4698"
    }
}


def get_gitverse_raw_url(category: str, filename: str) -> str:
    """Генерирует прямую ссылку на файл в GitVerse"""
    # Формат для GitVerse: /raw/branch/master/path/to/file
    return f"https://gitverse.ru/RUVIPIEN/russian-white-bolt/raw/branch/master/VPNMIRRORS/{category}/{filename}"


def format_number(num: int) -> str:
    """Форматирует число с разделителями тысяч"""
    return f"{num:,}".replace(",", " ")


def generate_platform_badges(platforms: list) -> str:
    """Генерирует бейджи платформ"""
    badges = []
    platform_icons = {
        "Windows": "💻",
        "Android": "📱",
        "iOS": "🍎",
        "macOS": "🖥️",
        "Linux": "🐧"
    }
    for platform in platforms:
        icon = platform_icons.get(platform, "📱")
        badges.append(f"{icon} {platform}")
    return " ".join(badges)


def generate_config_badges(counts: dict) -> str:
    """Генерирует бейджи с количеством конфигов по протоколам"""
    badges = []
    protocols = [
        ("vless", "VLESS", "blue"),
        ("vmess", "VMess", "green"),
        ("trojan", "Trojan", "red"),
        ("ss", "SS", "orange"),
        ("hysteria", "Hysteria", "purple"),
    ]
    
    for key, name, color in protocols:
        if counts.get(key, 0) > 0:
            badges.append(f"`{name}: {counts[key]}`")
    
    if counts.get("other", 0) > 0:
        badges.append(f"`Other: {counts['other']}`")
    
    return " ".join(badges) if badges else "`Configs: {counts.get('total', 0)}`"


def generate_readme():
    """Основная функция генерации README"""
    
    if not METADATA_FILE.exists():
        print(f"❌ Error: {METADATA_FILE} not found. Run fetch_configs.py first!")
        return False
    
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Группируем конфиги по категориям
    grouped = defaultdict(list)
    for cfg in data["configs"]:
        grouped[cfg["category"]].append(cfg)
    
    # Статистика
    total_configs = data.get("total_configs", 0)
    total_files = len(data["configs"])
    success_sources = data.get("success", 0)
    failed_sources = data.get("failed", 0)
    updated = data.get("updated_msk", data.get("updated_formatted", "Unknown"))
    
    lines = []
    
    # ===== HEADER =====
    lines.append("# 🌐 VPN White-Lists для России")
    lines.append("")
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append("![Auto Update](https://img.shields.io/badge/Auto%20Update-Every%203%20Hours-brightgreen?style=for-the-badge)")
    lines.append(f"![Configs](https://img.shields.io/badge/Configs-{total_configs}-blue?style=for-the-badge)")
    lines.append(f"![Sources](https://img.shields.io/badge/Sources-{success_sources}%2F{success_sources+failed_sources}-orange?style=for-the-badge)")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    
    # ===== INFO BLOCK =====
    lines.append("## 📊 Информация")
    lines.append("")
    lines.append("| Параметр | Значение |")
    lines.append("|----------|----------|")
    lines.append(f"| 🕐 **Последнее обновление** | `{updated}` |")
    lines.append(f"| 📁 **Всего файлов** | `{total_files}` |")
    lines.append(f"| 🔗 **Всего конфигураций** | `{format_number(total_configs)}` |")
    lines.append(f"| ✅ **Рабочих источников** | `{success_sources}` |")
    if failed_sources > 0:
        lines.append(f"| ❌ **Недоступных источников** | `{failed_sources}` |")
    lines.append("")
    
    # ===== VPN APPS SECTION =====
    lines.append("---")
    lines.append("")
    lines.append("## 📱 VPN Приложения")
    lines.append("")
    lines.append("> Выберите приложение для вашей платформы и импортируйте конфигурации из таблиц ниже")
    lines.append("")
    
    # Таблица приложений
    lines.append("| Приложение | Платформы | Описание | Скачать |")
    lines.append("|------------|-----------|----------|---------|")
    
    for cat in ["nekobox", "v2ray", "happ", "singbox", "clash"]:
        if cat in APPS_INFO:
            app = APPS_INFO[cat]
            platforms = generate_platform_badges(app["platforms"])
            lines.append(f"| {app['icon']} **{app['name']}** | {platforms} | {app['description']} | [⬇️ Скачать]({app['download_url']}) |")
    
    lines.append("")
    
    # ===== QUICK START =====
    lines.append("---")
    lines.append("")
    lines.append("## 🚀 Быстрый старт")
    lines.append("")
    lines.append("1. **Выберите приложение** из таблицы выше и установите его")
    lines.append("2. **Найдите нужный конфиг** в разделах ниже")
    lines.append("3. **Нажмите на ссылку \"📋 Копировать\"** или \"⬇️ Скачать\"**")
    lines.append("4. **Импортируйте** ссылку или файл в ваше VPN приложение")
    lines.append("")
    lines.append("> 💡 **Совет:** Конфигурации обновляются автоматически каждые 3 часа!")
    lines.append("")
    
    # ===== CONFIGS BY CATEGORY =====
    lines.append("---")
    lines.append("")
    lines.append("## 📂 Конфигурации по категориям")
    lines.append("")
    
    # Порядок категорий
    category_order = ["nekobox", "v2ray", "happ", "singbox", "clash", "tor"]
    
    for cat in category_order:
        configs = grouped.get(cat, [])
        if not configs:
            continue
        
        app_info = APPS_INFO.get(cat, {
            "name": cat.upper(),
            "icon": "📄",
            "badge": "",
            "description": ""
        })
        
        cat_total = sum(c["counts"]["total"] for c in configs)
        cat_files = len(configs)
        
        # Заголовок категории
        lines.append(f"### {app_info['icon']} {app_info['name']}")
        lines.append("")
        lines.append(f"> {app_info['description']}")
        lines.append("")
        lines.append(f"**Файлов:** `{cat_files}` | **Конфигураций:** `{format_number(cat_total)}`")
        lines.append("")
        
        # Таблица файлов
        lines.append("| № | Название | Конфиги | Размер | Обновлено | Ссылка |")
        lines.append("|---|----------|---------|--------|-----------|--------|")
        
        for idx, cfg in enumerate(configs, 1):
            raw_url = get_gitverse_raw_url(cfg["category"], cfg["filename"])
            counts = cfg["counts"]
            config_badges = generate_config_badges(counts)
            
            lines.append(
                f"| {idx} | **{cfg['name']}**<br>{config_badges} | "
                f"`{format_number(counts['total'])}` | "
                f"`{cfg['size_kb']} KB` | "
                f"`{cfg['updated']}` | "
                f"[⬇️ Скачать]({raw_url}) |"
            )
        
        lines.append("")
    
    # ===== ALL FILES SUMMARY =====
    lines.append("---")
    lines.append("")
    lines.append("## 📋 Все файлы (быстрый доступ)")
    lines.append("")
    lines.append("<details>")
    lines.append("<summary>🔽 Нажмите чтобы развернуть список всех файлов</summary>")
    lines.append("")
    lines.append("```")
    
    for cat in category_order:
        configs = grouped.get(cat, [])
        if not configs:
            continue
        
        app_info = APPS_INFO.get(cat, {"name": cat.upper()})
        lines.append(f"\n📁 {app_info['name']}/")
        
        for cfg in configs:
            raw_url = get_gitverse_raw_url(cfg["category"], cfg["filename"])
            lines.append(f"  ├── {cfg['filename']}")
            lines.append(f"  │   └── {raw_url}")
    
    lines.append("```")
    lines.append("</details>")
    lines.append("")
    
    # ===== ERRORS SECTION =====
    if data.get("errors"):
        lines.append("---")
        lines.append("")
        lines.append(f"## ⚠️ Временно недоступные источники ({len(data['errors'])})")
        lines.append("")
        lines.append("| Источник | Категория | Ошибка |")
        lines.append("|----------|-----------|--------|")
        
        for err in data["errors"][:10]:  # Показываем первые 10 ошибок
            short_err = err["error"][:50] + "..." if len(err["error"]) > 50 else err["error"]
            lines.append(f"| {err['name']} | `{err.get('category', 'N/A')}` | `{short_err}` |")
        
        if len(data["errors"]) > 10:
            lines.append(f"| ... | ... | *и еще {len(data['errors']) - 10} ошибок* |")
        
        lines.append("")
        lines.append("> ⏰ Недоступные источники будут проверены при следующем обновлении (через 3 часа)")
        lines.append("")
    
    # ===== FOOTER =====
    lines.append("---")
    lines.append("")
    lines.append("## 🔄 Автоматическое обновление")
    lines.append("")
    lines.append("Этот репозиторий автоматически обновляется каждые **3 часа** через GitVerse CI/CD.")
    lines.append("")
    lines.append("### 📅 Расписание обновлений:")
    lines.append("- `00:00 MSK` - Ночное обновление")
    lines.append("- `03:00 MSK` - Раннее утро")
    lines.append("- `06:00 MSK` - Утро")
    lines.append("- `09:00 MSK` - Позднее утро")
    lines.append("- `12:00 MSK` - День")
    lines.append("- `15:00 MSK` - После обеда")
    lines.append("- `18:00 MSK` - Вечер")
    lines.append("- `21:00 MSK` - Поздний вечер")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📝 Как добавить источник")
    lines.append("")
    lines.append("1. Отредактируйте файл `sources/urls.txt`")
    lines.append("2. Добавьте строку в формате: `URL|CATEGORY|NAME`")
    lines.append("3. Доступные категории: `nekobox`, `v2ray`, `happ`, `singbox`, `clash`, `tor`")
    lines.append("4. Создайте Pull Request или запушьте изменения")
    lines.append("")
    lines.append("**Пример:**")
    lines.append("```")
    lines.append("https://example.com/config.txt|v2ray|My Config")
    lines.append("```")
    lines.append("")
    
    # ===== STATS & INFO =====
    lines.append("---")
    lines.append("")
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append("**🤖 Автоматизировано с любовью для свободного интернета**")
    lines.append("")
    lines.append(f"*Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S MSK')}*")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    
    # Записываем README
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    
    print(f"✅ README.md generated successfully!")
    print(f"   - Total configs: {total_configs}")
    print(f"   - Total files: {total_files}")
    print(f"   - Categories: {len([c for c in category_order if c in grouped])}")
    
    return True


if __name__ == "__main__":
    generate_readme()
