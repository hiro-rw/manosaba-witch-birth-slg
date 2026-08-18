# -*- coding: utf-8 -*-
"""
actions_night.py
夜：触手調教（受胎度）／触手から因子を引き出す／就寝
触手交尾は廃止。
"""
import random

import config
from game import state as S


def tentacle_load(g):
    """
    触手調教のストレス・体力。
    館の触手レベル補正 + 女の子開発Lv軽減。
    Lv6以上は2本倍率。
    """
    train_lv = g.get("training_level", 0)
    tlv = max(1, min(config.TENTACLE_LEVEL_MAX, S.state.get("tentacle_level", 1)))

    stress = float(random.randint(*config.TENTACLE_TRAIN_STRESS))
    stamina = float(random.randint(*config.TENTACLE_TRAIN_STAMINA))

    # 触手レベル補正（1〜10）
    stress *= 1.0 + config.TENTACLE_LEVEL_STRESS_PER * (tlv - 1)
    stamina *= 1.0 + config.TENTACLE_LEVEL_STAMINA_PER * (tlv - 1)

    # 6以上：2本
    dual = tlv >= config.TENTACLE_LEVEL_DUAL
    if dual:
        stress *= config.TENTACLE_DUAL_MULT
        stamina *= config.TENTACLE_DUAL_MULT

    # 女の子の開発Lvで軽減
    stress -= train_lv * config.TENTACLE_STRESS_REDUCE_PER_LV
    stamina -= train_lv * config.TENTACLE_STAMINA_REDUCE_PER_LV

    stress = max(config.TENTACLE_STRESS_FLOOR, int(round(stress)))
    stamina = max(config.TENTACLE_STAMINA_FLOOR, int(round(stamina)))
    return stress, stamina, tlv, dual


def _check_witchify(g):
    if g.get("stress", 0) >= 100:
        g["witch_progress"] = min(100, g.get("witch_progress", 0) + random.randint(5, 12))
    elif g.get("stress", 0) >= 85:
        g["witch_progress"] = min(100, g.get("witch_progress", 0) + random.randint(1, 4))
    if g.get("witch_progress", 0) >= 100:
        from game import cycle
        cycle.trigger_witchify(g)


def apply_tentacle_train(g, silent=False):
    """受胎度・ストレス・体力のみ。妊娠なし。"""
    if g["stamina"] < 10 or S.is_period(g) or S.is_sealed(g):
        return False
    if S.is_pregnant_known(g):
        return False

    from game.characters.registry import get_module
    mod = get_module(g.get("key"))
    stress_gain, stamina_cost, tlv, dual = tentacle_load(g)

    if not silent:
        print(f"\n{'='*60}")
        print(f"  触手調教（受胎度）  ―  {g['name']}  ［触手Lv{tlv}" + ("・2本" if dual else "") + "］")
        print(f"{'='*60}")
        print(f"\n深夜。{g['name']}の部屋。")
        print(S.pick_line(g, "sleep"))
        for line in S.COMMON.get("tentacle_intro", []):
            print(line)
        if dual:
            print("触手は二本に分かれ、左右から彼女の身体を同時に攻めてくる……。")
        S.pause()
        used = False
        if mod and hasattr(mod, "on_tentacle_train"):
            result = mod.on_tentacle_train(g)
            if isinstance(result, str):
                print(result)
                used = True
            elif result:
                for line in result:
                    print(line)
                used = True
        if not used:
            for line in S.COMMON.get("tentacle_train", []):
                print(line)
            print(f"\n「{S.pick_line(g, 'tentacle_touch')}」\n")
        print("触手は受精せず、秘部を魔女向きに改造していく……。")
    else:
        extra = "（2本）" if dual else ""
        print(f"\n……触手Lv{tlv}{extra}が {g['name']} の受胎度を上げていく。")
        if mod and hasattr(mod, "on_tentacle_train"):
            result = mod.on_tentacle_train(g)
            if isinstance(result, str):
                print(result)
            elif result:
                for line in result:
                    print(line)

    before = g.get("conception", 0)
    conc_gain = random.randint(*config.TENTACLE_CONCEPTION_GAIN)
    if dual:
        conc_gain += random.randint(2, 5)
    g["stamina"] = max(0, g["stamina"] - stamina_cost)
    g["stress"] = min(100, g["stress"] + stress_gain)
    g["conception"] = min(100, before + conc_gain)
    actual = g["conception"] - before

    print(f"【結果】体力 -{stamina_cost}  ストレス +{stress_gain}  受胎度 +{actual} → {g['conception']}/100  （触手Lv{tlv}）")
    if g["conception"] >= 100:
        print("（受胎度が上限に達した。大魔女の受精が可能になる）")
    _check_witchify(g)
    if not silent:
        S.pause()
    return True


