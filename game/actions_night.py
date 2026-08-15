# -*- coding: utf-8 -*-
"""
actions_night.py
夜中：触手調教／触手交尾／就寝／自動触手。
- プレイヤーが選んだ触手交尾：処女なら処女喪失
- 自動触手：処女には交尾しない（調教のみ）
- ストレスは必ず上昇
"""

import random

import config
from game import state as S
from game import fertility as F


def tentacle_load(g, kind="train"):
    """
    触手のストレス・体力。kind: train / sex
    開発Lvで軽減（下限あり）。触手では開発Lvを上げない。
    """
    lv = g.get("training_level", 0)
    if kind == "sex":
        stress = random.randint(*config.TENTACLE_SEX_STRESS)
        stamina = random.randint(*config.TENTACLE_SEX_STAMINA)
    else:
        stress = random.randint(*config.TENTACLE_TRAIN_STRESS)
        stamina = random.randint(*config.TENTACLE_TRAIN_STAMINA)
    stress = int(round(stress - lv * config.TENTACLE_STRESS_REDUCE_PER_LV))
    stamina = int(round(stamina - lv * config.TENTACLE_STAMINA_REDUCE_PER_LV))
    stress = max(config.TENTACLE_STRESS_FLOOR, stress)
    stamina = max(config.TENTACLE_STAMINA_FLOOR, stamina)
    return stress, stamina



def apply_tentacle_train(g, silent=False):
    if g["stamina"] < 10 or S.is_period(g) or S.is_sealed(g):
        return False
    if S.is_pregnant_known(g):
        return False

    from game.characters.registry import get_module
    mod = get_module(g.get("key"))
    if not silent:
        print(f"\n{'='*60}")
        print(f"  触手調教  ―  {g['name']}")
        print(f"{'='*60}")
        print(f"\n深夜。{g['name']}の部屋。")
        print(S.pick_line(g, "sleep"))
        for line in S.COMMON.get("tentacle_intro", []):
            print(line)
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
    else:
        print(f"\n……触手が {g['name']} の元で、体を開発していく。")

    stress_gain, stamina_cost = tentacle_load(g, "train")
    conc_gain = random.randint(8, 16)
    g["stamina"] = max(0, g["stamina"] - stamina_cost)
    g["stress"] = min(100, g["stress"] + stress_gain)
    g["conception"] = min(100, g["conception"] + conc_gain)
    # 触手では開発Lvは上がらない
    print(f"【結果】体力 -{stamina_cost}  ストレス +{stress_gain}  受胎度 +{conc_gain}（開発Lvは変化なし）")
    _check_witchify(g)
    if not silent:
        S.pause()
    return True


def apply_tentacle_sex(g, silent=False, allow_take_virgin=True):
    """
    触手交尾。
    allow_take_virgin: プレイヤー操作時 True。自動時は処女に呼ばない想定。
    """
    if g["stamina"] < 12 or S.is_period(g) or S.is_sealed(g):
        if not silent:
            print(f"\n今は触手交尾できません。")
            S.pause()
        return False
    if S.is_pregnant_known(g):
        if not silent:
            print(f"\n{g['name']}は妊娠が分かっています。")
            S.pause()
        return False
    # 自動などで処女に交尾させない
    if S.has_tag(g, "virgin") and not allow_take_virgin:
        return False

    from game.characters.registry import get_module
    mod = get_module(g.get("key"))
    if not silent:
        print(f"\n{'='*60}")
        print(f"  触手交尾（大魔女受胎）  ―  {g['name']}")
        print(f"{'='*60}")
        print(f"\n深夜。{g['name']}の部屋。")
        print(S.pick_line(g, "sleep"))
        for line in S.COMMON.get("tentacle_intro", []):
            print(line)
        S.pause()
        used = False
        if mod and hasattr(mod, "on_tentacle_sex"):
            result = mod.on_tentacle_sex(g)
            if isinstance(result, str):
                print(result)
                used = True
            elif result:
                for line in result:
                    print(line)
                used = True
        if not used:
            print("触手は脚をそっと開き、秘部に先端を寄せる。")
            print(f"「{S.pick_line(g, 'tentacle_touch')}」")
            S.pause()
            for line in S.COMMON.get("tentacle_enter", []):
                print(line)
            print(f"「{S.pick_line(g, 'tentacle_deep')}」")
            for line in S.COMMON.get("tentacle_womb", []):
                print(line)
            print(f"{g['name']}の腰が小さく浮く。")
            S.pause()
            for line in S.COMMON.get("tentacle_fill", []):
                print(line)
            print(f"「{S.pick_line(g, 'tentacle_climax')}」")
            print(f"「{S.pick_line(g, 'tentacle_after')}」")
    else:
        print(f"\n……触手が {g['name']} に交尾を仕掛けた。")

    # プレイヤー選択の触手交尾：処女なら喪失
    lost_virgin = False
    if allow_take_virgin and S.has_tag(g, "virgin"):
        lost_virgin = True
        S.remove_tag(g, "virgin")

    stress_gain, stamina_cost = tentacle_load(g, "sex")
    # 交尾は判定中心。受胎度は微増
    conc_gain = random.randint(0, 4)
    g["stamina"] = max(0, g["stamina"] - stamina_cost)
    g["stress"] = min(100, g["stress"] + stress_gain)
    g["conception"] = min(100, g["conception"] + conc_gain)
    # 触手では開発Lvは上がらない

    chance = F.witch_fertility(g)
    print(f"【結果】体力 -{stamina_cost}  ストレス +{stress_gain}  受胎度 +{conc_gain}  大魔女受精目安 {chance}%（開発Lvは変化なし）")
    if lost_virgin:
        print("（触手交尾により、処女を失った）")

    # 内部妊娠中は着床判定のみスキップ（表示は通常）
    if not g.get("pregnant_internal") and not S.has_tag(g, "pregnant"):
        if g["conception"] >= 40 and chance > 0 and random.randint(1, 100) <= chance:
            g["pregnant_internal"] = True
            g["pregnancy_noticed"] = False
            g["pregnancy_days"] = 1
            g["baby_type"] = "大魔女"
            # ネタバレ文は出さない

    _check_witchify(g)
    if not silent:
        S.pause()
    return True


