# -*- coding: utf-8 -*-
"""
actions_day.py
午前・午後：開発／仲良くする／エッチする／休憩／体力トレーニング
自分の行動：テクニック向上／瞑想／アルバイト
"""

import random

import config
from game import state as S
from game import fertility as F


def choose_intensity(g):
    print("\n強度を選んでください:")
    print("  1. ソフト")
    print(f"  2. ノーマル（好感目安 {config.AFFECTION_NORMAL_OK}+）")
    print(f"  3. ハード（好感目安 {config.AFFECTION_HARD_OK}+）")
    print("  0. キャンセル")
    mapping = {1: "soft", 2: "normal", 3: "hard"}
    while True:
        try:
            c = int(input("番号 > "))
            if c == 0:
                return None
            if c in mapping:
                return mapping[c]
        except ValueError:
            pass
        print("正しい番号を入力してください。")


def action_train(intensity=None):
    """開発する（強度制）。発覚済み妊娠・生理・医務室は不可。内部妊娠は可。"""
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g):
        print(f"\n{g['name']}は封印されており、開発できません。")
        S.pause()
        return False
    if S.is_in_infirmary(g):
        print(f"\n{g['name']}は医務室にいます。開発はできません（仲良くするのみ）。")
        S.pause()
        return False
    if S.is_period(g):
        print(f"\n{g['name']}は生理中です。開発は全面休止です。")
        S.pause()
        return False
    # 発覚後のみ制限（内部妊娠はネタバレせず可）
    if S.is_pregnant_known(g):
        print(f"\n{g['name']}は妊娠が分かっています。開発は控えましょう。")
        S.pause()
        return False
    if g["stamina"] < 10:
        print(f"\n{g['name']}の体力が足りません。")
        S.pause()
        return False

    if intensity is None:
        intensity = choose_intensity(g)
        if not intensity:
            return False
    if intensity not in ("soft", "normal", "hard"):
        return False

    aff = g.get("affection", 0)
    if intensity == "hard" and aff < config.AFFECTION_HARD_OK:
        print(f"\n{g['name']}は顔をしかめ、体を強張らせた。")
        print("「……そんなに強くしないで。」")
        g["affection"] = max(0, aff - random.randint(5, 12))
        g["stress"] = min(100, g["stress"] + random.randint(6, 12))
        print("【結果】ハードは早すぎた。好感度↓ ストレス↑")
        S.pause()
        return True

    print(f"\n--- 開発する：{g['name']}（{config.INTENSITY_NAMES[intensity]}）---")
    from game.characters.registry import get_module
    mod = get_module(g["key"])
    shown = False
    if mod and hasattr(mod, "on_train"):
        result = mod.on_train(g, intensity)
        if isinstance(result, str):
            print(result)
            shown = True
        elif result:
            for line in result:
                print(line)
            shown = True
    if not shown:
        from game import common_lines
        for line in common_lines.on_train(g, intensity):
            print(line)
        print(f"「{S.pick_line(g, 'train')}」")

    skill_key = {"soft": "skill_soft", "normal": "skill_normal", "hard": "skill_hard"}[intensity]
    skill_lv = S.state.get(skill_key, 0)
    bonus = 1.0 + skill_lv * 0.1

    stamina_cost = random.randint(8, 14)
    train_gain = max(1, int(random.randint(2, 5) * bonus))
    if intensity == "soft":
        train_gain = max(1, train_gain - 1)
    elif intensity == "hard":
        train_gain += 2
        if aff < config.AFFECTION_HARD_OK + 10:
            g["affection"] = max(0, aff - random.randint(0, 3))

    # 好感次第：高いとストレス軽減、低いと逆効果
    if aff >= config.AFFECTION_STRESS_RELIEF:
        stress_delta = -random.randint(3, 8)
        if intensity == "hard":
            stress_delta = -random.randint(1, 4)
    elif aff >= config.AFFECTION_NORMAL_OK:
        stress_delta = random.randint(0, 3)
    else:
        stress_delta = random.randint(3, 8)
        if intensity == "hard":
            stress_delta += 2

    g["stamina"] = max(0, g["stamina"] - stamina_cost)
    if stress_delta >= 0:
        g["stress"] = min(100, g["stress"] + stress_delta)
        stress_txt = f"ストレス +{stress_delta}"
    else:
        g["stress"] = max(0, g["stress"] + stress_delta)
        stress_txt = f"ストレス {stress_delta}"
    g["training_level"] = min(100, g.get("training_level", 0) + train_gain)
    print(f"【結果】体力 -{stamina_cost}  {stress_txt}  開発Lv +{train_gain}")
    S.pause()
    return True


