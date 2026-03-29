#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Генерация красивого README.md с конфигами
"""

import json
from pathlib import Path
from datetime import datetime

def generate_readme():
    meta_path = Path("configs/metadata.json")
        if not meta_path.exists():
                print("❌ metadata.json не найден. Запустите сначала fetch_configs.py")
                        return
                            
                                with open(meta_path, 'r', encoding='utf-8') as f:
                                        data = json.load(f)
                                            
                                                # Группировка по категориям
                                                    from collections import defaultdict
                                                        grouped = defaultdict(list)
                                                            for cfg in data["configs"]:
                                                                    grouped[cfg["category"]].append(cfg)
                                                                        
                                                                            readme = f"""# 🔐 VPN для обхода White-листов

                                                                            > ⚡ **Авто-обновление**: каждые 3 часа | 🔄 Последнее: `{data["updated"]}`  
                                                                            > ✅ Рабочих источников: `{data["success"]}` / `{data["total_sources"]}`

                                                                            ---

                                                                            ## 📱 Приложения для подключения

                                                                            | Приложение | Иконка | Ссылка | Поддерживает |
                                                                            |------------|--------|--------|--------------|
                                                                            | **Nekobox** | 🦊 | [nekobox.one](https://nekobox.one) | VLESS, VMess, Trojan, SS, Reality |
                                                                            | **V2RayNG** | ⚡ | [getv2rayng.com](https://getv2rayng.com) | VLESS, VMess, Trojan, SS |
                                                                            | **Happ VPN** | 🎯 | [happ.su](https://happ.su) | VLESS, Trojan, TOR Bridges |

                                                                            > 💡 Все конфигурации ниже работают на **всех платформах**: Android, iOS, Windows, macOS, Linux

                                                                            ---

                                                                            """
                                                                                
                                                                                    # Блоки по категориям
                                                                                        category_names = {
                                                                                                    "nekobox": "🦊 Nekobox Configs",
                                                                                                            "v2ray": "⚡ V2RayNG Configs",         "happ": "🎯 Happ VPN Configs"
                                                                                        }
                                                                                            
                                                                                                for cat, configs in grouped.items():
                                                                                                        readme += f"### {category_names.get(cat, cat.upper())}\n\n"
                                                                                                                for cfg in configs:
                                                                                                                            readme += f"""<details>
                                                                                                                            <summary><b>{cfg["app_icon"]} {cfg["name"]}</b> — {cfg["count"]} конфигов · {cfg["size_kb"]} КБ · <code>{cfg["updated"]}</code></summary>

                                                                                                                            | Параметр | Значение |
                                                                                                                            |----------|----------|
                                                                                                                            | 📦 Файл | `{cfg["filename"]}` |
                                                                                                                            | 🔗 Источник | [Открыть]({cfg["url"]}) |
                                                                                                                            | 📊 Конфигураций | `{cfg["count"]}` |
                                                                                                                            | 🔐 Хэш | `{cfg["hash"]}` |
                                                                                                                            | 📥 Скачать | [🦊 Nekobox](configs/{cfg["category"]}/{cfg["filename"]}) · [⚡ V2Ray](configs/{cfg["category"]}/{cfg["filename"]}) · [🎯 Happ](configs/{cfg["category"]}/{cfg["filename"]}) |

                                                                                                                            > ⚠️ Нажмите на ссылку скачивания → «Сохранить ссылку как» → импортируйте в приложение

                                                                                                                            </details>

                                                                                                                            """
                                                                                                                                
                                                                                                                                    # Секция ошибок (если есть)
                                                                                                                                        if data["errors"]:
                                                                                                                                                readme += "### ⚠️ Временно недоступные источники\n\n"
                                                                                                                                                        for err in data["errors"]:
                                                                                                                                                                    readme += f"- `{err['name']}` — `{err['error']}`\n"
                                                                                                                                                                            readme += "\n> Они будут проверены при следующем обновлении.\n\n"
                                                                                                                                                                                
                                                                                                                                                                                    # Футер
                                                                                                                                                                                        readme += f"""---

                                                                                                                                                                                        ## 🔄 Как работает авто-обновление

                                                                                                                                                                                        1. 🤖 **GitHub Actions** запускается каждые 3 часа
                                                                                                                                                                                        2. 📥 Скрипт скачивает все 57 источников
                                                                                                                                                                                        3. 🔍 Парсит и считает валидные конфигурации
                                                                                                                                                                                        4. 🎨 Генерирует этот README с актуальной статистикой
                                                                                                                                                                                        5. 💾 Пушит изменения в репозиторий

                                                                                                                                                                                        > ⏱️ Следующее обновление: ~через 3 часа от последнего коммита

                                                                                                                                                                                        ## 🛠️ Добавить свой источник

                                                                                                                                                                                        1. Отредактируйте `sources/urls.txt`
                                                                                                                                                                                        2. Формат: `URL|CATEGORY|NAME`
                                                                                                                                                                                        3. CATEGORY: `nekobox` | `v2ray` | `happ`
                                                                                                                                                                                        4. Создайте PR — бот проверит и добавит!
                                                                                                                                                                                        ---

                                                                                                                                                                                        > 🇷🇺 Сделано для обхода ограничений | Не хранит логи | Только публичные источники  
                                                                                                                                                                                        > 🕒 Обновлено: `{datetime.now().strftime("%Y-%m-%d %H:%M UTC")}`

                                                                                                                                                                                        *Если конфиги перестали работать — проверьте обновления или напишите в Issues.*
                                                                                                                                                                                        """
                                                                                                                                                                                            
                                                                                                                                                                                                with open("README.md", 'w', encoding='utf-8') as f:
                                                                                                                                                                                                        f.write(readme)
                                                                                                                                                                                                            
                                                                                                                                                                                                                print("✅ README.md сгенерирован")

                                                                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                                                                    generate_readme()
                                                                                        }