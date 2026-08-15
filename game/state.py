# -*- coding: utf-8 -*-
"""
state.py
少女データ・プレイヤー状態の保持、タグ操作。
少女定義は game/characters/（1人1ファイル）。
"""

import json
import random
import os

import config

girls = {}
state = {}
COMMON = {}


def load_common():
    global COMMON
    if os.path.exists(config.COMMON_PATH):
        with open(config.COMMON_PATH, "r", encoding="utf-8") as f:
            COMMON = json.load(f)
    else:
        COMMON = {}
    return COMMON


def load_girls():
    """game/characters/ の INITIAL からニューゲーム用データを載せる。"""
    global girls
    # パッケージ経由より直接モジュール指定の方が環境差に強い
    from game.characters.registry import all_initials
    girls = all_initials()
    for data in girls.values():
        data.setdefault("max_stamina", 100)
        data.setdefault("training_level", 0)
        data.setdefault("pregnancy_days", 0)
        data.setdefault("witch_progress", 0)
        # ニューゲーム時は周期を完全ランダム（INITIAL の固定値は上書き）
        data["cycle_len"] = config.CYCLE_LEN + random.randint(-2, 2)
        data["period_days"] = random.randint(4, 6)
        data["cycle_day"] = random.randint(1, data["cycle_len"])
        data.setdefault("affection", 0)
        data.setdefault("baby_type", None)
        data.setdefault("conception", 0)
        data.setdefault("tags", ["virgin"])
        data.setdefault("lines", {})
        data.setdefault("flags", [0, 0, 0, 0, 0])
        # 妊娠発覚前フラグ（True になるまでステータスに妊娠と出さない）
        data.setdefault("pregnancy_noticed", False)
        data.setdefault("pregnant_internal", False)
        # 封印（魔女化後）
        data.setdefault("sealed", False)
        # 部位システム廃止。旧セーブに parts があっても使わない
        data.pop("parts", None)
    return girls


def init_state(player_name="あなた"):
    """ゲーム開始時のプレイヤー状態（因子持ち男性候補）。"""
    global state
    state = {
        "day": 1,
        "phase": "morning",
        "money": 5000,
        "current_target": list(girls.keys())[0] if girls else None,
        "tentacle_action_tonight": False,
        "player_type": "candidate_male",
        "player_name": player_name or "あなた",
        "player_factor": 0,
        "births_witch": 0,
        "births_human": 0,
        "emma_witchified": False,
        "all_sealed": False,
        "skill_charm": 0,
        "skill_soft": 0,
        "skill_normal": 0,
        "skill_hard": 0,
        # 旧セーブ互換（読み込み時に無視可）
        "skill_breast": 0,
        "skill_pussy": 0,
        "skill_ass": 0,
    }
    return state


def save_girl_file(girl):
    """定義ファイルは書き換えない。互換のため残す。"""
    return


def has_tag(g, tag):
    return tag in g.get("tags", [])


def add_tag(g, tag):
    if tag not in g.get("tags", []):
        g.setdefault("tags", []).append(tag)


def remove_tag(g, tag):
    if tag in g.get("tags", []):
        g["tags"].remove(tag)


def is_sealed(g):
    return g.get("sealed") or g.get("witch_progress", 0) >= 100


def is_usable(g):
    """行動可能な候補か。"""
    return not is_sealed(g)


def is_period(g):
    """生理期か。発覚済み妊娠中は周期停止なので False。"""
    if has_tag(g, "pregnant") or g.get("pregnant_internal"):
        # 発覚前でも内部妊娠中は「生理が来ない」扱い → 生理ではない
        if g.get("pregnant_internal") and not g.get("pregnancy_noticed"):
            return False
        if has_tag(g, "pregnant"):
            return False
    period_len = g.get("period_days", 5)
    return 1 <= g.get("cycle_day", 1) <= period_len


def is_ovulation(g):
    if has_tag(g, "pregnant") or g.get("pregnant_internal"):
        return False
    clen = max(20, g.get("cycle_len", config.CYCLE_LEN))
    # 中ほどに幅を持たせる
    mid = clen // 2
    return (mid - 2) <= g.get("cycle_day", 1) <= (mid + 2)


def is_pregnant_known(g):
    """プレイヤーに妊娠が分かっているか。"""
    return has_tag(g, "pregnant") and g.get("pregnancy_noticed", True)


def is_in_infirmary(g):
    """出産直前の医務室状態。"""
    if not has_tag(g, "pregnant"):
        return False
    return g.get("pregnancy_days", 0) >= config.INFIRMARY_FROM_DAY


def count_usable():
    return sum(1 for g in girls.values() if is_usable(g))


def get_tier(level):
    if level < config.TRAIN_TIER_MID:
        return "low"
    if level < config.TRAIN_TIER_HIGH:
        return "mid"
    return "high"


def pick_line(g, base):
    tier = get_tier(g.get("training_level", 0))
    lines = g.get("lines", {})
    key = f"{base}_{tier}"
    if key in lines and lines[key]:
        return random.choice(lines[key])
    for t in ("low", "mid", "high"):
        k = f"{base}_{t}"
        if k in lines and lines[k]:
            return random.choice(lines[k])
    if base in lines and lines[base]:
        return random.choice(lines[base])
    return "……"


def player_name():
    return state.get("player_name") or "あなた"


def pause():
    input("\n[Enterで続ける]")


def bootstrap():
    """起動時（名前入力前に少女定義だけ載せる場合もある）。"""
    load_common()
    load_girls()
    # state は main で名前入力後に init_state
