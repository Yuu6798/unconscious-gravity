from dataclasses import dataclass

@dataclass
class TurnLog:
    """
    1ターン分の対話ログ情報をまとめるデータクラス
    """
    TurnId: int      # ターンの識別子（例：連番）
    Prompt: str      # ユーザーからの入力テキスト
    Response: str    # AIからの応答テキスト
    Q_self: float    # 自己照合スコア（例：前後レスポンス類似度）
    S_q: float       # 照合空間の大きさ・密度
    t_total: int     # このターンでかかった処理時間（ミリ秒）
    M: float         # 任意のメトリクス（例：追加評価指標）