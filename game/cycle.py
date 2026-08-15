# -*- coding: utf-8 -*-
"""
cycle.py
フェイズ進行・日付進行・フリー行動・妊娠発覚・出産・魔女化。
"""

import random
import sys

import config
from game import state as S
from game.actions_night import night_auto_tentacle


def day_auto_actions(include_target=False):
    """未選択（または目標フリー時）の少女のフリー行動。"""
    print("\n【少女たちの様子】")
    target = S.state["current_target"]
    any_shown = False
    for key, g in S.girls.items():
        if (not include_target) and key == target:
            continue
        if S.is_sealed(g):
            continue
        any_shown = True
        r = random.random()
        name = g["name"]
        if S.is_in_infirmary(g):
            print(f"・{name}は医務室で静かに過ごしている。")
            g["stress"] = max(0, g["stress"] - 2)
        elif S.is_pregnant_known(g) and r < 0.40:
            print(f"・{name}は妊娠した体を労わりながら過ごしている。")
            g["stress"] = max(0, g["stress"] - 2)
            g["stamina"] = min(g.get("max_stamina", 100), g["stamina"] + 5)
        elif S.is_period(g):
            print(f"・{name}は生理のため、部屋で控えめにしている。")
            g["stress"] = min(100, g["stress"] + random.randint(0, 2))
        elif r < 0.18:
            # トレーニング
            cost = random.randint(4, 8)
            gain = 1 if random.random() < 0.7 else 0
            g["stamina"] = max(0, g["stamina"] - cost)
            if gain:
                g["max_stamina"] = min(150, g.get("max_stamina", 100) + gain)
            print(f"・{name}は自分で軽いトレーニングをした。（体力 -{cost}" +
                  (f" 最大体力 +{gain}" if gain else "") + "）")
        elif r < 0.38:
            # 休憩
            rec = random.randint(8, 14)
            sd = random.randint(2, 5)
            g["stamina"] = min(g.get("max_stamina", 100), g["stamina"] + rec)
            g["stress"] = max(0, g["stress"] - sd)
            print(f"・{name}は自分で休みを取った。（体力 +{rec} ストレス -{sd}）")
        elif r < 0.52:
            # ストレス軽減
            sd = random.randint(3, 7)
            g["stress"] = max(0, g["stress"] - sd)
            print(f"・{name}はぼんやりして気を紛らわせた。（ストレス -{sd}）")
        elif r < 0.68 and not S.is_period(g):
            # 自慰
            gain = random.randint(1, 2)
            g["training_level"] = min(100, g.get("training_level", 0) + gain)
            g["stress"] = max(0, g["stress"] - random.randint(0, 2))
            print(f"・{name}は部屋で、自分の体を慰めていた……（開発Lv +{gain}）")
        elif r < 0.82:
            print(f"・{name}は部屋で過ごしている。")
            g["stress"] = min(100, g["stress"] + random.randint(-2, 3))
            g["stress"] = max(0, g["stress"])
        else:
            print(f"・{name}は少し不安そうだ……。")
            g["stress"] = min(100, g["stress"] + random.randint(3, 7))
    if not any_shown:
        print("・（特に変わった様子はない）")
    S.pause()


def trigger_witchify(g):
    if g.get("sealed"):
        return
    from game.characters.registry import get_module
    mod = get_module(g["key"])
    print(f"\n{'='*60}")
    print(f"  魔女化  ―  {g['name']}")
    print(f"{'='*60}")
    if mod and hasattr(mod, "on_witchify"):
        result = mod.on_witchify(g)
        if isinstance(result, str):
            print(result)
        elif result:
            for line in result:
                print(line)
    else:
        print(f"{g['name']}の瞳が、魔女の色に濁る。")
        print("まもなく彼女は処刑され、封印された。")
    g["sealed"] = True
    g["witch_progress"] = 100

    if g.get("key") == "エマ":
        print("\n……エマの崩壊が、館のすべてを飲み込む。")
        print("他の魔女候補たちも、次々と光を失っていく。")
        for other in S.girls.values():
            other["sealed"] = True
            other["witch_progress"] = 100
        S.state["emma_witchified"] = True
        S.state["all_sealed"] = True
        print("【全員封印】行動できる少女がいなくなった。")
    S.pause()
    check_bad_end()


def check_bad_end():
    if S.count_usable() <= 0:
        S.state["all_sealed"] = True
        print("\n※ 行動できる少女がいません。システムメニューの「エンディングへ」から結末を確定できます。")
        return True
    return False


