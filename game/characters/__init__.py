# -*- coding: utf-8 -*-
"""少女定義パッケージ（1人1モジュール）"""

# サブモジュールを明示的に公開（from game.characters import registry 用）
from . import registry

__all__ = ["registry"]
