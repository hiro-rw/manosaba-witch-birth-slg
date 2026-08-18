# -*- coding: utf-8 -*-
"""
save_load.py
セーブスロットの保存・復元。
プロトタイプのため旧データ互換は行わない（アップデート後はニューゲーム想定）。
"""

import json
import os

import config
from game import state as S


def _list_slots():
    print("\nセーブスロット (1-5):")
    found = False
    for i in range(1, 6):
        path = os.path.join(config.SAVE_DIR, f"save_{i:02d}.json")
        if os.path.exists(path):
            found = True
            with open(path, "r", encoding="utf-8") as f:
                s = json.load(f)
            st = s.get("state", {})
            print(f"  {i}. {st.get('day', '?')}日目 "
                  f"{config.PHASE_NAMES.get(st.get('phase'), '?')} "
                  f"{st.get('player_name', '?')} 目標:{st.get('current_target', '?')}")
        else:
            print(f"  {i}. （空き）")
    return found


def do_save():
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    _list_slots()
    print("  0. キャンセル")
    try:
        c = int(input("番号 > "))
    except ValueError:
        return
    if c == 0 or not (1 <= c <= 5):
        return
    path = os.path.join(config.SAVE_DIR, f"save_{c:02d}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"state": S.state, "girls": S.girls}, f, ensure_ascii=False, indent=2)
    print(f"スロット{c}にセーブしました。")
    S.pause()


def do_load():
    print("\nロードスロット (1-5):")
    found = _list_slots()
    if not found:
        print("セーブデータがありません。")
        S.pause()
        return
    print("  0. キャンセル")
    try:
        c = int(input("番号 > "))
    except ValueError:
        return
    if c == 0 or not (1 <= c <= 5):
        return
    path = os.path.join(config.SAVE_DIR, f"save_{c:02d}.json")
    if not os.path.exists(path):
        print("空です。")
        S.pause()
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    S.state.clear()
    S.state.update(data["state"])
    S.girls.clear()
    S.girls.update(data["girls"])
    print(f"スロット{c}をロードしました。")
    S.pause()
