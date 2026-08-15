# -*- coding: utf-8 -*-
"""
桜羽エマ（key: エマ）の定義ファイル。

仕様：
- 1人1ファイル
- INITIAL・行動メソッド・個別イベントを定義
- 受胎そのものでは妊娠を発覚させない
- 妊娠発覚は on_pregnancy_notice() から
- 妊娠期間はゲームエンジン側で100日として管理
- 妊娠中の細かな心情・所作はこのファイルで表現
"""

import random

from game import common_lines

KEY = "エマ"
NAME = "桜羽エマ"


INITIAL = {
    "key": "エマ",
    "name": "桜羽エマ",
    "stamina": 78,
    "max_stamina": 95,
    "stress": 12,
    "conception": 0,
    "training_level": 0,
    "pregnancy_days": 0,
    "witch_progress": 0,
    "cycle_day": 3,
    "tags": [
        "virgin",
    ],
    "lines": {
        "breast_low": [
            "……ん、誰……？",
            "あっ……くすぐったいよ……",
            "……変な感じ……",
        ],
        "breast_mid": [
            "……んっ、熱いよ……",
            "あっ……ボクの胸……",
            "……嫌じゃない、けど……",
        ],
        "breast_high": [
            "んあっ……そこ、いい……っ",
            "はぁっ……もっと、触って……",
            "……そばに、いて……っ",
        ],
        "pussy_low": [
            "……んぅ、そこは……",
            "あっ……変、だよ……",
            "……やめて、って言っても……",
        ],
        "pussy_mid": [
            "んっ……熱い……ボク……",
            "はぁっ……奥が、変……",
            "……嫌じゃない、かも……っ",
        ],
        "pussy_high": [
            "んあっ……奥、いい……っ",
            "はぁあっ……もっと……ボクの中……",
            "……注いで……っ",
        ],
        "ass_low": [
            "……ん、お尻は……",
            "あっ……くすぐったい……",
            "……変なところ……",
        ],
        "ass_mid": [
            "んっ……そこも、熱い……",
            "……ふぁ、変な感じ……",
            "……腰が……",
        ],
        "ass_high": [
            "んあっ……お尻、いい……っ",
            "はぁっ……もっと……",
            "……だめなのに……っ",
        ],
        "tentacle_touch": [
            "……ん、誰……？",
            "あっ……くすぐったいよ……",
        ],
        "tentacle_deep": [
            "んっ……奥、熱い……ボク……",
            "はぁっ……誰か、触ってる……？",
        ],
        "tentacle_climax": [
            "んあっ……！　ボク、変になる……っ",
            "はぁっ……誰か、いて……！",
        ],
        "tentacle_after": [
            "……ん。なんだか、あったかい……",
            "……そばに、いてくれたの……？",
        ],
        "sleep": [
            "……誰か、そばにいて……",
            "ん……ボク、一人は……嫌……",
        ],
    },
    "affection": 0,
    "baby_type": None,
    "flags": [
        0,  # 告白済み
        0,
        0,
        0,
        0,
    ],
}


def _tier_from_g(g):
    lv = g.get("training_level", 0)
    if lv <= 20:
        return "low"
    if lv <= 50:
        return "mid"
    return "high"


def _lines(g, base, tier=None):
    """INITIAL['lines'] から tier 付きキーで取得（フォールバック付き）。"""
    tier = tier or _tier_from_g(g)
    bag = g.get("lines") or INITIAL.get("lines") or {}

    for key in (f"{base}_{tier}", f"{base}_low", base):
        if key in bag and bag[key]:
            return bag[key]

    return ["……"]


def _affection_tier(g):
    """会話用の好感度段階。"""
    aff = g.get("affection", 0)

    if aff < 30:
        return "low"
    if aff < 71:
        return "mid"
    if aff < 100:
        return "high"
    return "love"


def on_breast(g, tier=None):
    """おっぱい調教。共通地の文＋個人の反応。"""
    out = []
    out.extend(common_lines.on_breast(g, tier))
    out.append("「" + random.choice(_lines(g, "breast", tier)) + "」")
    return out


