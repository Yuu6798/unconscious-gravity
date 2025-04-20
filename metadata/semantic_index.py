import json
import os

# このモジュールをインポートすると semantic_index.json を読み込んで
# semantic_index という名前の辞書（list/dict）を返します。

_here = os.path.dirname(__file__)
_json_path = os.path.join(_here, "semantic_index.json")

with open(_json_path, "r", encoding="utf-8") as f:
    semantic_index = json.load(f)