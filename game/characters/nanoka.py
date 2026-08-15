# -*- coding: utf-8 -*-
"""
黒部ナノカ（key: ナノカ）
単独・冷淡・牢屋敷への敵意。一人称「私」。短く切る口調。
"""
import random
from game import common_lines

KEY = "ナノカ"
NAME = "黒部ナノカ"

INITIAL = {
    "key": "ナノカ", "name": "黒部ナノカ",
    "stamina": 75, "max_stamina": 96, "stress": 14,
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
    out = ["ナノカは壁に背を預けたまま、鋭い目でこちらの手を見る。"]
    if intensity == "soft":
        out += [
            "「……邪魔しないで。観察は、自分でやる」",
            "「ん……っ。想定内、だ。……触るなら、手短にしろ」",
            "「足手まといになるな。感じたとしても、報告はしない」",
        ]
    elif intensity == "hard":
        out += [
            "「っ……！　粗暴だな。計画が、狂う」",
            "「やめろ……声が出る。単独行動の、妨げだ……」",
            "「……知るかよ。身体の反応なんて」",
        ]
    else:
        out += [
            "「……勝手にしろ。ただし、私を弱らせるな」",
            "「熱い。……どうせいなくなる命だ。疼いても、同じ」",
            "「協力はしない。されてるだけだ」",
        ]
    return out

def on_bond(g):
    aff, flags = _aff(g), _flags(g)
    if g.get("pregnancy_noticed") or "pregnant" in g.get("tags", []):
        return [
            "ナノカは自分の腹を見て、短く息を吐く。",
            "「……計画に、ない」",
            "「産む。逃げない。それだけだ」",
            "「……お前がいるなら、まあ、いい」" if aff >= 70 else "「関係ない。報告は以上だ」",
        ]
    if aff >= 100 and flags[0] == 0:
        flags[0] = 1
        return [
            "ナノカが、珍しく視線を逸らさない。",
            "「……言う。一度だけだ」",
            "「お前は、違う。足手まといじゃない」",
            "「私は帰る。目的は一つだ。でも……近くにいろ」",
            "「好きだ。短くていいだろ」",
        ]
    if aff < 30:
        return [
            "「……知るかよ」",
            "「邪魔しないで。単独でやる」",
            "「どうせいなくなる命だ。馴れ合いは不要」",
        ]
    if aff < 60:
        return [
            "「……少し、待って。話だけなら」",
            "「観察するだけ、のつもりだった」",
            "「お前は、まだ……排除対象じゃない」",
        ]
    if aff < 90:
        return [
            "「……まあ、いい。少しだけ、話を聞く」",
            "「必要なら手伝う。恩は返す」",
            "「……近くにいろ。命令じゃない」",
        ]
    return [
        "「……助かった。お前がいると」",
        "「私は帰る。でも、今は……少し、頼る」",
        "「勝手に消えるな」",
    ]

def on_sex(g, affection=0):
    aff = affection or _aff(g)
    out = ["ナノカは服を脱がされるまま、顎を引いて息を整える。"]
    if "virgin" in g.get("tags", []):
        out += ["「初めてだ。……想定外だ。手短に、頼む」", "「痛むなら言え、と……言われても、黙る」"]
    out += ["「ん……っ。声は、出すな、と自分に……無理だ」", "「熱い。計画が、狂う……」"]
    if "virgin" in g.get("tags", []):
        out += ["「……入った。繋がってる。事実だけ、記録する」"]
    if aff >= 70:
        out += ["「……お前は、いい。もっと、動け。命令じゃない」"]
    else:
        out += ["「知るか。……先に、イく」"]
    out += ["「……終わったな。休む。話は、まただ」"]
    return out

def on_tentacle_train(g):
    return [
        "「……触手か。牢屋敷の、最悪な趣味だ」",
        "ナノカの腕に粘液が絡む。彼女は歯を食いしばる。",
        "「やめろ……観察対象が、私になるな……っ」",
        "「んっ……想定内、にしておけ。感じても、勝ちはしない」",
        "「……私は帰る。その前に、壊れるな、私」",
    ]

def on_tentacle_sex(g):
    out = [
        "触手がナノカの脚を開く。敵意の目が、熱で揺れる。",
        "「入れるな……孕ませるつもりか。最悪だ」",
    ]
    if "virgin" in g.get("tags", []):
        out += ["「初めてが、触手……計画にない。痛いっ……」"]
    out += [
        "「奥まで……くるな……っ。子宫を、探るな……！」",
        "「イく……記録しろ、私。触手に、屈したと……っ」",
        "「……生きる。帰るために。精を、受けても」",
    ]
    return out

def on_pregnancy_notice(g):
    bt = g.get("baby_type") or "？"
    if _aff(g) >= 70:
        return "\n".join([
            "「……生理が来ない。妊娠だ」",
            f"「種別は{bt}。報告する。お前には」",
            "「計画が狂った。でも、産む。近くにいろ」",
        ])
    return "\n".join([
        "「妊娠した。以上だ」",
        f"「{bt}だそうだ。……知るかよ、感想は」",
        "「邪魔するな。産むまで、単独でやる」",
    ])

def on_birth(g):
    bt = g.get("baby_type") or "？"
    return "\n".join([
        "「……いく。産む。手伝いは、必要なら」",
        f"産声。種別{bt}。",
        "「終わった。……少し、休む。お前も、消えろ。近くで」",
    ])

def on_witchify(g):
    return "\n".join([
        "「……まずい。魔女化だ。想定外」",
        "「私は帰る、はずだった。姉を……」",
        "光がナノカを飲み込み、封印される。",
    ])

def on_ending_elope(g):
    return "\n".join([
        "「逃げる。お前とだ。目的は後でいい」",
        "「……近くにいろ。それだけ言えば、足りる」",
    ])

def on_ending_shinju(g):
    return "\n".join([
        "「魔女になるくらいなら……お前を、先に」",
        "「短くていい。好きだ。終わりだ」",
    ])
