# -*- coding: utf-8 -*-
"""
fertility.py
受胎度A案：
  0〜99 → 大魔女 0% / 人間は周期どおり
  100   → 大魔女のみ（因子＋周期） / 人間 0%
触手では妊娠しない。
"""
from game import state as S
import config


def human_fertility(g):
    """人間の子。受胎度100では 0。発覚妊娠・生理は 0。"""
    if S.is_pregnant_known(g) or S.is_period(g):
        return 0
    if g.get("conception", 0) >= config.CONCEPTION_WITCH_READY:
        return 0
    if S.is_ovulation(g):
        return 55
    d = g.get("cycle_day", 1)
    if d <= g.get("period_days", 5):
        return 0
    return 8


def player_witch_fertility(g):
    """大魔女。受胎度が100未満は常に 0。"""
    if S.is_pregnant_known(g) or S.is_period(g):
        return 0
    if g.get("conception", 0) < config.CONCEPTION_WITCH_READY:
        return 0
    factor = S.state.get("player_factor", 0)
    pct = config.PLAYER_WITCH_BASE_PCT + factor * config.PLAYER_WITCH_PER_FACTOR
    if S.is_ovulation(g):
        pct *= 1.5
    else:
        pct *= 0.4
    return max(0, min(45, int(pct)))


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
