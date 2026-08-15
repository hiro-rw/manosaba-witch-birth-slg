# -*- coding: utf-8 -*-
"""グローバル設定（前回のプレイヤー名など）"""

import json
import os
import config

SETTINGS_PATH = os.path.join(config.SAVE_DIR, "settings.json")


def load_settings():
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    if not os.path.exists(SETTINGS_PATH):
        return {"player_name": "あなた"}
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"player_name": "あなた"}


def save_settings(data):
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_last_name():
    return load_settings().get("player_name") or "あなた"


def set_last_name(name):
    s = load_settings()
    s["player_name"] = name or "あなた"
    save_settings(s)