def action_bond():
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g):
        print(f"\n{g['name']}は封印されています。")
        S.pause()
        return False
    g.setdefault("flags", [0, 0, 0, 0, 0])
    print(f"\n--- 仲良くする：{g['name']} ---")
    charm = S.state.get("skill_charm", 0)
    gain = random.randint(4, 9) + charm
    # ストレスケアを強化（触手負荷の主な回復手段）
    stress_down = random.randint(*config.BOND_STRESS_DOWN) + max(0, charm // 3)
    g["affection"] = min(100, g.get("affection", 0) + gain)
    g["stress"] = max(0, g["stress"] - stress_down)

    from game.characters.registry import get_module
    mod = get_module(g["key"])
    if mod and hasattr(mod, "on_bond"):
        result = mod.on_bond(g)
        if isinstance(result, str):
            print(result)
        elif result:
            for line in result:
                print(line)
    else:
        for line in S.COMMON.get("bond", ["一緒に過ごす。"]):
            print(line)

    print(f"\n【結果】好感度 +{gain} → {g['affection']}  ストレス -{stress_down}")
    S.pause()
    return True


def _apply_conceive(g, baby_type):
    """内部受胎のみ。表示・タグは付けない。"""
    g["pregnant_internal"] = True
    g["pregnancy_noticed"] = False
    g["pregnancy_days"] = 1
    g["baby_type"] = baby_type


def action_sex():
    """エッチする。発覚前は内部妊娠でも可（ネタバレなし）。"""
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g):
        print(f"\n{g['name']}は封印されています。")
        S.pause()
        return False
    if S.is_in_infirmary(g):
        print(f"\n医務室ではエッチできません。")
        S.pause()
        return False
    # 発覚後のみ不可
    if S.is_pregnant_known(g):
        print(f"\n{g['name']}は妊娠が分かっています。エッチは控えましょう。")
        S.pause()
        return False
    if S.is_period(g):
        print(f"\n{g['name']}は生理中です。エッチはできません。")
        S.pause()
        return False
    if g["stamina"] < 12:
        print(f"\n{g['name']}の体力が足りません。")
        S.pause()
        return False

    aff = g.get("affection", 0)
    # 仲良し必須：閾値未満は行動不可（フェイズ消費なし）
    if aff < config.AFFECTION_SEX_MIN:
        print(f"\n{g['name']}とは、まだその関係になれない。")
        print(f"（エッチには好感度 {config.AFFECTION_SEX_MIN} 以上が必要。いま {aff}）")
        print("先に「仲良くする」で距離を縮めよう。")
        S.pause()
        return False

    print(f"\n--- エッチする：{g['name']}（好感度 {aff}／受胎度 {g.get('conception', 0)}）---")

    from game.characters.registry import get_module
    mod = get_module(g["key"])

    lost_virgin = False
    if S.has_tag(g, "virgin"):
        lost_virgin = True
        S.remove_tag(g, "virgin")

    if mod and hasattr(mod, "on_sex"):
        result = mod.on_sex(g, aff)
        if isinstance(result, str):
            print(result)
        elif result:
            for line in result:
                print(line)
    else:
        print("互いの体温を確かめ合う。")
        if lost_virgin:
            print("（初めての壁が、静かにほどける）")
        print(f"「{S.pick_line(g, 'sex')}」")

    # 体力：開発Lvで軽減
    lv = g.get("training_level", 0)
    stamina_cost = random.randint(*config.SEX_STAMINA)
    stamina_cost = int(round(stamina_cost - lv * config.SEX_STAMINA_REDUCE_PER_LV))
    stamina_cost = max(config.SEX_STAMINA_FLOOR, stamina_cost)
    g["stamina"] = max(0, g["stamina"] - stamina_cost)

    # ストレス：好感が高いと軽減、低いと逆効果（通常は閾値以上なので軽減寄り）
    if aff >= config.AFFECTION_LOVE:
        stress_delta = -random.randint(8, 14)
    elif aff >= config.AFFECTION_STRESS_RELIEF:
        stress_delta = -random.randint(4, 10)
    else:
        stress_delta = random.randint(1, 5)
    if stress_delta >= 0:
        g["stress"] = min(100, g["stress"] + stress_delta)
        stress_txt = f"ストレス +{stress_delta}"
    else:
        g["stress"] = max(0, g["stress"] + stress_delta)
        stress_txt = f"ストレス {stress_delta}"

    human_c = F.human_fertility(g)
    witch_c = F.player_witch_fertility(g)
    conc = g.get("conception", 0)
    print(f"\n【結果】体力 -{stamina_cost}  {stress_txt}")
    print(f"  受胎度 {conc}/100  → 人間受精目安 {human_c}%  大魔女目安 {witch_c}%")
    if conc < config.CONCEPTION_WITCH_READY:
        print("  （受胎度100未満のため大魔女は着床しない／人間のみ）")
    else:
        print("  （おまんこ開発完了：大魔女専用。人間の子は着床しない）")

    if not g.get("pregnant_internal"):
        if witch_c > 0 and random.randint(1, 100) <= witch_c:
            _apply_conceive(g, "大魔女")
        elif human_c > 0 and random.randint(1, 100) <= human_c:
            _apply_conceive(g, "人間")

    if lost_virgin:
        print("（処女を失った）")
    S.pause()
    return True


