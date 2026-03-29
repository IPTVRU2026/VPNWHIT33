#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт скачивания и парсинга конфигураций
Сохраняет файлы в папку VPNMIRRORS
"""

import re
import time
import json
import hashlib
import requests
import base64
from datetime import datetime, timezone
from pathlib import Path

# Настройки
TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
OUTPUT_DIR = Path("VPNMIRRORS")  # Новая папка в корне
SOURCES_FILE = Path("sources/urls.txt")

# Приложения для отображения
APPS = {
    "nekobox": {"name": "Nekobox", "icon": "📦", "platform": "Android"},
    "v2ray":   {"name": "V2RayNG", "icon": "🚀", "platform": "Android"},
    "happ":    {"name": "Happ VPN", "icon": "⚡", "platform": "iOS/Android"},
    "singbox": {"name": "SingBox", "icon": "📦", "platform": "All"},
    "default": {"name": "Config", "icon": "📄", "platform": "Any"}
}

def count_configs(content: str) -> int:
    """Считает количество валидных конфигураций"""
    if not content.strip():
        return 0
    patterns = [
        r'^vless://', r'^vmess://', r'^trojan://', r'^ss://', r'^ssr://',
        r'^tuic://', r'^hysteria://', r'^hy2://', r'^\d+\.\d+\.\d+\.\d+',
        r'^bridge\s*=', r'^obfs4', r'^meek'
    ]
    count = 0
    for line in content.splitlines():
        line = line.strip()
        if any(re.match(p, line, re.I) for p in patterns):
            count += 1
    return count if count > 0 else (1 if content.strip() else 0)

def fetch_url(url: str) -> tuple:
    """Скачивает файл, пытается декодировать base64 если нужно"""
    try:        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        content = resp.text.strip()

        # Попытка декодирования, если нет явных признаков протокола
        if content and not any(c in content for c in ['://', 'bridge', 'obfs']):
            try:
                decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                if decoded.strip() and any(c in decoded for c in ['://', 'bridge']):
                    content = decoded
            except Exception:
                pass

        count = count_configs(content)
        return content, count, ""
    except Exception as e:
        return "", 0, str(e)

def save_config(name: str, category: str, content: str, count: int, url: str) -> dict:
    """Сохраняет конфиг в папку VPNMIRRORS"""
    app_info = APPS.get(category, APPS["default"])
    
    # Создаем папку, если нужно (хотя сейчас все в одну кучу или по подпапкам)
    # По вашему запросу: "файлы будут храниться загружаться все текстовые файлы... в папке VPNMIRRORS"
    # Сделаем плоскую структуру или с подкатегорией для порядка. Давайте с подкатегорией для чистоты.
    sub_dir = OUTPUT_DIR / category
    sub_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r'[^\w\-_.]', '_', name)[:40]
    filename = f"{safe_name}.txt"
    filepath = sub_dir / filename

    # Запись файла с заголовком
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n")
        f.write(f"# Source: {url}\n")
        f.write(f"# Updated: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"# Count: {count}\n\n")
        f.write(content)

    file_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    
    # Формируем относительный путь для ссылки (например: VPNMIRRORS/nekobox/file.txt)
    relative_path = f"{category}/{filename}"

    return {
        "name": name,
        "category": category,
        "filename": filename,        "relative_path": relative_path,
        "count": count,
        "url_source": url,
        "app_name": app_info["name"],
        "app_icon": app_info["icon"],
        "platform": app_info["platform"],
        "size_kb": round(len(content.encode()) / 1024, 1),
        "hash": file_hash,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    }

def main():
    print(f"Starting update: {datetime.now(timezone.utc).isoformat()}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    errors = []

    if not SOURCES_FILE.exists():
        print(f"Error: {SOURCES_FILE} not found!")
        return 1

    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('|')
        if len(parts) < 3:
            print(f"Skip invalid line: {line}")
            continue
            
        url, category, name = parts[0], parts[1].lower().strip(), parts[2].strip()

        print(f"Downloading: {name} ...")
        content, count, error = fetch_url(url)

        if error:
            errors.append({"name": name, "url": url, "error": error})
            print(f"⚠️ Warning (skipping): {error}")
            continue

        meta = save_config(name, category, content, count, url)
        results.append(meta)
        print(f"✅ OK {name}: {count} configs, {meta['size_kb']} KB")
        time.sleep(0.5) # Небольшая пауза

    # Сохраняем метаданные для генератора README
    metadata_path = OUTPUT_DIR / "metadata.json"    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump({
            "updated": datetime.now(timezone.utc).isoformat(),
            "total_sources": len(results) + len(errors),
            "success": len(results),
            "failed": len(errors),
            "configs": results,
            "errors": errors
        }, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {len(results)} success, {len(errors)} warnings")
    return 0

if __name__ == "__main__":
    exit(main())
