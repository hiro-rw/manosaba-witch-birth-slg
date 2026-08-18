#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
大魔女受胎SLG 起動入口。
"""

import config
from game import state as S
from game import status
from game import actions_day as day
from game import actions_night as night
from game import cycle
from game import save_load
from game import endings
from game import settings_io


INTRO_TEXT = """
――牢屋敷。魔女因子を持つ者たちが集められる場所。

これまで、ストレスで魔女化させ、大魔女を呼び出そうとする試みは
ことごとく失敗してきた。

方針は変わった。
「大魔女を、生んでもらう」

ゴクチョーは、なぜか魔女因子を持つ一般の男性である{name}に、
計画の実行を命じた。

・館の触手 …… 身体を「魔女のおまんこ」へ改造（受精はしない）
・あなた自身 …… 関係を築き、エッチで人間／大魔女を孕ませる

少女たちの心と体を、優しくほどきながら、
誰かに大魔女を宿し、出産まで至らせること。

それが果たされたとき、あなたにも外への道が開かれる。
果たせなければ、封印だけが残る。
"""


def ask_name(default=None):
    default = default or settings_io.get_last_name() or "あなた"
    print(f"\nあなたの名前を入力してください（Enterで「{default}」）")
    name = input("> ").strip()
    if not name:
        name = default
    settings_io.set_last_name(name)
    return name


def show_intro_choice(player_name):
    print("\nあらすじを表示しますか？")
    print("  1. 表示する")
    print("  2. 省略する")
    while True:
        try:
            c = int(input("番号 > "))
        except ValueError:
            continue
        if c == 1:
            print("\n" + "=" * 64)
            print("  あらすじ")
            print("=" * 64)
            print(INTRO_TEXT.format(name=player_name))
            print("=" * 64)
            S.pause()
            return
        if c == 2:
            return
        print("1 または 2 を入力してください。")


def change_name():
    cur = S.state.get("player_name", "あなた")
    print(f"\n現在の名前: {cur}")
    name = ask_name(default=cur)
    S.state["player_name"] = name
    print(f"名前を「{name}」に変更しました。")
    S.pause()


def menu_system():
    while True:
        print("\n【システム】")
        print("  1. ステータス一覧")
        print("  2. ステータス詳細")
        print("  3. セーブ")
        print("  4. ロード")
        print("  5. エンディングへ")
        print("  6. 名前を変更")
        print("  7. 終了")
        print("  0. 戻る")
        try:
            cmd = int(input("番号 > "))
        except ValueError:
            continue
        if cmd == 0:
            return None
        if cmd == 1:
            status.show_status_list()
        elif cmd == 2:
            status.show_status_detail()
        elif cmd == 3:
            save_load.do_save()
        elif cmd == 4:
            save_load.do_load()
        elif cmd == 5:
            result = endings.menu_endings()
            if result == "ended":
                return "quit"
        elif cmd == 6:
            change_name()
        elif cmd == 7:
            print("\n終了します。")
            return "quit"
        else:
            print("正しい番号を入力してください。")


def menu_target_day():
    g = S.girls.get(S.state["current_target"])
    if g and S.is_in_infirmary(g):
        print("\n【医務室】可能な行動は「仲良くする」のみです。")
        print("  1. 仲良くする")
        print("  0. 戻る")
        try:
            cmd = int(input("番号 > "))
        except ValueError:
            return False, False
        if cmd == 0:
            return False, False
        if cmd == 1:
            return day.action_bond(), False
        return False, False

    print("\n【目標への行動】")
    print("  1. 仲良くする")
    print("  2. エッチする")
    print("  3. 開発（ソフト）")
    print("  4. 開発（ノーマル）")
    print("  5. 開発（ハード）")
    print("  6. 体力トレーニング")
    print("  7. 休憩")
    print("  0. 戻る")
    try:
        cmd = int(input("番号 > "))
    except ValueError:
        return False, False
    if cmd == 0:
        return False, False
    if cmd == 1:
        return day.action_bond(), False
    if cmd == 2:
        return day.action_sex(), False
    if cmd == 3:
        return day.action_train("soft"), False
    if cmd == 4:
        return day.action_train("normal"), False
    if cmd == 5:
        return day.action_train("hard"), False
    if cmd == 6:
        return day.action_stamina_train(), False
    if cmd == 7:
        return day.action_rest(), False
    print("正しい番号を入力してください。")
    return False, False


def menu_self_day():
    print("\n【自分の行動】")
    print("  1. テクニック向上（資金・時間）")
    print("  2. 瞑想をする（因子を整える）")
    print("  3. アルバイト（資金を増やす）")
    print("  0. 戻る")
    try:
        cmd = int(input("番号 > "))
    except ValueError:
        return False, False
    if cmd == 0:
        return False, False
    if cmd == 1:
        ok = day.action_technique()
        return ok, ok
    if cmd == 2:
        ok = day.action_meditate()
        return ok, ok
    if cmd == 3:
        ok = day.action_job()
        return ok, ok
    print("正しい番号を入力してください。")
    return False, False


def menu_target_night():
    print("\n【夜の行動】")
    print("  1. 触手調教（受胎度）")
    print("  2. 触手から因子を引き出す")
    print("  3. 就寝")
    print("  0. 戻る")
    try:
        cmd = int(input("番号 > "))
    except ValueError:
        return False
    if cmd == 0:
        return False
    if cmd == 1:
        return night.action_tentacle_train()
    if cmd == 2:
        return night.action_extract_factor()
    if cmd == 3:
        return night.action_sleep()
    print("正しい番号を入力してください。")
    return False


def game_loop():
    while True:
        if S.state.get("all_sealed") or S.count_usable() <= 0:
            cycle.check_bad_end()
            print("\n行動できる少女がいません。【システム】からエンディングへ／終了を選んでください。")
            result = menu_system()
            if result == "quit":
                return
            continue
        if S.state.get("day", 1) > config.DAYS_IN_YEAR:
            print("\n期限を過ぎています。【システム】→エンディングへ、で結末を確定できます。")
        status.show_status()
        phase = S.state["phase"]
        print(f"\n【{config.PHASE_NAMES[phase]}】何をしますか？")
        if phase in ("morning", "afternoon"):
            print("  1. 目標への行動")
            print("  2. 自分の行動")
            print("  3. 目標を変更する（時間消費なし）")
            print("  4. ステータス一覧（時間消費なし）")
            print("  5. システム")
            try:
                cmd = int(input("番号 > "))
            except ValueError:
                continue
            if cmd == 1:
                consumed, free_target = menu_target_day()
                if consumed:
                    cycle.advance_phase(target_was_free=free_target)
            elif cmd == 2:
                consumed, free_target = menu_self_day()
                if consumed:
                    cycle.advance_phase(target_was_free=free_target)
            elif cmd == 3:
                status.change_target()
            elif cmd == 4:
                status.show_status_list()
            elif cmd == 5:
                result = menu_system()
                if result == "quit":
                    return
            else:
                print("正しい番号を入力してください。")
        else:
            print("  1. 夜の行動")
            print("  2. 目標を変更する（時間消費なし）")
            print("  3. ステータス一覧（時間消費なし）")
            print("  4. システム")
            try:
                cmd = int(input("番号 > "))
            except ValueError:
                continue
            if cmd == 1:
                consumed = menu_target_night()
                if consumed:
                    cycle.advance_phase()
            elif cmd == 2:
                status.change_target()
            elif cmd == 3:
                status.show_status_list()
            elif cmd == 4:
                result = menu_system()
                if result == "quit":
                    return
            else:
                print("正しい番号を入力してください。")


def title_menu():
    S.bootstrap()
    while True:
        print("\n" + "=" * 64)
        print("  魔法少女ノ魔女裁判 - 大魔女受胎SLG")
        print("=" * 64)
        print("  1. 最初から")
        print("  2. ロード")
        print("  3. 終了")
        try:
            cmd = int(input("番号 > "))
        except ValueError:
            continue
        if cmd == 1:
            name = ask_name()
            S.init_state(player_name=name)
            show_intro_choice(name)
            print(f"\nようこそ、{name}。")
            print("クリア条件はメニュー「エンディングへ」から確定します。")
            S.pause()
            game_loop()
        elif cmd == 2:
            # ロード用に空状態でも girls が必要な場合あり
            if not S.girls:
                S.load_girls()
            if not S.state:
                S.init_state(player_name=settings_io.get_last_name())
            save_load.do_load()
            if S.state and S.girls:
                game_loop()
        elif cmd == 3:
            print("終了します。")
            return
        else:
            print("正しい番号を入力してください。")


def main():
    title_menu()


if __name__ == "__main__":
    main()
