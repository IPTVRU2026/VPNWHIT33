#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def generate_readme():
    meta_path = Path("configs/metadata.json")
    if not meta_path.exists():
        print("metadata.json not found. Run fetch_configs.py first")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    grouped = defaultdict(list)
    for cfg in data["configs"]:
        grouped[cfg["category"]].append(cfg)

    total_configs = sum(cfg["count"] for cfg in data["configs"])
    updated = data["updated"][:16].replace("T", " ")

    lines = []

    lines.append("# VPN White-Lists для России")
    lines.append("")
    lines.append("> **Последнее обновление:** `" + updated + " UTC`")
    lines.append(">")
    lines.append("> Источников: **" + str(data["success"]) + "** из **" + str(data["total_sources"]) + "**  |  Конфигураций: **" + str(total_configs) + "**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Как использовать")
    lines.append("")
    lines.append("1. Найди нужный файл в таблице ниже")
    lines.append("2. Нажми **Скачать** — откроется прямая ссылка на файл")
    lines.append("3. Импортируй ссылку в приложение")
    lines.append("")
    lines.append("| Приложение | Платформа | Ссылка |")
    lines.append("|------------|-----------|--------|")
    lines.append("| Nekobox | Android | [nekobox.one](https://nekobox.one) |")
    lines.append("| V2RayNG | Android | [play.google.com](https://play.google.com/store/apps/details?id=com.v2ray.ang) |")
    lines.append("| Happ VPN | Android / iOS | [happ.su](https://happ.su) |")
    lines.append("")
    lines.append("---")
    lines.append("")

    category_info = {
        "nekobox": "Nekobox — Белые листы, CIDR, VLESS, Reality",
        "v2ray":   "V2RayNG — VLESS, VMess, Trojan, Shadowsocks",
        "happ":    "Happ VPN — VLESS, Trojan, TOR Bridges",
    }

    for cat in ["nekobox", "v2ray", "happ"]:
        configs = grouped.get(cat, [])
        if not configs:
            continue

        cat_total = sum(c["count"] for c in configs)
        lines.append("## " + category_info.get(cat, cat.upper()))
        lines.append("")
        lines.append("Файлов: **" + str(len(configs)) + "**  |  Конфигураций: **" + str(cat_total) + "**")
        lines.append("")
        lines.append("| Название | Конфигов | Размер | Обновлено | Скачать |")
        lines.append("|----------|----------|--------|-----------|---------|")

        for cfg in configs:
            raw_url = (
                "https://gitverse.ru/RUVIPIEN/russian-white-bolt"
                "/raw/branch/master/configs/"
                + cfg["category"] + "/" + cfg["filename"]
            )
            lines.append(
                "| **" + cfg["name"] + "**"
                + " | `" + str(cfg["count"]) + "`"
                + " | `" + str(cfg["size_kb"]) + " KB`"
                + " | `" + cfg["updated"] + "`"
                + " | [Скачать](" + raw_url + ") |"
            )

        lines.append("")

    if data["errors"]:
        lines.append("---")
        lines.append("")
        lines.append("## Временно недоступны (" + str(len(data["errors"])) + ")")
        lines.append("")
        lines.append("| Источник | Ошибка |")
        lines.append("|----------|--------|")
        for err in data["errors"]:
            short_err = err["error"][:60] + "..." if len(err["error"]) > 60 else err["error"]
            lines.append("| " + err["name"] + " | `" + short_err + "` |")
        lines.append("")
        lines.append("> Будут проверены при следующем обновлении.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("Репозиторий автоматически обновляется каждые 3 часа через GitVerse CI/CD.")
    lines.append("")
    lines.append("Добавить источник: отредактируй `sources/urls.txt` в формате `URL|CATEGORY|NAME`")
    lines.append("")
    lines.append("*Обновлено: " + datetime.now().strftime("%Y-%m-%d %H:%M UTC") + "*")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
