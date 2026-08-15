# -*- coding: utf-8 -*-
"""
紫藤アリサ（key: アリサ）の定義ファイル。
仕様：1人1ファイル。INITIAL・行動メソッド・個別イベント。
共通文は game.common_lines を任意で呼ぶ（必須ではない）。
"""

import random

from game import common_lines

KEY = 'アリサ'
NAME = '紫藤アリサ'

# # flags[0]=心を開いた/告白相当  [1]=予備
INITIAL = {
    'key': 'アリサ',
    'name': '紫藤アリサ',
    'stamina': 88,
    'max_stamina': 110,
    'stress': 25,
    'conception': 0,
    'training_level': 0,
    'pregnancy_days': 0,
    'witch_progress': 0,
    'cycle_day': 25,
    'tags': [
        'virgin',
    ],
    'lines': {
        'breast_low': [
            '……触んな',
            'ん……うるせえ……',
            '……ウチに近づくなよ',
        ],
        'breast_mid': [
            '……んっ、クソ……',
            '……体が、勝手に……',
            '……やめて、って言ってんだろ……',
        ],
        'breast_high': [
            'んっ……そこ、触んな……っ',
            '……クソ、感じて……',
            '……もう、どうでもいい……っ',
        ],
        'pussy_low': [
            '……そこは、触んな',
            'ん……やめろ……',
            '……殴るぞ',
        ],
        'pussy_mid': [
            'んっ……奥が、熱い……クソ……',
            '……体が、受け入れて……',
            '……やめて、なのに……っ',
        ],
        'pussy_high': [
            'んあっ……奥、深い……っ',
            '……クソ、いい……なのに……',
            '……満たして、くれよ……っ',
        ],
        'ass_low': [
            '……お尻は、だめだ',
            'ん……くすぐった……',
            '……触んなって',
        ],
        'ass_mid': [
            'んっ……そこも……クソ……',
            '……体が、震える……',
            '……やめて……っ',
        ],
        'ass_high': [
            'んっ……お尻まで……っ',
            '……もう、抵抗、できねえ……',
            '……好きに、しろよ……っ',
        ],
        'tentacle_touch': [
            '……何だ、これ',
            'ん……触んな……',
        ],
        'tentacle_deep': [
            'んっ……奥まで……入って……クソ……',
            '……やめろ、なのに……っ',
        ],
        'tentacle_climax': [
            'んあっ……！\u3000体が……っ',
            '……クソ、イキそう……！',
        ],
        'tentacle_after': [
            '……はあ……最悪だ',
            '……体が、熱い……クソ……',
        ],
        'sleep': [
            '……ウチは、一人でいい……',
            'ん……近づくな……',
        ],
    },
    'affection': 0,
    'baby_type': None,
    'flags': [
        0,
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
    for k in (f"{base}_{tier}", f"{base}_low", base):
        if k in bag and bag[k]:
            return bag[k]
    return ["……"]


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
    flags[0]==0 かつ好感度が高いと告白イベント（一度きり）。
    """
    out = []
    out.extend(common_lines.on_bond(g))
    flags = g.setdefault("flags", [0, 0, 0, 0, 0])
    aff = g.get("affection", 0)

    # 告白（好感度100以上・未告白）
    if aff >= 100 and flags[0] == 0:
        flags[0] = 1
        if KEY == "アリサ":
            out.append("「……チッ、好きとか、そういうの……認めてやるよ」")
        elif KEY == "エマ":
            out.append("「……ボク、あなたが好き。そばに、いて」")
        elif KEY == "ヒロ":
            out.append("「……正しいかどうかは分からない。でも、あなたが必要だ」")
        elif KEY == "シェリー":
            out.append("「ふふっ……探偵としてではなく、一人の女として、好きです」")
        elif KEY == "マーゴ":
            out.append("「計算外ね……あなたのこと、本気で欲しがっているみたい」")
        elif KEY == "アンアン":
            out.append("「……わがはいも、あなたが……好き、です」")
        else:
            out.append("「……好きです」")
        return out

    if aff < 30:
        out.append("「……まだ、距離がある、ような気がする。」")
    elif aff < 71:
        out.append("「……少し、話せてよかった。」")
    else:
        extra = None
        if KEY == "アリサ":
            extra = "……チッ、まあ、話くらいなら……"
        elif KEY == "エマ":
            extra = "……ボク、ここにいていいの……？"
        if extra:
            out.append(extra)
        else:
            out.append("「……あなたといると、落ち着く。」")
    return out


def on_sex(g, affection):
    """
    交尾のテキスト一式。
    処女なら喪失演出を含める（tags の着脱はエンジン側でも行う想定）。
    戻り値: 表示行のリスト
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
    return ["★ " + NAME + "は、あなたの子を受胎した（人間）。"]


def on_witch_conceive(g):
    return ["★★ " + NAME + "は、大魔女を受胎した。"]


def on_train(g, intensity="normal"):
    """強度調教。性感帯はテキストで表現。"""
    out = []
    out.extend(common_lines.on_train(g, intensity))
    # 部位反応は lines からランダム
    part = random.choice(["breast", "pussy", "ass"])
    out.append("「" + random.choice(_lines(g, part)) + "」")
    if intensity == "hard":
        out.append("（強い刺激に、体が小さく震える）")
    return out


def on_witchify(g):
    """魔女化→処刑→封印のテキスト。"""
    return [
        NAME + "の瞳が、魔女の色に濁る。",
        "抵抗する暇もなく、彼女は捕らえられ、封印された。",
        "「……こんな、終わり方……」",
    ]


def on_pregnancy_notice(g):
    """生理が来ないことによる妊娠の報告。"""
    aff = g.get("affection", 0)
    bt = g.get("baby_type") or "？"
    if aff >= 71:
        return [
            NAME + "は頬を染め、そっとお腹に手を当てた。",
            "「……来ないの。生理が。たぶん、……赤ちゃん。種別は" + str(bt) + "、だと思う。」",
        ]
    return [
        NAME + "の顔色が変わり、言葉少なに報告する。",
        "「……生理が、来ません。検査では、妊娠だそうです。」",
    ]


def on_birth(g):
    bt = g.get("baby_type") or "？"
    return [
        NAME + "は医務室で、新しい命を産み落とした（" + str(bt) + "）。",
        "「……終わった、の？」",
    ]


def on_human_conceive(g):
    return ["（" + NAME + "の奥で、何かが着床した……まだ本人も気づいていない）"]


def on_witch_conceive(g):
    return ["（" + NAME + "の子宮に、大魔女の兆しが宿った……まだ分からない）"]


def on_tentacle_train(g):
    return [
        "「はあ？　触手？　ふざけんな、ウチに触るな！」",
        "アリサが暴れるほど、触手は緩く、しかし確実に絡む。",
        "「んっ……感じねえ、感じねえからな……嘘だ、熱い……っ」",
        "「自罰とか、関係ねえ……ただ、気持ち悪いっ」",
    ]

def on_tentacle_sex(g):
    out = [
        "「入れるな……！　ウチを孕ませるつもりか、クソが……！」",
    ]
    if "virgin" in g.get("tags", []):
        out.append("「初めてが触手だと……？　最悪だ……痛えっ……！」")
    out += [
        "「奥まで……くるな……子宮、いじるな……っ」",
        "「イク……触手なんかに、イかされ……て……っ！」",
        "「……精、入ってる。生きてやる。あんたも見ろ」",
    ]
    return out

def on_ending_elope(g):
    return "\n".join([
        "「逃げるぞ。ウチとだ。文句あっか」",
        "「外でも、一人で死ぬな。……好きだ、バカ」",
    ])

def on_ending_shinju(g):
    return "\n".join([
        "「魔女になるくらいなら……先に、あんたを抱いて終わる」",
        "「自罰じゃねえ。選択だ。……好きだ」",
    ])
