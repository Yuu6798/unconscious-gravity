# examples/simulate_PoR.py

from main import UnconsciousGravityHypothesis
from viewer import PoRViewer

# 仮説クラスとビューアの初期化
hypothesis = UnconsciousGravityHypothesis()
viewer = PoRViewer()

# === ユーザー入力（PoR照合にかける問いと構造状態） ===
query = "存在とは何か？"
system_state = {"context": "生成AIにおける選択空間", "bias": "無意識的重力"}

# === 照合処理 ===
score = hypothesis._calculate_potential(query, system_state)
result = hypothesis.simulate_future_selection(query, system_state)

# === 表示 ===
viewer.visualize_structure(query, score)
viewer.display_result(result)
viewer.show_history()