def on_pussy(g, tier=None):
    """おまんこ調教。"""
    out = []
    out.extend(common_lines.on_pussy(g, tier))
    out.append("「" + random.choice(_lines(g, "pussy", tier)) + "」")
    return out


def on_ass(g, tier=None):
    """おしり調教。"""
    out = []
    out.extend(common_lines.on_ass(g, tier))
    out.append("「" + random.choice(_lines(g, "ass", tier)) + "」")
    return out


def on_bond(g):
    """
    親交を深める。

    好感度に応じて会話内容を変化させる。
    flags[0] == 0 かつ好感度100以上で告白イベント。
    """
    out = []
    out.extend(common_lines.on_bond(g))

    flags = g.setdefault("flags", [0, 0, 0, 0, 0])
    while len(flags) < 5:
        flags.append(0)

    aff = g.get("affection", 0)

    if aff >= 100 and flags[0] == 0:
        flags[0] = 1
        out.extend([
            "エマは少しだけ迷うように視線を伏せ、それからまっすぐこちらを見る。",
            "「……ボク、あなたが好き。」",
            "「ここに来てから、ずっと怖かったけど……あなたがいると、少しだけ安心できる。」",
            "「だから……そばに、いて。」",
        ])
        return out

    tier = _affection_tier(g)

    if tier == "low":
        out.extend([
            "エマは少し離れたところに座り、こちらの様子をうかがっている。",
            "「……まだ、距離がある、ような気がする。」",
            "「でも……こうして話してくれるのは、嫌じゃないよ。」",
        ])

    elif tier == "mid":
        out.extend([
            "エマは小さく笑いながら、ぽつぽつと言葉を交わす。",
            "「……少し、話せてよかった。」",
            "「ここって静かだから……誰かと話せるだけでも、ちょっと違うね。」",
        ])

    elif tier == "high":
        out.extend([
            "エマは自然な様子で隣に座る。",
            "「……あなたといると、落ち着く。」",
            "「今日は何をしてたの？　ちゃんと休んでる？」",
            "「……ボクのことばっかり気にしなくてもいいんだよ。」",
        ])

    else:
        out.extend([
            "エマは安心したように微笑み、こちらの顔をのぞき込む。",
            "「……今日も来てくれた。」",
            "「ボク、あなたが来るの……ちょっと楽しみにしてる。」",
            "「……ふふ。変だよね。こんな場所なのに。」",
        ])

    return out


def on_pregnancy_bond(g):
    """
    妊娠発覚後の「仲良くする」専用会話。

    妊娠日数そのものをメイン画面に表示する設計とは分離し、
    日数帯だけを内部的な文章分岐に利用する。
    """
    out = []

    days = g.get("pregnancy_days", 0)
    aff = g.get("affection", 0)

    if days < 20:
        out.extend([
            "エマは少し落ち着かない様子で、それでもこちらの隣に座る。",
            "「まだ……実感はあんまりないんだ。」",
            "「でも、ちゃんとここにいるんだよね。」",
        ])

    elif days < 50:
        out.extend([
            "エマは自分のお腹にそっと手を添えてから、こちらを見る。",
            "「最近ね、前より少しだけ身体のことが気になるようになったの。」",
            "「無理しないほうがいいって言われたから……ちゃんと気をつけるね。」",
        ])

    elif days < 80:
        out.extend([
            "エマはゆっくり腰を下ろし、少しだけ息をつく。",
            "「前より疲れやすくなったかも。」",
            "「でも……あなたが来てくれると、なんだか安心する。」",
        ])

    else:
        out.extend([
            "エマはお腹をいたわるように両手を添え、ゆっくり息を吐く。",
            "「もうすぐなんだよね……。」",
            "「怖くないって言ったら嘘になるけど……あなたがそばにいてくれるなら、大丈夫だと思う。」",
        ])

    if aff >= 71:
        out.append("「……ねえ。あなたも、ちゃんと休んでね。」")

    return out