def action_rest():
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g):
        print(f"\n{g['name']}は封印されています。")
        S.pause()
        return False
    recover = random.randint(22, 32)
    if S.is_pregnant_known(g):
        recover = int(recover * 0.7)
    stress_down = random.randint(1, 4)  # 体力主・ストレスは控えめ
    g["stamina"] = min(g.get("max_stamina", 100), g["stamina"] + recover)
    g["stress"] = max(0, g["stress"] - stress_down)
    print(f"\n{g['name']}を休ませました。")
    print(f"体力 +{recover}  ストレス -{stress_down}（ストレスケアは仲良くする向き）")
    S.pause()
    return True


def action_stamina_train():
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g) or S.is_in_infirmary(g):
        print(f"\n今はトレーニングできません。")
        S.pause()
        return False
    if g["stamina"] < 20:
        print(f"\n{g['name']}の体力が足りません。")
        S.pause()
        return False
    cost = random.randint(15, 22)
    gain = random.randint(2, 4)
    g["stamina"] = max(0, g["stamina"] - cost)
    g["max_stamina"] = min(150, g.get("max_stamina", 100) + gain)
    print(f"\n{g['name']}に体力トレーニングをさせた。")
    print(f"体力 -{cost}  最大体力 +{gain} → 上限 {g['max_stamina']}")
    S.pause()
    return True


def skill_upgrade_cost(current_lv):
    return config.SKILL_COST_BASE * ((current_lv + 1) ** 2)


def action_technique():
    print("\n--- テクニック向上（勉強）---")
    print("上げる項目を選んでください:")
    print("  1. 魅力（仲良くするの効率）")
    print("  2. ソフト")
    print("  3. ノーマル")
    print("  4. ハード")
    print("  0. キャンセル")
    key_map = {
        1: ("skill_charm", "魅力"),
        2: ("skill_soft", "ソフト"),
        3: ("skill_normal", "ノーマル"),
        4: ("skill_hard", "ハード"),
    }
    try:
        c = int(input("番号 > "))
    except ValueError:
        return False
    if c == 0 or c not in key_map:
        return False
    sk, label = key_map[c]
    lv = S.state.get(sk, 0)
    if lv >= config.SKILL_MAX:
        print(f"{label}はすでに最大レベル（{config.SKILL_MAX}）です。")
        S.pause()
        return False
    cost = skill_upgrade_cost(lv)
    print(f"\n{label} Lv{lv} → Lv{lv+1}  必要資金: {cost}G（所持: {S.state['money']}G）")
    if S.state["money"] < cost:
        print("資金が足りません。")
        S.pause()
        return False
    S.state["money"] -= cost
    S.state[sk] = lv + 1
    print(f"【結果】{label}が Lv{S.state[sk]} になった。資金 -{cost}G")
    print("（勉強中、目標の少女は自由に過ごしている）")
    S.pause()
    return True


def action_meditate():
    pf = S.state.get("player_factor", 0)
    if pf >= config.PLAYER_FACTOR_MAX:
        print(f"\n因子は十分に整っている（{config.PLAYER_FACTOR_MAX}）。")
        S.pause()
        return False
    gain = random.randint(*config.MEDITATE_FACTOR_GAIN)
    if pf + gain > config.PLAYER_FACTOR_MAX:
        gain = config.PLAYER_FACTOR_MAX - pf
    print("\n--- 瞑想 ---")
    S.state["player_factor"] = pf + gain
    print("静かに呼吸を整え、体内の魔女因子に意識を向ける。")
    print(f"【結果】因子 +{gain} → {S.state['player_factor']}/{config.PLAYER_FACTOR_MAX}")
    print("（触手レベルは上がらない。安全に因子を稼ぐ手段）")
    print("（その間、目標の少女は自由に過ごしている）")
    S.pause()
    return True


def action_job():
    """アルバイト。資金を増やす。目標は自由行動。"""
    pay = random.randint(config.JOB_PAY_MIN, config.JOB_PAY_MAX)
    S.state["money"] += pay
    print("\n--- アルバイト ---")
    print("館の雑務や帳簿整理などをこなし、報酬を得た。")
    print(f"【結果】資金 +{pay}G → 所持 {S.state['money']}G")
    print("（その間、目標の少女は自由に過ごしている）")
    S.pause()
    return True
