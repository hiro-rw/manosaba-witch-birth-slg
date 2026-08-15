# -*- coding: utf-8 -*-
"""
common_lines.py
共通の地の文。個人の on_* から任意で呼ぶ。
"""

import random

from game import state as S


def on_train(g, intensity="normal"):
    """強度調教の共通地の文。性感帯はテキストでランダムに触れる。"""
    soft = [
        "指先でゆっくりと体温を確かめるように撫でていく。",
        "急かさず、息がかかる距離で体をほどいていく。",
    ]
    normal = [
        "甘い刺激を重ね、感度の良い場所を丁寧に開いていく。",
        "胸から腰へ、視線と手のひらで反応を拾っていく。",
    ]
    hard = [
        "ためらいを残さず、奥まで届く刺激を繰り返す。",
        "腰が逃げるのを許さず、快感の波を押し付けていく。",
    ]
    pool = {"soft": soft, "normal": normal, "hard": hard}.get(intensity, normal)
    return [random.choice(pool)]


def on_breast(g, tier=None):
    pool = S.COMMON.get("breast") or [
        "ゆっくりと胸を包み込むように撫でていく。",
    ]
    return [random.choice(pool)]


def on_pussy(g, tier=None):
    pool = S.COMMON.get("pussy") or [
        "秘部に指を這わせ、割れ目を優しく撫でていく。",
    ]
    return [random.choice(pool)]


def on_ass(g, tier=None):
    pool = S.COMMON.get("ass") or [
        "尻の柔らかい肉を両手で包み、ゆっくりと揉みしだく。",
    ]
    return [random.choice(pool)]


def on_bond(g):
    pool = S.COMMON.get("bond") or ["二人で静かな時間を過ごす。"]
    return [random.choice(pool)]


def on_sex_foreplay(g):
    return list(S.COMMON.get("sex_foreplay") or ["互いの体温を確かめ合う。"])


def on_sex_enter(g):
    return list(S.COMMON.get("sex_enter") or ["慎重に、奥へと沈んでいく。"])


def on_sex_climax(g):
    return list(S.COMMON.get("sex_climax") or ["甘い吐息とともに、ピークが訪れる。"])
