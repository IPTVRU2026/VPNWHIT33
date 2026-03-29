#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор красивого README с таблицей ссылок
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Базовый URL репозитория (замените на свой, если отличается)
# Формат: https://gitverse.ru/USER/REPO/raw/branch/main/PATH
BASE_RAW_URL = "https://gitverse.ru/RUVIPIEN/russian-white-bolt/raw/branch/master"

def generate_readme():
    meta_path = Path("VPNMIRRORS/metadata.json")
    if not meta_path.exists():
        print("❌ metadata.json not found. Run fetch_configs.py first")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    grouped = defaultdict(list)
    for cfg in data["configs"]:
        grouped[cfg["category"]].append(cfg)

    total_configs = sum(cfg["count"] for cfg in data["configs"])
    updated_time = data["updated"][:16].replace("T", " ") + " UTC"

    lines = []

    # --- ЗАГОЛОВОК ---
    lines.append("# 🇷🇺 VPN White-Lists для России")
    lines.append("")
    lines.append("> ⏱ **Последнее обновление:** `" + updated_time + "`")
    lines.append(">")
    lines.append(f"> ✅ Успешно: **{data['success']}** источников | ❌ Ошибок: **{data['failed']}**")
    lines.append(f"> 🔗 Всего активных конфигураций: **{total_configs:,}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- ИНСТРУКЦИЯ И ПЛАТФОРМЫ ---
    lines.append("## 📱 Как использовать")
    lines.append("")
    lines.append("1. Выберите приложение для вашей платформы ниже.")
    lines.append("2. Найдите нужный файл в таблице и нажмите **Скачать**.")
    lines.append("3. В приложении выберите **Импорт из файла** или **Импорт из URL**.")    lines.append("")
    
    lines.append("### Поддерживаемые приложения")
    lines.append("")
    lines.append("| Приложение | Платформа | Описание | Ссылка |")
    lines.append("|------------|-----------|----------|--------|")
    lines.append("| **Nekobox** | Android | Лучший выбор для РФ, поддержка Reality | [Скачать](https://github.com/MatsuriDayo/nebula/releases) |")
    lines.append("| **V2RayNG** | Android | Классический клиент, стабильная работа | [Play Store](https://play.google.com/store/apps/details?id=com.v2ray.ang) |")
    lines.append("| **Happ VPN** | iOS / Android | Удобный интерфейс, работает на iPhone | [Сайт](https://happ.su) |")
    lines.append("| **SingBox** | All (PC/Mac) | Продвинутая настройка, ядро SingBox | [GitHub](https://github.com/SagerNet/sing-box) |")
    lines.append("| **FoXray** | iOS | Мощный клиент для iPhone | [App Store](https://apps.apple.com/app/foxray/id6448196107) |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- ТАБЛИЦА ФАЙЛОВ ---
    lines.append("## 📂 Доступные списки (Прямые ссылки)")
    lines.append("")
    lines.append("Файлы обновляются автоматически каждые 3 часа. Нажмите **Скачать**, чтобы получить прямой `.txt` файл.")
    lines.append("")

    category_names = {
        "nekobox": "📦 Nekobox (Reality, VLESS)",
        "v2ray": "🚀 V2RayNG (VMess, Trojan)",
        "happ": "⚡ Happ VPN (iOS/Android)",
        "singbox": "🧬 SingBox (Universal)",
        "other": "📄 Другие конфигурации"
    }

    # Сортировка категорий: сначала известные, потом остальные
    order = ["nekobox", "v2ray", "happ", "singbox"]
    all_cats = list(grouped.keys())
    sorted_cats = [c for c in order if c in all_cats] + [c for c in all_cats if c not in order]

    for cat in sorted_cats:
        configs = grouped[cat]
        if not configs:
            continue

        cat_total = sum(c["count"] for c in configs)
        title = category_names.get(cat, f"📁 {cat.upper()}")
        
        lines.append(f"### {title}")
        lines.append(f"*Всего файлов: {len(configs)} | Серверов: {cat_total}*")
        lines.append("")
        lines.append("| Название источника | Серверов | Размер | Обновлено | Действие |")
        lines.append("|--------------------|----------|--------|-----------|----------|")

        for cfg in configs:
            # Формируем прямую ссылку на файл в папке VPNMIRRORS            raw_link = f"{BASE_RAW_URL}/VPNMIRRORS/{cfg['relative_path']}"
            
            lines.append(
                f"| {cfg['name']} "
                f"| `{cfg['count']}` "
                f"| `{cfg['size_kb']} KB` "
                f"| {cfg['updated']} "
                f"| [⬇️ Скачать]({raw_link}) |"
            )
        lines.append("")

    # --- ОШИБКИ ---
    if data["errors"]:
        lines.append("---")
        lines.append("")
        lines.append("## ⚠️ Временно недоступные источники")
        lines.append("")
        lines.append("Эти источники не ответили при последнем обновлении. Они будут проверены снова через 3 часа.")
        lines.append("")
        lines.append("| Источник | Статус ошибки |")
        lines.append("|----------|---------------|")
        for err in data["errors"]:
            short_err = err["error"][:50] + "..." if len(err["error"]) > 50 else err["error"]
            lines.append(f"| {err['name']} | `{short_err}` |")
        lines.append("")

    # --- ПОДВАЛ ---
    lines.append("---")
    lines.append("")
    lines.append("ℹ️ **Информация**")
    lines.append("- Репозиторий обновляется автоматически каждые **3 часа** через CI/CD.")
    lines.append("- Все ссылки прямые, подходят для импорта в любые клиенты (v2ray, clash, singbox).")
    lines.append("- Исходный код парсера открыт. Чтобы добавить источник, отредактируйте файл `sources/urls.txt`.")
    lines.append("")
    lines.append(f"*Авто-обновление завершено: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*")

    # Запись файла
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ README.md успешно сгенерирован!")

if __name__ == "__main__":
    generate_readme()
