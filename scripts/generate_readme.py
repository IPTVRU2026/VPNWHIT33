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

    lines = []
    lines.append("# VPN configs")
    lines.append("")
    lines.append("> Auto-update every 3 hours | Last: " + data["updated"])
    lines.append("> Working sources: " + str(data["success"]) + " / " + str(data["total_sources"]))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Apps")
    lines.append("")
    lines.append("| App | Link | Supports |")
    lines.append("|-----|------|----------|")
    lines.append("| **Nekobox** | [nekobox.one](https://nekobox.one) | VLESS, VMess, Trojan, SS, Reality |")
    lines.append("| **V2RayNG** | [getv2rayng.com](https://getv2rayng.com) | VLESS, VMess, Trojan, SS |")
    lines.append("| **Happ VPN** | [happ.su](https://happ.su) | VLESS, Trojan, TOR Bridges |")
    lines.append("")
    lines.append("---")
    lines.append("")

    category_names = {
        "nekobox": "Nekobox Configs",
        "v2ray": "V2RayNG Configs",
        "happ": "Happ VPN Configs"
    }

    for cat, configs in grouped.items():
        lines.append("### " + category_names.get(cat, cat.upper()))
        lines.append("")
        for cfg in configs:
            lines.append("<details>")
            lines.append("<summary><b>" + cfg["name"] + "</b> — " + str(cfg["count"]) + " configs, " + str(cfg["size_kb"]) + " KB, " + cfg["updated"] + "</summary>")
            lines.append("")
            lines.append("| Parameter | Value |")
            lines.append("|-----------|-------|")
            lines.append("| File | " + cfg["filename"] + " |")
            lines.append("| Source | " + cfg["url"] + " |")
            lines.append("| Configs | " + str(cfg["count"]) + " |")
            lines.append("| Hash | " + cfg["hash"] + " |")
            lines.append("| Download | [configs/" + cfg["category"] + "/" + cfg["filename"] + "](configs/" + cfg["category"] + "/" + cfg["filename"] + ") |")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    if data["errors"]:
        lines.append("### Unavailable sources")
        lines.append("")
        for err in data["errors"]:
            lines.append("- " + err["name"] + " — " + err["error"][:80])
        lines.append("")
        lines.append("> Will be retried on next update.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## How auto-update works")
    lines.append("")
    lines.append("1. GitVerse Actions runs every 3 hours")
    lines.append("2. Script downloads all sources")
    lines.append("3. Parses and counts valid configs")
    lines.append("4. Generates this README")
    lines.append("5. Pushes changes to repo")
    lines.append("")
    lines.append("## Add your source")
    lines.append("")
    lines.append("1. Edit sources/urls.txt")
    lines.append("2. Format: URL|CATEGORY|NAME")
    lines.append("3. CATEGORY: nekobox | v2ray | happ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M UTC"))

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
