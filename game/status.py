# -*- coding: utf-8 -*-
"""
status.py
画面表示。妊娠日数は詳細のみ。
"""

import config
from game import state as S
from game import fertility as F


def _tag_short(g, show_days=False):
    tags = []
    if S.is_sealed(g):
        tags.append("封印")
    if S.is_pregnant_known(g):
        if show_days:
            tags.append(f"妊娠{g.get('pregnancy_days', 0)}日/{g.get('baby_type') or '?'}")
        else:
            tags.append(f"妊娠({g.get('baby_type') or '?'})")
        if S.is_in_infirmary(g):
            tags.append("医務室")
    if S.has_tag(g, "virgin"):
        tags.append("処女")
    if S.has_tag(g, "lactating"):
        tags.append("授乳")
    if g.get("witch_progress", 0) > 0 and not S.is_sealed(g):
        tags.append(f"魔女{g['witch_progress']}%")
    return " ".join(tags) if tags else "—"


def show_status():
    st = S.state
    girls = S.girls
    print("\n" + "=" * 64)
    print(f"【大魔女受胎計画】 {st['day']}日目/{config.DAYS_IN_YEAR}日  "
          f"フェイズ:{config.PHASE_NAMES[st['phase']]}")
    print(f"あなた:{st.get('player_name', '？')}  資金:{st['money']}G  "
          f"因子:{st.get('player_factor', 0)}/{config.PLAYER_FACTOR_MAX}")
    print(f"テク 魅{st.get('skill_charm', 0)}/"
          f"ソ{st.get('skill_soft', 0)}/"
          f"ノ{st.get('skill_normal', 0)}/"
          f"ハ{st.get('skill_hard', 0)}")
    print("-" * 64)
    t = girls.get(st["current_target"])
    if not t:
        print("（目標が設定されていません）")
        print("=" * 64)
        return
    print(f"★目標: {t['name']}")
    print(f"  体力:{t['stamina']:3d}/{t.get('max_stamina', 100):3d}  "
          f"ストレス:{t['stress']:3d}  受胎度:{t['conception']:3d}")
    print(f"  好感:{t.get('affection', 0):3d}  開発Lv:{t.get('training_level', 0):3d}  "
          f"周期:{F.cycle_label(t)}")
    print(f"  状態: {_tag_short(t, show_days=False)}")
    print(f"  受精目安  人間:{F.human_fertility(t)}%  "
          f"大魔女(触手):{F.witch_fertility(t)}%  "
          f"大魔女(あなた):{F.player_witch_fertility(t)}%")
    print("=" * 64)


def show_status_list():
    st = S.state
    print("\n--- ステータス一覧 ---")
    for key, g in S.girls.items():
        mark = "★" if key == st["current_target"] else " "
        print(
            f"{mark}{g['name']:8s} "
            f"体{g['stamina']:3d}/{g.get('max_stamina', 100):3d} "
            f"ス{g['stress']:3d} 受{g['conception']:3d} "
            f"好{g.get('affection', 0):3d} 開{g.get('training_level', 0):3d}  "
            f"{F.cycle_label(g)}  {_tag_short(g, show_days=False)}"
        )
    S.pause()


def show_status_detail():
    keys = list(S.girls.keys())
    print("\n--- ステータス詳細：誰を見ますか ---")
    for i, key in enumerate(keys, 1):
        mark = "★" if key == S.state["current_target"] else " "
        print(f"  {i}. {mark}{S.girls[key]['name']}")
    print("  0. 戻る")
    try:
        c = int(input("番号 > "))
    except ValueError:
        return
    if c == 0 or not (1 <= c <= len(keys)):
        return
    g = S.girls[keys[c - 1]]
    print(f"\n=== {g['name']} ===")
    print(f"体力:{g['stamina']}/{g.get('max_stamina', 100)}  ストレス:{g['stress']}")
    print(f"受胎度:{g['conception']}  好感度:{g.get('affection', 0)}  "
          f"開発Lv:{g.get('training_level', 0)}")
    print(f"周期:{F.cycle_label(g)}  状態:{_tag_short(g, show_days=True)}")
    print(f"人間:{F.human_fertility(g)}%  "
          f"大魔女(触手):{F.witch_fertility(g)}%  "
          f"大魔女(あなた):{F.player_witch_fertility(g)}%")
    if g.get("baby_type") and g.get("pregnancy_noticed"):
        print(f"baby_type: {g['baby_type']}  妊娠日数: {g.get('pregnancy_days', 0)}")
    S.pause()


def change_target():
    st = S.state
    girls = S.girls
    print("\n目標を変更します:")
    keys = [k for k, g in girls.items() if S.is_usable(g)]
    if not keys:
        print("行動可能な少女がいません。")
        return
    for i, key in enumerate(keys, 1):
        mark = "★" if key == st["current_target"] else " "
        print(f"  {i}. {mark}{girls[key]['name']}")
    print("  0. キャンセル")
    while True:
        try:
            c = int(input("番号 > "))
            if c == 0:
                return
            if 1 <= c <= len(keys):
                st["current_target"] = keys[c - 1]
                print(f"\n目標を {girls[st['current_target']]['name']} に変更しました。")
                return
        except ValueError:
            pass
        print("正しい番号を入力してください。")