def trigger_pregnancy_notice(g):
    if g.get("pregnancy_noticed"):
        return
    g["pregnancy_noticed"] = True
    S.add_tag(g, "pregnant")
    g["pregnant_internal"] = True
    from game.characters.registry import get_module
    mod = get_module(g["key"])
    print(f"\n{'='*60}")
    print(f"  妊娠の発覚  ―  {g['name']}")
    print(f"{'='*60}")
    if mod and hasattr(mod, "on_pregnancy_notice"):
        result = mod.on_pregnancy_notice(g)
        if isinstance(result, str):
            print(result)
        elif result:
            for line in result:
                print(line)
    else:
        aff = g.get("affection", 0)
        bt = g.get("baby_type") or "？"
        if aff >= config.AFFECTION_LOVE:
            print(f"{g['name']}は頬を染め、そっとお腹に手を当てた。")
            print(f"「……来ないの。生理が。たぶん、赤ちゃん……{bt}、だと思う。」")
        else:
            print(f"{g['name']}の顔色が変わり、言葉少なに報告する。")
            print(f"「……生理が、来ません。検査では、妊娠、だそうです。」")
    print(f"（{g['name']}の妊娠が発覚した／種別: {g.get('baby_type')}）")
    S.pause()


def trigger_birth(g):
    from game.characters.registry import get_module
    mod = get_module(g["key"])
    bt = g.get("baby_type") or "？"
    print(f"\n{'='*60}")
    print(f"  出産  ―  {g['name']}")
    print(f"{'='*60}")
    if mod and hasattr(mod, "on_birth"):
        result = mod.on_birth(g)
        if isinstance(result, str):
            print(result)
        elif result:
            for line in result:
                print(line)
    else:
        print(f"{g['name']}は医務室で、新しい命を産み落とした（{bt}）。")
    from game import endings
    endings.record_birth(g, bt if bt in ("大魔女", "人間") else "人間")
    if bt == "大魔女":
        print("\n【達成】大魔女の出産に成功した（エンディングはメニューから確定できます）。")
    if S.has_tag(g, "virgin"):
        S.remove_tag(g, "virgin")
        print(f"（{g['name']}の処女膜は出産により失われた）")
    S.remove_tag(g, "pregnant")
    g["pregnant_internal"] = False
    g["pregnancy_noticed"] = False
    g["pregnancy_days"] = 0
    g["conception"] = max(0, g.get("conception", 0) // 2)
    g["baby_type"] = None
    g["cycle_day"] = 1
    g["cycle_len"] = config.CYCLE_LEN + random.randint(-2, 2)
    g["period_days"] = random.randint(4, 6)
    S.pause()


def advance_phase(target_was_free=False):
    st = S.state
    idx = config.PHASES.index(st["phase"])
    if idx < 2:
        st["phase"] = config.PHASES[idx + 1]
        if target_was_free:
            day_auto_actions(include_target=True)
        return

    night_auto_tentacle()
    day_auto_actions(include_target=False)

    st["day"] += 1
    st["phase"] = "morning"
    st["tentacle_action_tonight"] = False

    for g in S.girls.values():
        if S.is_sealed(g):
            continue

        if g.get("pregnant_internal") or S.has_tag(g, "pregnant"):
            g["pregnancy_days"] = g.get("pregnancy_days", 0) + 1
            if not g.get("pregnancy_noticed"):
                g["cycle_day"] = g.get("cycle_day", 1) + 1
                clen = max(20, g.get("cycle_len", config.CYCLE_LEN))
                if g["cycle_day"] > clen:
                    g["cycle_day"] = 1
                    trigger_pregnancy_notice(g)
            else:
                if g["pregnancy_days"] >= 40 and not S.has_tag(g, "lactating") and random.random() < 0.12:
                    S.add_tag(g, "lactating")
                    print(f"\n※ {g['name']}に母乳の兆候。")
                if g["pregnancy_days"] >= config.PREGNANCY_DAYS_TO_BIRTH:
                    trigger_birth(g)
        else:
            g["cycle_day"] = g.get("cycle_day", 1) + 1
            clen = max(20, g.get("cycle_len", config.CYCLE_LEN))
            if g["cycle_day"] > clen:
                g["cycle_day"] = 1
                g["cycle_len"] = config.CYCLE_LEN + random.randint(-2, 2)
                g["period_days"] = random.randint(4, 6)

        if g["stress"] >= 85 and random.random() < 0.3:
            g["witch_progress"] = min(100, g.get("witch_progress", 0) + random.randint(2, 8))
            if g["witch_progress"] >= 100:
                trigger_witchify(g)

        rec = 5 if S.is_pregnant_known(g) else 8
        g["stamina"] = min(g.get("max_stamina", 100), g["stamina"] + rec)

    check_bad_end()
    cur = st.get("current_target")
    if cur and S.is_sealed(S.girls.get(cur, {})):
        for k, gg in S.girls.items():
            if S.is_usable(gg):
                st["current_target"] = k
                print(f"\n（目標を {gg['name']} に変更しました）")
                break

    print(f"\n--- {st['day']}日目 午前が始まりました ---")
    if st["day"] > config.DAYS_IN_YEAR:
        print("\n※ 期限を過ぎました。システムメニューの「エンディングへ」から結末を確定できます。")
