# -*- coding: utf-8 -*-
"""
endings.py
エンディング到達判定と確定処理。自動終了はしない（呼び出し側で選ばせる）。
"""

import config
from game import state as S


ENDINGS = {
    "E1": "大魔女出産END",
    "E2": "全員人間出産END",
    "E3": "全員大魔女出産END",
    "E4": "エマ魔女化END",
    "E5": "駆け落ちEND",
    "E6": "処刑END",
    "E7": "心中END",
}


def _candidates():
    """エンド判定の対象少女（封印含む全員。履歴用）"""
    return list(S.girls.values())


def _active():
    return [g for g in S.girls.values() if not S.is_sealed(g)]


def list_available():
    """到達可能なエンド ID のリスト。"""
    st = S.state
    available = []
    births_w = st.get("births_witch", 0)
    births_h = st.get("births_human", 0)
    day = st.get("day", 1)

    if births_w >= 1:
        available.append("E1")

    girls = _candidates()
    if girls:
        all_human = all(
            "人間" in (g.get("birth_history") or []) for g in girls
        ) and births_w == 0 and births_h >= len(girls)
        # 履歴ベースが空なら人数カウントでも可
        if not any(g.get("birth_history") for g in girls):
            all_human = births_h >= len(girls) and births_w == 0
        else:
            all_human = all("人間" in (g.get("birth_history") or []) for g in girls) and births_w == 0
        if all_human and births_h >= 1:
            available.append("E2")

        if all("大魔女" in (g.get("birth_history") or []) for g in girls) and births_w >= len(girls):
            available.append("E3")

    if st.get("emma_witchified") or (
        S.girls.get("エマ") and S.is_sealed(S.girls["エマ"]) and S.count_usable() <= 0
    ):
        available.append("E4")

    if day >= config.DAYS_IN_YEAR:
        love100 = [g for g in _active() if g.get("affection", 0) >= 100]
        if len(love100) == 1:
            available.append("E5")

    if day > config.DAYS_IN_YEAR and births_w < 1:
        available.append("E6")

    for g in S.girls.values():
        if g.get("affection", 0) >= 100 and g.get("stress", 0) >= 90 and not S.is_sealed(g):
            available.append("E7")
            break

    # 重複除去・順序固定
    order = ["E1", "E2", "E3", "E4", "E5", "E6", "E7"]
    return [e for e in order if e in available]


def record_birth(g, baby_type):
    st = S.state
    st.setdefault("births_witch", 0)
    st.setdefault("births_human", 0)
    hist = g.setdefault("birth_history", [])
    if baby_type == "大魔女":
        st["births_witch"] = st.get("births_witch", 0) + 1
        if "大魔女" not in hist:
            hist.append("大魔女")
    else:
        st["births_human"] = st.get("births_human", 0) + 1
        if "人間" not in hist:
            hist.append("人間")


def _print_result(text):
    if isinstance(text, str):
        print(text)
    elif text:
        for line in text:
            print(line)


def resolve(ending_id):
    """エンド確定。エピローグ表示。"""
    name = ENDINGS.get(ending_id, ending_id)
    print("\n" + "=" * 64)
    print(f"  {name}")
    print("=" * 64)

    if ending_id == "E1":
        print("大魔女がこの世に生を受けた。")
        print("計画は果たされ、少女たちにも、あなたにも、外への道が開かれる。")
    elif ending_id == "E2":
        print("全員が、人間の子を産み終えた。")
        print("大魔女はまだ遠い。だが調教師としての腕は確かだ。")
        print("あなたはここで、次の機会を待つことになる……。")
    elif ending_id == "E3":
        print("全員が大魔女を宿し、産み落とした。")
        print("世界の傾きが、誰にも止められないものになっていく……。")
    elif ending_id == "E4":
        print("エマの魔女化が、すべてを飲み込む。")
        print("他の候補も光を失い、館に静寂だけが残る。")
    elif ending_id == "E5":
        love = [g for g in _active() if g.get("affection", 0) >= 100]
        g = love[0] if love else None
        if g:
            from game.characters.registry import get_module
            mod = get_module(g["key"])
            if mod and hasattr(mod, "on_ending_elope"):
                _print_result(mod.on_ending_elope(g))
            else:
                print(f"あなたは{g['name']}の手を取り、牢屋敷を出た。")
        else:
            print("想い人とともに、ここを離れる。")
    elif ending_id == "E6":
        print("期限は過ぎた。成果は示せなかった。")
        print("ゴクチョーの裁定により、あなたは処刑される。")
    elif ending_id == "E7":
        cands = [
            g for g in S.girls.values()
            if g.get("affection", 0) >= 100 and g.get("stress", 0) >= 90 and not S.is_sealed(g)
        ]
        if len(cands) > 1:
            print("誰と心中しますか？")
            for i, g in enumerate(cands, 1):
                print(f"  {i}. {g['name']}")
            try:
                c = int(input("番号 > "))
                g = cands[c - 1] if 1 <= c <= len(cands) else cands[0]
            except (ValueError, IndexError):
                g = cands[0]
        else:
            g = cands[0] if cands else None
        if g:
            from game.characters.registry import get_module
            mod = get_module(g["key"])
            if mod and hasattr(mod, "on_ending_shinju"):
                _print_result(mod.on_ending_shinju(g))
            else:
                print(f"{g['name']}は、魔女になるくらいならと、あなたと終わりを選んだ。")
        else:
            print("想いとストレスが、二人を飲み込む。")
    else:
        print("（エンド）")

    print("\n=== END ===")
    S.pause()
    return True


def menu_endings():
    """システムから呼ばれる。到達可能なエンドを選ばせる。"""
    avail = list_available()
    print("\n--- エンディングへ ---")
    if not avail:
        print("現在、確定できるエンディングはありません。")
        print("（条件を満たすとここに表示されます）")
        S.pause()
        return False
    for i, eid in enumerate(avail, 1):
        print(f"  {i}. {ENDINGS[eid]}（{eid}）")
    print("  0. キャンセル")
    try:
        c = int(input("番号 > "))
    except ValueError:
        return False
    if c == 0 or not (1 <= c <= len(avail)):
        return False
    resolve(avail[c - 1])
    return "ended"
