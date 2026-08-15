# -*- coding: utf-8 -*-
"""
config.py
定数・バランス。仕様書の数値はここを中心に調整する。
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")
COMMON_PATH = os.path.join(BASE_DIR, "common_texts.json")

DAYS_IN_YEAR = 365
PREGNANCY_DAYS_TO_BIRTH = 100
CYCLE_LEN = 28

PHASES = ["morning", "afternoon", "night"]
PHASE_NAMES = {"morning": "午前", "afternoon": "午後", "night": "夜中"}

INTENSITY_NAMES = {
    "soft": "ソフト",
    "normal": "ノーマル",
    "hard": "ハード",
}
AFFECTION_NORMAL_OK = 30
AFFECTION_HARD_OK = 60
AFFECTION_REFUSE = 30
AFFECTION_LOVE = 71

TRAIN_TIER_MID = 21
TRAIN_TIER_HIGH = 51

SKILL_MAX = 10
SKILL_COST_BASE = 500

JOB_PAY_MIN = 800
JOB_PAY_MAX = 1500

# 触手：基準ストレス＋20前後。交尾＞調教。開発Lvで軽減
TENTACLE_TRAIN_STRESS = (18, 22)
TENTACLE_SEX_STRESS = (22, 28)
TENTACLE_TRAIN_STAMINA = (14, 20)
TENTACLE_SEX_STAMINA = (20, 28)
# 開発Lv 1 あたりの軽減（下限は別途）
TENTACLE_STRESS_REDUCE_PER_LV = 0.12
TENTACLE_STAMINA_REDUCE_PER_LV = 0.10
TENTACLE_STRESS_FLOOR = 6
TENTACLE_STAMINA_FLOOR = 8

# プレイヤー因子（瞑想）
PLAYER_FACTOR_MAX = 100
PLAYER_WITCH_BASE_PCT = 1.0
PLAYER_WITCH_PER_FACTOR = 0.25  # 100時 +25 → ベースと合わせて上限側でキャップ

INFIRMARY_FROM_DAY = 95
