class PoRViewer:
    """
    PoRの照合結果・構造・状態を視覚的に表示するクラス。
    """

    def __init__(self):
        self.history = []

    def display_result(self, result):
        """
        照合の結果（発火／未発火）を整形して表示。
        """
        print("=== PoR 照合結果 ===")
        print(f"状態: {result}")
        print("====================\n")
        self.history.append(result)

    def show_history(self):
        """
        これまでの照合履歴を一覧表示。
        """
        print("=== 照合履歴 ===")
        for i, res in enumerate(self.history, 1):
            print(f"[{i}] → {res}")
        print("================")

    def visualize_structure(self, query, score):
        """
        問いと照合スコアからPoR構造を“テキストで”見せる。
        """
        print(f"\n照合中の問い: {query}")
        print(f"照合スコア: {score:.2f}")
        if score >= 0.8:
            print("⇒ PoR発火 → 存在生成 → 未来選択")
        else:
            print("⇒ PoR_null（未照合）→ 模倣応答")