def on_player_tired(g):
    """
    プレイヤー側の疲労を見たときの個別反応。
    エンジン側から任意に呼び出す。
    """
    aff = g.get("affection", 0)

    if aff < 30:
        return [
            "エマは少し心配そうにこちらを見る。",
            "「……大丈夫？　無理してない？」",
        ]

    if aff < 71:
        return [
            "「今日はちょっと疲れてるみたい。」",
            "「ちゃんと休んだほうがいいよ。」",
        ]

    return [
        "エマは心配そうにこちらの顔を見る。",
        "「……先輩、頑張りすぎ。」",
        "「ボクのことを気にしてくれるのは嬉しいけど、先輩まで倒れたら嫌だから。」",
        "「今日は少し休もう？」",
    ]


def on_sex(g, affection):
    """
    交尾のテキスト一式。
    処女なら喪失演出を含める（tags の着脱はエンジン側でも行う想定）。
    """
    out = []
    out.extend(common_lines.on_sex_foreplay(g))

    tags = g.get("tags") or []

    if "virgin" in tags:
        if affection >= 71:
            out.append("（" + NAME + "は、甘い空気の中で初めてを委ねた）")
            out.append("「……あなたなら、いい。」")
        else:
            out.append("（" + NAME + "の初めての壁が、静かにほどける）")
            out.append("「……んっ……」")

    out.extend(common_lines.on_sex_enter(g))
    out.append("「" + random.choice(_lines(g, "pussy")) + "」")
    out.extend(common_lines.on_sex_climax(g))

    if affection >= 71:
        out.append("「……好き。もっと、奥まで……」")
    else:
        out.append("「……んっ、熱い……」")

    return out


def on_defloration(g, affection):
    """後方互換。on_sex 内の処理を優先。"""
    if affection >= 71:
        return [
            "（" + NAME + "は、甘い空気の中で初めてを委ねた）",
            "「……あなたなら、いい。」",
        ]

    return [
        "（" + NAME + "の初めての壁が、静かにほどける）",
        "「……んっ……」",
    ]


def on_human_conceive(g):
    """
    受胎成立時には何も表示しない。

    仕様上、本人への発覚は on_pregnancy_notice() まで行わない。
    """
    return []


def on_witch_conceive(g):
    """
    大魔女受胎成立時にも何も表示しない。

    受胎成立と発覚を完全に分離する。
    """
    return []


def on_train(g, intensity="normal"):
    """強度調教。性感帯はテキストで表現。"""
    out = []
    out.extend(common_lines.on_train(g, intensity))

    part = random.choice(["breast", "pussy", "ass"])
    out.append("「" + random.choice(_lines(g, part)) + "」")

    if intensity == "hard":
        out.append("（強い刺激に、体が小さく震える）")

    return out


def on_witchify(g):
    """エマが魔女化したとき。エンジン側で全員封印される。"""
    return [
        "桜羽エマの体が、光を失うように歪む。",
        "「……みんな、ごめん……ボクが、壊しちゃう……」",
        "忌む力が館全体に走り、他の魔女候補たちの息が止まる。",
        "エマは処刑され、封印された。そして、誰も残らなかった。",
    ]


def on_pregnancy_notice(g):
    """
    生理が来ないことによる妊娠の発覚。
    ここに到達するまで妊娠状態は本人に通知しない。
    """
    aff = g.get("affection", 0)
    bt = g.get("baby_type") or "？"

    if aff >= 71:
        return [
            NAME + "はしばらく黙ったまま、自分のお腹にそっと手を当てる。",
            "「……来ないの。生理が。」",
            "エマは不安そうにこちらを見る。",
            "「たぶん……赤ちゃん。種別は" + str(bt) + "、だと思う。」",
        ]

    if aff >= 30:
        return [
            NAME + "は検査結果を何度も確認してから、ゆっくり口を開く。",
            "「……生理が、来ません。」",
            "「検査では、妊娠だそうです。」",
            "エマはしばらく黙り込んでいる。",
        ]

    return [
        NAME + "の顔色が変わり、言葉少なに報告する。",
        "「……生理が、来ません。」",
        "「検査では、妊娠だそうです。」",
    ]


