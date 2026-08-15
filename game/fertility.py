# -*- coding: utf-8 -*-
"""
fertility.py
受精確率。
表示用は発覚前の内部妊娠を無視（0%に落とさない）。
実際の着床判定は呼び出し側で pregnant_internal を見てスキップする。
"""

from game import state as S
import config


def human_fertility(g):
    """表示・参考用。発覚済み妊娠・生理のみ 0。"""
    if S.is_pregnant_known(g) or S.is_period(g):
        return 0
    if S.is_ovulation(g):
        return 55
    d = g.get("cycle_day", 1)
    period_len = g.get("period_days", 5)
    if d <= period_len:
        return 0
    return 8


def witch_fertility(g):
    """触手交尾用。発覚済み妊娠・生理のみ 0。開発Lvは成功率に直接乗せない（耐性は負荷側）。"""
    if S.is_pregnant_known(g) or S.is_period(g):
        return 0
    base = g.get("conception", 0) * 0.28
    if S.is_ovulation(g):
        base += 18 + g.get("conception", 0) * 0.15
    else:
        base *= 0.35
    return max(0, min(55, int(base)))


def player_witch_fertility(g):
    """
    エッチでの大魔女確率。
    player_factor 0〜100。上限付近で触手よりは低いが十分狙える。
    """
    if S.is_pregnant_known(g) or S.is_period(g):
        return 0
    factor = S.state.get("player_factor", 0)
    pct = config.PLAYER_WITCH_BASE_PCT + factor * config.PLAYER_WITCH_PER_FACTOR
    if S.is_ovulation(g):
        pct *= 1.4
    else:
        pct *= 0.45
    return max(0, min(35, int(pct)))


def cycle_label(g):
    if S.is_pregnant_known(g):
        bt = g.get("baby_type") or "？"
        return f"妊娠中({bt}) 周期停止"
    d = g.get("cycle_day", 1)
    period_len = g.get("period_days", 5)
    clen = g.get("cycle_len", config.CYCLE_LEN)
    if 1 <= d <= period_len:
        return f"生理期({d}日目)"
    mid = max(1, clen // 2)
    if (mid - 2) <= d <= (mid + 2):
        return f"排卵期({d}日目)"
    if d < mid:
        return f"安全期前半({d}日目)"
    return f"安全期後半({d}日目)"
