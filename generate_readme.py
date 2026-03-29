#!/usr/bin/env python3оhj
# -*- coding: utf-8 -*-
g
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

    readme = "# VPN configs

"
    readme += "> Auto-update every 3 hours | Last: " + data["updated"] + "
"
    readme += "> Working sources: " + str(data["success"]) + " / " + str(data["total_sources"]) + "

"
    readme += "---

"
    readme += "## Apps

"
    readme += "| App | Link | Supports |
"
    readme += "|-----|------|----------|
"
    readme += "| **Nekobox** | [nekobox.one](https://nekobox.one) | VLESS, VMess, Trojan, SS, Reality |
"
    readme += "| **V2RayNG** | [getv2rayng.com](https://getv2rayng.com) | VLESS, VMess, Trojan, SS |
"
    readme += "| **Happ VPN** | [happ.su](https://happ.su) | VLESS, Trojan, TOR Bridges |
"
    readme += "
---

"

    category_names = {
        "nekobox": "Nekobox Configs",
        "v2ray": "V2RayNG Configs",
        "happ": "Happ VPN Configs"
    }

    for cat, configs in grouped.items():
        readme += "### " + category_names.get(cat, cat.upper()) + "

"
        for cfg in configs:
            readme += "<details>
"
            readme += "<summary><b>" + cfg["name"] + "</b> — " + str(cfg["count"]) + " configs, " + str(cfg["size_kb"]) + " KB, " + cfg["updated"] + "</summary>

"
            readme += "| Parameter | Value |
"
            readme += "|-----------|-------|
"
            readme += "| File | " + cfg["filename"] + " |
"
            readme += "| Source | " + cfg["url"] + " |
"
            readme += "| Configs | " + str(cfg["count"]) + " |
"
            readme += "| Hash | " + cfg["hash"] + " |
"
            readme += "| Download | [configs/" + cfg["category"] + "/" + cfg["filename"] + "](configs/" + cfg["category"] + "/" + cfg["filename"] + ") |
"
            readme += "
</details>

"

    if data["errors"]:
        readme += "### Unavailable sources

"
        for err in data["errors"]:
            readme += "- " + err["name"] + " — " + err["error"][:80] + "
"
        readme += "
> Will be retried on next update.

"

    readme += "---

"
    readme += "## How auto-update works

"
    readme += "1. GitVerse Actions runs every 3 hours
"
    readme += "2. Script downloads all sources
"
    readme += "3. Parses and counts valid configs
"
    readme += "4. Generates this README
"
    readme += "5. Pushes changes to repo

"
    readme += "## Add your source

"
    readme += "1. Edit sources/urls.txt
"
    readme += "2. Format: URL|CATEGORY|NAME
"
    readme += "3. CATEGORY: nekobox | v2ray | happ

"
    readme += "---

"
    readme += "> Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M UTC") + "
"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