def on_pregnancy_day(g):
    """
    妊娠経過中の個別イベント。
    100日進行そのものはエンジン側で管理する。

    戻り値:
        その日の経過イベントがなければ []。
    """
    days = g.get("pregnancy_days", 0)
    aff = g.get("affection", 0)

    # 特定日だけイベントを出す。
    events = {
        1: [
            "エマは何度も自分のお腹を見下ろしている。",
            "「……本当に、いるのかな。」",
        ],
        20: [
            "エマは少し不思議そうに自分のお腹へ手を添える。",
            "「まだ何も分からないけど……身体って、ちゃんと変わっていくんだね。」",
        ],
        40: [
            "エマは以前よりゆっくり動くようになった。",
            "「最近、ちょっと疲れやすいかも。」",
            "「でも、休めば大丈夫だから。」",
        ],
        60: [
            "エマは椅子に座ると、ほっとしたように息を吐く。",
            "「ここまで来たんだね……。」",
            "「なんだか、最初よりずっと実感がある。」",
        ],
        80: [
            "エマはお腹をいたわるように手を添える。",
            "「もう少し……なんだよね。」",
            "「楽しみって気持ちと、ちょっと怖いって気持ちが半分ずつ。」",
        ],
        90: [
            "エマは立ち上がる前に一度深呼吸する。",
            "「身体が重くなってきたなぁ……。」",
            "「でも、あと少しだから。」",
        ],
        99: [
            "エマは医務室へ向かう準備をしながら、こちらを振り返る。",
            "「明日……かな。」",
            "「最後まで、そばにいてくれる？」",
        ],
    }

    out = list(events.get(days, []))

    if out and aff >= 71:
        out.append("「……ありがとう。あなたが一緒にいてくれて、本当によかった。」")

    return out


def on_birth(g):
    """
    出産イベント。
    出産そのものの進行はエンジン側で管理し、ここでは個別演出のみ。
    """
    bt = g.get("baby_type") or "？"
    aff = g.get("affection", 0)

    out = [
        NAME + "は医務室で、新しい命を産み落とした（" + str(bt) + "）。",
    ]

    if aff >= 71:
        out.extend([
            "しばらく目を閉じていたエマが、ゆっくりこちらを見る。",
            "「……終わった、の？」",
            "「……あなた、ちゃんといる？」",
            "エマは安心したように小さく笑う。",
            "「……よかった。」",
        ])
    elif aff >= 30:
        out.extend([
            "エマは疲れ切った様子で、それでも小さく息を吐く。",
            "「……終わったんだ。」",
        ])
    else:
        out.extend([
            "エマはしばらく黙ったまま、静かに呼吸を整えている。",
            "「……終わった、の？」",
        ])

    return out


def on_tentacle_train(g):
    return [
        "触手がエマの足首に絡む。彼女は『ボク』と小さく呟いて身を固くする。",
        "「やだ……触手、やめて。ボク、まだ……っ」",
        "「んっ……変な感じ。嫌い、なのに……熱い」",
        "「一人にしないで……。触られても、あなたの声が欲しい」",
    ]

def on_tentacle_sex(g):
    out = [
        "触手が脚を開き、エマの秘部に先端を押し当てる。",
        "「入ってこないで……ボクの中、触手なんか……っ」",
    ]
    if "virgin" in g.get("tags", []):
        out.append("「初めてが、こんなの……痛いよ……っ」")
    out += [
        "「奥まで……くる。子宮、さわらないで……っ」",
        "「イく……触手に、イかされるの、嫌なのに……！」",
        "「……おなか、変。でも、生きてる。あなたも、いて」",
    ]
    return out

def on_ending_elope(g):
    return "\n".join([
        "「……逃げよう。ボクと、一緒に」",
        "「外でも、一人にしないで。約束だよ」",
    ])

def on_ending_shinju(g):
    return "\n".join([
        "「魔女になるくらいなら……あなたを、ひとりにしない」",
        "「ボク、あなたが好き。だから……これで、終わり」",
    ])