def action_tentacle_train():
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g) or S.is_period(g) or S.is_pregnant_known(g):
        print("\n今は触手調教できません。")
        S.pause()
        return False
    if g["stamina"] < 10:
        print(f"\n{g['name']}の体力が足りません。")
        S.pause()
        return False
    S.state["tentacle_action_tonight"] = True
    return apply_tentacle_train(g, silent=False)


def action_extract_factor():
    """
    触手から因子を引き出す。
    因子 +10〜20、触手レベル +1（上限10）。受胎度は増えない。
    """
    pf = S.state.get("player_factor", 0)
    tlv = S.state.get("tentacle_level", 1)
    if pf >= config.PLAYER_FACTOR_MAX and tlv >= config.TENTACLE_LEVEL_MAX:
        print("\n因子も触手レベルも上限です。")
        S.pause()
        return False

    print(f"\n{'='*60}")
    print("  触手から因子を引き出す")
    print(f"{'='*60}")
    print("あなたは影に手を伸ばし、館の触手から魔女因子を吸い上げる。")
    print("触手が、より貪欲に、より太く脈打つ……。")

    gain = random.randint(*config.EXTRACT_FACTOR_GAIN)
    if pf + gain > config.PLAYER_FACTOR_MAX:
        gain = config.PLAYER_FACTOR_MAX - pf
    S.state["player_factor"] = pf + gain

    lv_up = 0
    if tlv < config.TENTACLE_LEVEL_MAX:
        S.state["tentacle_level"] = tlv + 1
        lv_up = 1

    print(f"【結果】因子 +{gain} → {S.state['player_factor']}/{config.PLAYER_FACTOR_MAX}")
    if lv_up:
        print(f"【結果】触手レベル +1 → Lv{S.state['tentacle_level']}/{config.TENTACLE_LEVEL_MAX}")
        if S.state["tentacle_level"] >= config.TENTACLE_LEVEL_DUAL:
            print("（触手が二本に増える域に入っている。以降の調教はより苛烈になる）")
    else:
        print(f"（触手レベルは上限 Lv{config.TENTACLE_LEVEL_MAX}）")
    print("※触手レベルは下がらない。以降のすべての触手行為が重くなる。")

    S.state["tentacle_action_tonight"] = True
    S.pause()
    return True


def action_sleep():
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g):
        print(f"\n{g['name']}は封印されています。")
        S.pause()
        return False
    recover = random.randint(20, 30)
    if S.is_pregnant_known(g):
        recover = int(recover * 0.7)
    stress_down = random.randint(1, 4)
    g["stamina"] = min(g.get("max_stamina", 100), g["stamina"] + recover)
    g["stress"] = max(0, g["stress"] - stress_down)
    print(f"\n{g['name']}は眠りについた。")
    print(f"体力 +{recover}  ストレス -{stress_down}")
    S.pause()
    return True


def night_auto_tentacle():
    """触手調教・因子引き出しを選ばなかった夜、1人に調教自動。"""
    if S.state.get("tentacle_action_tonight"):
        return
    candidates = []
    for g in S.girls.values():
        if S.is_sealed(g) or S.is_period(g) or S.is_pregnant_known(g):
            continue
        if g["stamina"] < 10:
            continue
        candidates.append(g["key"])
    if not candidates:
        return
    key = random.choice(candidates)
    g = S.girls[key]
    tlv = S.state.get("tentacle_level", 1)
    print(f"\n……触手は絶倫だ（Lv{tlv}）。今夜は {g['name']} の受胎度を上げに来た。")
    apply_tentacle_train(g, silent=True)