def _check_witchify(g):
    if g["stress"] >= 80:
        g["witch_progress"] = min(100, g.get("witch_progress", 0) + random.randint(3, 10))
        print(f"警告: 魔女化 {g['witch_progress']}%")
    if g.get("witch_progress", 0) >= 100 and not g.get("sealed"):
        from game.cycle import trigger_witchify
        trigger_witchify(g)


def action_tentacle_train():
    g = S.girls[S.state["current_target"]]
    ok = apply_tentacle_train(g, silent=False)
    if ok:
        S.state["tentacle_action_tonight"] = True
    return ok


def action_tentacle_sex():
    """プレイヤー操作：処女でも交尾可（処女喪失）。"""
    g = S.girls[S.state["current_target"]]
    ok = apply_tentacle_sex(g, silent=False, allow_take_virgin=True)
    if ok:
        S.state["tentacle_action_tonight"] = True
    return ok


def action_sleep():
    g = S.girls[S.state["current_target"]]
    if S.is_sealed(g):
        print(f"\n{g['name']}は封印されています。")
        S.pause()
        return False
    recover = random.randint(20, 30)
    if S.is_pregnant_known(g):
        recover = int(recover * 0.75)
    stress_down = random.randint(4, 9)
    g["stamina"] = min(g.get("max_stamina", 100), g["stamina"] + recover)
    g["stress"] = max(0, g["stress"] - stress_down)
    print(f"\n{g['name']}を就寝させた。")
    print(f"体力 +{recover}  ストレス -{stress_down}")
    S.pause()
    return True


def night_auto_tentacle():
    """
    自動触手。
    処女には交尾しない（調教のみ）。
    """
    if S.state.get("tentacle_action_tonight"):
        return
    candidates = []
    for key, g in S.girls.items():
        if S.is_sealed(g) or S.is_period(g) or S.is_pregnant_known(g):
            continue
        if g["stamina"] < 10:
            continue
        candidates.append(key)
    if not candidates:
        print("\n（今夜、触手が訪れるのに適した少女はいなかった）")
        S.pause()
        return

    # 交尾候補：処女ではない・内部妊娠でも見込み表示はするが交尾で着床はスキップ
    fertile = []
    for k in candidates:
        g = S.girls[k]
        if S.has_tag(g, "virgin"):
            continue  # 処女には自動交尾しない
        if g.get("pregnant_internal"):
            continue  # 内部妊娠中は自動交尾より調教側へ
        if S.is_ovulation(g) or g.get("conception", 0) >= 40:
            fertile.append(k)

    if fertile:
        key = random.choice(fertile)
        g = S.girls[key]
        print(f"\n……触手は絶倫だ。今夜は受胎の兆しがある {g['name']} の元へ這い寄った。")
        apply_tentacle_sex(g, silent=True, allow_take_virgin=False)
    else:
        key = random.choice(candidates)
        g = S.girls[key]
        print(f"\n……触手は絶倫だ。今夜も誰かの体を求め、{g['name']}の元へ這い寄った。")
        apply_tentacle_train(g, silent=True)
    S.pause()
