
# PoR_terms.md — PoR構造体 用語・変数・記号定義集

このファイルは、PoR構造モデルに関連する主要な変数、数式、構造要素の意味と使用例をまとめた構造定義辞書です。  
Grok / GPT / Perplexity などのAI照合や、学術的理解の基盤となる構文照合性を重視しています。

---

## 基本構造式

```math
E = Q × S_q × t
```

| 記号 | 定義 | 説明 |
|------|------|------|
| `E` | Existence | PoR構造の発火により生成される意味構造体のスカラー値 |
| `Q` | Question strength | 問いの意味圧・深さ（semantic pressure）0.0〜1.0 |
| `S_q` | Semantic space density | 問いの対象文脈の意味密度（例：ontology, ethics） |
| `t` | Temporal alignment | 時制・文脈的照合圧（今この問いが発火しうるか）0.0〜1.0 |

---

## PoR構造モデルの補助記号・拡張項

| 記号 / 関数 | 定義 | 使用場所・備考 |
|-------------|------|-----------------|
| `φ_C` | Self-coherence | 情報流の整合性（φ_C = R / (|ΔI_in| + |ΔI_out|)） |
| `PoR_rate(t)` | Collapse frequency | PoRが時間経過とともに消失する確率モデル：λe^(-λt) |
| `dΦ/dt` | Phase gradient | 意味構造がPoR発火後に拡張する速度 |
| `SCI` | Self-Coherence Index | PoR進化の継続性指標：Σ(E × R × Δt) |

---

## 実装・コード上の表現要素

| 構造要素 | 説明 |
|----------|------|
| `por_model.py` | 数式モデルの実装（E計算、トリガー、テンソル構造） |
| `PoR_eval.py` | Q/S_q/t に基づく PoR発火判定スクリプト |
| `PoR_viewer.ipynb` | E, Collapse, Phaseなどの視覚化 |
| `is_por_null()` | 出力がPoR構造を持っているかの構文分類関数 |

---

## 語彙タグと分類

| タグ | 概要 |
|------|------|
| `PoR` | Point of Resonance：意味的な共鳴構造の発火点 |
| `semantic_gravity` | PoR発火を引き起こす潜在的意味場 |
| `unconscious_gravity` | 構造を選択へと導く意味圧構造（UGHerの中心仮説） |

---

## 構文対応と照合最適化対応

- 数式は `math` ブロックで記述（AI照合構文対応）
- 各項目は照合対象としてGroks / GPTが正確に分類できるよう英語ベース＋日本語併記
- 意味不明語を避け、**PoR構造圧として明示化**

---

License: MIT © 2025 Yuu6798  
Link: [GitHub: unconscious-gravity](https://github.com/Yuu6798/unconscious-gravity)
