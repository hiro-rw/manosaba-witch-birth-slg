# -*- coding: utf-8 -*-
"""
橘シェリー（key: シェリー）の定義ファイル。
仕様：1人1ファイル。INITIAL・行動メソッド・個別イベント。
共通文は game.common_lines を任意で呼ぶ（必須ではない）。
"""

import random

from game import common_lines

KEY = 'シェリー'
NAME = '橘シェリー'

# # flags[0]=告白済み  [1]=予備
INITIAL = {
    'key': 'シェリー',
    'name': '橘シェリー',
    'stamina': 82,
    'max_stamina': 105,
    'stress': 15,
    'conception': 0,
    'training_level': 0,
    'pregnancy_days': 0,
    'witch_progress': 0,
    'cycle_day': 18,
    'tags': [
        'virgin',
    ],
    'lines': {
        'breast_low': [
            '……ん、くすぐったい……です……',
            'ふぁ……なんか、変な感じ……',
            '……興味深い、です……',
        ],
        'breast_mid': [
            '……んっ、熱い……です……',
            'ふぁ……体が、反応して……',
            '……もっと、触られても……いい、かも……',
        ],
        'breast_high': [
            'んあっ……そこ、いい……です……',
            'ふぁっ……もっと、お願いします……',
            '……腰が、止まらない……っ',
        ],
        'pussy_low': [
            '……ん、そこは……',
            'ふぁ……変、です……',
            '……興味深い、のに……っ',
        ],
        'pussy_mid': [
            'んっ……奥、熱い……です……',
            'ふぁっ……子宮が……',
            '……変な感じ、なのに……嫌じゃない……っ',
        ],
        'pussy_high': [
            'んあっ……！\u3000奥、いい……っ',
            'ふぁあっ……子宮、くすぐったい……もっと……',
            '……注いで、ください……っ',
        ],
        'ass_low': [
            '……ん、お尻は……',
            'ふぁ……くすぐったいです……',
            '……そこも、興味深い……',
        ],
        'ass_mid': [
            'んっ……そこも、熱い……',
            'ふぁ……変な感じ……です……',
            '……腰が……',
        ],
        'ass_high': [
            'んあっ……お尻、いい……です……っ',
            'ふぁっ……もっと……',
            '……探偵として、放置できません……っ',
        ],
        'tentacle_touch': [
            '……ん、何か……？',
            'ふぁ……くすぐったいです……',
        ],
        'tentacle_deep': [
            '……あっ……奥、熱い……',
            'んっ……これ、興味深い……ですね……っ',
        ],
        'tentacle_climax': [
            'んあっ……！\u3000変、です……っ',
            'ふぁあっ……腰が、勝手に……！',
        ],
        'tentacle_after': [
            '……ふぅ。なんだか、体が軽い……？',
            '面白い感触、でした……',
        ],
        'sleep': [
            'ふふっ……面白い夢、見られそうですね……',
            '……ん、何か……？',
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
        "「事件だ……！　触手さん、動機は受胎？　興味深い！」",
        "シェリーの目が輝くが、脚はすでに絡まれている。",
        "「んっ……調査中に、感じるのは反則です……」",
        "「でも、データは取ります。感度、上昇中……あっ」",
    ]

def on_tentacle_sex(g):
    out = [
        "「待って、挿入は証拠隠滅では……ひゃあっ」",
        "触手が探偵の秘部を貫く準備をする。",
    ]
    if "virgin" in g.get("tags", []):
        out.append("「初めての現場が、ここ……痛い、ですけど……記録しますっ」")
    out += [
        "「奥まで……真相に、近い……んあっ」",
        "「イく……名探偵が、触手にイかされる事件……！」",
        "「……おなかに、決定的証拠が。生きて、解明します」",
    ]
    return out

def on_ending_elope(g):
    return "\n".join([
        "「脱獄事件の共犯、やります！　あなたと」",
        "「外の謎も、一緒に解決しましょう」",
    ])

def on_ending_shinju(g):
    return "\n".join([
        "「魔女になるくらいなら……最後の事件は、心中です」",
        "「好き、です。これで、幕を閉じます」",
    ])
