# -*- coding: utf-8 -*-
"""
save_load.py
セーブスロットの保存・復元。
"""

import json
import os

import config
from game import state as S


def do_save():
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    print("\nセーブスロット (1-5):")
    for i in range(1, 6):
        path = os.path.join(config.SAVE_DIR, f"save_{i:02d}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                s = json.load(f)
            st = s.get("state", {})
            print(f"  {i}. {st.get('day','?')}日目 "
                  f"{config.PHASE_NAMES.get(st.get('phase'),'?')} "
                  f"{st.get('player_name','?')} 目標:{st.get('current_target','?')}")
        else:
            print(f"  {i}. （空き）")
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
    found = False
    for i in range(1, 6):
        path = os.path.join(config.SAVE_DIR, f"save_{i:02d}.json")
        if os.path.exists(path):
            found = True
            with open(path, "r", encoding="utf-8") as f:
                s = json.load(f)
            st = s.get("state", {})
            print(f"  {i}. {st.get('day','?')}日目 "
                  f"{config.PHASE_NAMES.get(st.get('phase'),'?')} "
                  f"{st.get('player_name','?')} 目標:{st.get('current_target','?')}")
        else:
            print(f"  {i}. （空き）")
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
    # 新キー補完
    for k, default in (
        ("player_type", "candidate_male"),
        ("player_name", "あなた"),
        ("player_factor", 0),
        ("skill_charm", 0),
        ("skill_soft", 0),
        ("skill_normal", 0),
        ("skill_hard", 0),
        ("tentacle_action_tonight", False),
        ("births_witch", 0),
        ("births_human", 0),
        ("emma_witchified", False),
        ("all_sealed", False),
    ):
        S.state.setdefault(k, default)
    S.state.pop("guilt", None)  # 仕様：罪悪感削除
    # 旧 skill_breast 等から soft 等への簡易移行
    if S.state.get("skill_soft", 0) == 0 and S.state.get("skill_breast", 0):
        S.state["skill_soft"] = S.state.get("skill_breast", 0)
    if S.state.get("skill_normal", 0) == 0 and S.state.get("skill_pussy", 0):
        S.state["skill_normal"] = S.state.get("skill_pussy", 0)
    if S.state.get("skill_hard", 0) == 0 and S.state.get("skill_ass", 0):
        S.state["skill_hard"] = S.state.get("skill_ass", 0)

    S.girls.clear()
    S.girls.update(data["girls"])
    for g in S.girls.values():
        g.setdefault("pregnancy_noticed", S.has_tag(g, "pregnant"))
        g.setdefault("pregnant_internal", S.has_tag(g, "pregnant"))
        g.setdefault("sealed", g.get("witch_progress", 0) >= 100)
        g.setdefault("cycle_len", config.CYCLE_LEN)
        g.setdefault("period_days", 5)
        g.setdefault("flags", [0, 0, 0, 0, 0])
        g.setdefault("birth_history", [])
    print(f"スロット{c}をロードしました。")
    S.pause()
