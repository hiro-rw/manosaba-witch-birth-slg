# -*- coding: utf-8 -*-
"""
registry.py
少女モジュールの登録表。新人は MODULES に1行追加。
"""

from game.characters import (
    emma, hiro, shelly, arisa, margo, anan,
    hanna, nanoka, noa, reia, miria, meruru,
)

MODULES = [
    emma, hiro, shelly, arisa, margo, anan,
    hanna, nanoka, noa, reia, miria, meruru,
]

BY_KEY = {m.KEY: m for m in MODULES}


def get_module(key):
    return BY_KEY.get(key)


def all_initials():
    import copy
    result = {}
    for m in MODULES:
        data = copy.deepcopy(m.INITIAL)
        result[data["key"]] = data
    return result
