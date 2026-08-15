# -*- coding: utf-8 -*-
"""
蓮見レイア（key: レイア）
役者・責任感・護る側。一人称「私」。紳士的で少し硬い口調。
"""
from game import common_lines

KEY = "レイア"
NAME = "蓮見レイア"

INITIAL = {
    "key": "レイア", "name": "蓮見レイア",
    "stamina": 78, "max_stamina": 100, "stress": 9,
    "conception": 0, "training_level": 0, "pregnancy_days": 0,
    "witch_progress": 0, "cycle_day": 1, "tags": ["virgin"],
    "lines": {}, "flags": [0, 0, 0, 0, 0],
}

def _aff(g): return g.get("affection", 0)
def _flags(g):
    f = g.setdefault("flags", [0,0,0,0,0])
    while len(f)<5: f.append(0)
    return f

def on_train(g, intensity="normal"):
    out = ["レイアは舞台に立つときのように背筋を伸ばし、それでも息が浅い。"]
    if intensity == "soft":
        out += [
            "「……構わない。私が受ける」",
            "「ん……感じてはいる。だが、崩れるわけにはいかない」",
            "「君が望むなら、台詞どおりに応えよう」",
        ]
    elif intensity == "hard":
        out += [
            "「っ……強いな。想定外だ」",
            "「護る側が、こんな声を……恥ずかしい」",
            "「それでも、逃げはしない。責任は、自分が取る」",
        ]
    else:
        out += [
            "「続けてくれ。中途半端は嫌いだ」",
            "「熱い……。役者の仮面が、少し、剥がれる」",
            "「……悪い。声が、漏れた」",
        ]
    return out

def on_bond(g):
    aff, flags = _aff(g), _flags(g)
    if g.get("pregnancy_noticed") or "pregnant" in g.get("tags", []):
        return [
            "レイアは腹に手を当て、静かに頷く。",
            "「新しい命の責任も、引き受ける」",
            "「君がそばにいてくれるなら……少し、楽だ」" if aff >= 70 else "「一人でもやり遂げる。それが私だ」",
        ]
    if aff >= 100 and flags[0] == 0:
        flags[0] = 1
        return [
            "レイアの目が、舞台袖の暗がりのように柔らぐ。",
            "「言うべきだろう。好きだ」",
            "「いつも護る側に回っていた。君の前では……頼りたい」",
            "「逃げないでくれ。私が中心でいられなくても、君がいてほしい」",
        ]
    if aff < 30:
        return [
            "「用件は？　無駄話に時間は使えない」",
            "「周囲を護るのが私の役目だ。君も、足手まといになるな」",
            "「……猫の話なら、少しだけなら聞ける」",
        ]
    if aff < 60:
        return [
            "「今日も無事か。確認しに来ただけだ」",
            "「努力は好きではないが、やらねばならない」",
            "「君は、比較的、話しやすい相手だ」",
        ]
    if aff < 90:
        return [
            "「……少し、休ませてくれ。仮面が重い」",
            "「君がいると、呼吸が楽になる。事実だ」",
            "「甘えるのは下手だ。許してくれ」",
        ]
    return [
        "「好きだ。何度でも言う」",
        "「舞台を降りても、君の隣に立ちたい」",
        "「護られる側になっても……いい、のか」",
    ]

def on_sex(g, affection=0):
    aff = affection or _aff(g)
    out = ["レイアは自ら襟をほどき、視線を逸らさない。"]
    if "virgin" in g.get("tags", []):
        out += ["「初めてだ。指導してくれ。……頼む」", "「痛むなら言う。役者の我慢は、ここでは不要だ」"]
    out += ["「ん……っ。台詞にない声だ」", "「深いな……責任を、感じる。奇妙な言い方だが」"]
    if "virgin" in g.get("tags", []):
        out += ["「繋がった……。逃げない。受け止める」"]
    if aff >= 70:
        out += ["「もっと、くれ。君の熱で、仮面を、外してくれ……っ」"]
    else:
        out += ["「先に、イく……すまない……っ」"]
    out += ["「……終わったな。隣にいてくれ。少しだけ」"]
    return out

def on_tentacle_train(g):
    return [
        "「触手か。……観客のいない舞台だな」",
        "レイアの手首を拘束するように、柔らかい腕が絡む。",
        "「やめろ……護る側が、開発されるなど……っ」",
        "「感じてしまう。認めざるを得ない」",
        "「……責任は、後で取る。今は、耐える」",
    ]

def on_tentacle_sex(g):
    out = [
        "触手がレイアの脚を開く。視線はまだ、どこか役者だ。",
        "「入れるのか。……孕ませるための、演出か」",
    ]
    if "virgin" in g.get("tags", []):
        out += ["「初めてが、これか。……受け入れる。選択の余地はない」"]
    out += [
        "「奥だ……っ。子宫を、護れない……」",
        "「イく……舞台袖で、崩れ落ちるみたいに……っ」",
        "「……精を、受けた。生きる。それも責任だ」",
    ]
    return out

def on_pregnancy_notice(g):
    bt = g.get("baby_type") or "？"
    if _aff(g) >= 70:
        return "\n".join([
            "「生理が来ない。妊娠だ」",
            f"「種別は{bt}。報告する。君にだけは、隠さない」",
            "「親になる責任も、背負う。そばにいてくれ」",
        ])
    return "\n".join([
        "「妊娠した。以上が報告だ」",
        f"「{bt}だ。……一人でもやり遂げる」",
    ])

def on_birth(g):
    bt = g.get("baby_type") or "？"
    return "\n".join([
        "「……いく。声を、抑えない。演技ではない」",
        f"産声。{bt}。",
        "「果たした。……君がいてくれて、助かった」",
    ])

def on_witchify(g):
    return "\n".join([
        "「護れない。……自分が、崩れても」",
        "「舞台上の偶像が、魔女になるなど」",
        "蓮見レイアは封印の光に消える。",
    ])

def on_ending_elope(g):
    return "\n".join([
        "「逃げる。護る対象は、君一人でいい」",
        "「外でも、隣に立たせてくれ」",
    ])

def on_ending_shinju(g):
    return "\n".join([
        "「魔女になるくらいなら……君を、一人にしない」",
        "「これが、私の最後の責任だ。好きだ」",
    ])
