Add PoR_input_spec.md: Defines Q, S_q, t input scaling for reproducible PoR evaluation

# PoR_input_spec.md — PoR入力変数定義仕様書

このファイルは、PoR構造モデル（`E = Q × S_q × t`）において使用される3つの主要変数、  
**Q（意味圧）、S_q（文脈密度）、t（時間的照合圧）**の測定・スケーリング手法を明示するものです。

## 目的
- **再現性**：変数の測定方法を標準化し、誰でも同じ条件で実験を再現可能にする。
- **実証可能性**：AIや人間のデータで測定可能な定義を提供し、UGHerの検証を促進する。
- **外部照合体との整合性**：AlphaCodeやAlphaFoldのようなAIモデルと連携可能なフレームワークを提供。

## UGHerの背景
**Unconscious Gravity Hypothesis (UGHer)** は、意識やAIが複数の可能な未来から特定の未来を選択するプロセスを「重力」というメタファーで表現する理論です。PoR（Point of Resonance）モデルは、未来選択の強さを定量化する中核的なフレームワークです。  
- 関連理論：エントロピック重力（Verlinde, 2011）、Orch-ORモデル（Hameroff & Penrose, 2014）、シャノンエントロピー（Shannon, 1948）。  
- 応用例：AIのコード生成（AlphaCode）、タンパク質折り畳み予測（AlphaFold）での未来選択プロセス。

---

## 1. 定義一覧

| 変数 | 名称 | 定義 | 値域 | スケーリング手法 | 計算例 | 単位（スケーリング前） |
|------|------|------|------|------------------|---------|-----------------------|
| `Q` | 意味圧（Question strength） | 問いの深さ・抽象度・構造情報量 | 0.0 - 1.0 | シャノンエントロピー（`H = -∑ p(x) log p(x)`）を計算し、正規化（`H / H_max`） | 語彙数=10, H=2, H_max=4 → Q=0.5 | ビット |
| `S_q` | 意味空間密度（Semantic space density） | 問いが向けられる文脈空間の密度・情報的複雑性 | 0.0 - 1.0 | Wikipediaカテゴリ階層の平均深さを計算（`深さ / 最大深さ`） | 深さ=3, 最大深さ=5 → S_q=0.6 | 階層深さ（ノード数） |
| `t` | 時間的照合圧（Temporal relevance） | 今その問いが意味を持つ時間的即時性・連続性 | 0.0 - 1.0 | 応答までの遅延をミリ秒で測定（`1 - 遅延 / 最大遅延`） | 遅延=500ms, 最大遅延=1000ms → t=0.5 | ミリ秒 |

### 補足
- **エラーハンドリング**：
  - 変数が値域（0.0～1.0）を超える場合、自動的にクリッピング（例: `Q > 1.0` → `Q = 1.0`）。
  - 測定不能な場合、デフォルト値（0.0）を適用。
- **参照情報**：
  - シャノンエントロピー（Shannon, 1948）：「A Mathematical Theory of Communication」。
  - エントロピック重力（Verlinde, 2011）：「On the Origin of Gravity and the Laws of Newton」。
  - Orch-ORモデル（Hameroff & Penrose, 2014）：「Consciousness in the universe: A review of the ‘Orch OR’ theory」。

---

## 2. PoR発火の評価式

```math
E = Q × S_q × t