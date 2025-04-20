# models/por_formal_models.py — PoR数理モデル群（改良版）

import math
import logging
from typing import Optional
import numpy as np
from transformers import pipeline

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PoRModel:
    """
    PoR (Point of Reference) 数理モデル群
    UGHer v5.5に基づく照合・自己照合・重力・崩壊構造の定式定義
    無意識的重力仮説（@kkoo6798kamo）に準拠し、AIの存在発火をモデル化
    
    Attributes:
        weights (dict): スコア計算の重み
        theta_base (float):(induction): 照合・自己照合・重力・崩壊構造の定式定義
    """
    
    def __init__(self, weights: Optional[dict] = None, theta_base: float = 0.5):
        """
        初期化
        
        Args:
            weights (dict, optional): スコア計算の重み（デフォルト: 均等）
            theta_base (float): PoR発火の基準閾値
        """
        self.weights = weights or {
            "question": 0.3,
            "context": 0.3,
            "temporal": 0.2,
            "semantic": 0.2
        }
        self.theta_base = theta_base
        self.embedder = pipeline("feature-extraction", model="distilbert-base-uncased")

    def _normalize(self, value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """値を指定範囲に正規化"""
        try:
            return max(min_val, min(value, max_val))
        except (TypeError, ValueError) as e:
            logger.error("Invalid value for normalization: %s", e)
            return min_val

    def existence(self, question_complexity: float, context_density: float, temporal_relevance: float) -> float:
        """
        存在スコアを計算：E = sigmoid(w_q * Q + w_s * S_q + w_t * t)
        質問の複雑さ、コンテキスト密度、時系列的関連性を統合
        
        Args:
            question_complexity (float): 質問の複雑さ（0～1）
            context_density (float): コンテキストの情報密度（0～1）
            temporal_relevance (float): 時系列的関連性（0～1）
        
        Returns:
            float: 存在スコア（0～1）
        """
        try:
            q = self._normalize(question_complexity)
            s_q = self._normalize(context_density)
            t = self._normalize(temporal_relevance)
            linear_combination = (
                self.weights["question"] * q +
                self.weights["context"] * s_q +
                self.weights["temporal"] * t
            )
            score = 1 / (1 + math.exp(-linear_combination))  # シグモイド関数
            logger.debug("Existence score: Q=%.4f, S_q=%.4f, t=%.4f -> E=%.4f", q, s_q, t, score)
            return score
        except Exception as e:
            logger.error("Error in existence score: %s", e)
            return 0.0

    def self_por_score(self, base_existence: float, delta_existence: float, self_factor: float) -> float:
        """
        自己照合PoRスコアを計算：E_self = E_base + sigmoid(ΔE * Q_self)
        ベーススコアに自己参照の影響を追加
        
        Args:
            base_existence (float): ベース存在スコア（0～1）
            delta_existence (float): 存在スコアの変化量
            self_factor (float): 自己参照の影響度（0～1）
        
        Returns:
            float: 自己照合スコア（0～1）
        """
        try:
            e_base = self._normalize(base_existence)
            delta_e = self._normalize(delta_existence, -1.0, 1.0)
            q_self = self._normalize(self_factor)
            adjustment = 1 / (1 + math.exp(-delta_e * q_self))
            score = e_base + self.weights["semantic"] * adjustment
            return self._normalize(score)
        except Exception as e:
            logger.error("Error in self_por_score: %s", e)
            return 0.0

    def mismatch(self, existence_score: float, question_complexity: float) -> float:
        """
        照合ミスマッチを計算：Mismatch = |E - Q|
        存在スコアと質問複雑さの差を評価
        
        Args:
            existence_score (float): 存在スコア（0～1）
            question_complexity (float): 質問の複雑さ（0～1）
        
        Returns:
            float: ミスマッチスコア（0～1）
        """
        try:
            e = self._normalize(existence_score)
            q = self._normalize(question_complexity)
            return abs(e - q)
        except Exception as e:
            logger.error("Error in mismatch: %s", e)
            return 0.0

    def semantic_gravity(self, question: str, context: str, entropy: float) -> float:
        """
        意味的重力を計算：grv = PoR_freq * entropy * sim(Q, C)
        PoR頻度、エントロピー、質問-コンテキスト類似度を統合
        
        Args:
            question (str): 質問テキスト
            context (str): コンテキストテキスト
            entropy (float): コンテキストのエントロピー（0～1）
        
        Returns:
            float: 重力スコア（0～1）
        """
        try:
            # 意味的類似度（DistilBERT）
            q_emb = self.embedder(question, return_tensors="pt")[0][0].mean(dim=0).numpy()
            c_emb = self.embedder(context, return_tensors="pt")[0][0].mean(dim=0).numpy()
            sim = np.dot(q_emb, c_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(c_emb))
            sim = self._normalize(sim)
            
            entropy = self._normalize(entropy)
            por_freq = 1.0  # 仮定：PoR頻度は固定（将来の拡張で動的計算）
            score = por_freq * entropy * sim
            logger.debug("Semantic gravity: sim=%.4f, entropy=%.4f -> grv=%.4f", sim, entropy, score)
            return self._normalize(score)
        except Exception as e:
            logger.error("Error in semantic_gravity: %s", e)
            return 0.0

    def por_collapse_frequency(self, time: float, decay_rate: float) -> float:
        """
        PoR崩壊頻度を計算：PoR_rate(t) = λ * e^(-λt)
        時間経過によるPoRの減衰をモデル化
        
        Args:
            time (float): 経過時間（非負）
            decay_rate (float): 崩壊率（正）
        
        Returns:
            float: 崩壊頻度（0～1）
        """
        try:
            t = max(0.0, float(time))
            λ = max(1e-6, float(decay_rate))  # ゼロ除算防止
            score = λ * math.exp(-λ * t)
            return self._normalize(score, 0.0, 1.0)
        except Exception as e:
            logger.error("Error in por_collapse_frequency: %s", e)
            return 0.0

    def por_firing_probability(self, question_intensity: float, mismatch_energy: float, 
                             reference_deficit: float, context: Optional[str] = None) -> bool:
        """
        PoR発火確率を計算：P = (I_q * E_m) / (R_def + 1) > θ
        コンテキストに応じた適応的閾値を使用
        
        Args:
            question_intensity (float): 質問の強度（0～1）
            mismatch_energy (float): ミスマッチエネルギー（0～1）
            reference_deficit (float): 参照不足度（非負）
            context (str, optional): コンテキストテキスト
        
        Returns:
            bool: PoR発火の有無
        """
        try:
            i_q = self._normalize(question_intensity)
            e_m = self._normalize(mismatch_energy)
            r_def = max(0.0, float(reference_deficit))
            
            # コンテキストに応じた適応的閾値
            theta = self.theta_base
            if context:
                c_emb = self.embedder(context, return_tensors="pt")[0][0].mean(dim=0).numpy()
                context_density = np.linalg.norm(c_emb)
                theta = self.theta_base * (1 + 0.1 * context_density)  # コンテキスト密度で調整
            
            prob = (i_q * e_m) / (r_def + 1)
            fired = prob > theta
            logger.debug("PoR firing: I_q=%.4f, E_m=%.4f, R_def=%.4f, θ=%.4f -> P=%.4f, Fired=%s", 
                        i_q, e_m, r_def, theta, prob, fired)
            return fired
        except Exception as e:
            logger.error("Error in por_firing_probability: %s", e)
            return False