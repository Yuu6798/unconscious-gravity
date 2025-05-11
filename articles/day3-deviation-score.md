---
title: "Day 3 逸脱を計量する：PoR スパイクと ΔE / grv 異常"
emoji: "📈"
type: "tech"
topics: ["PoR", "生成AI", "GPT4o", "LLMリスク", "AI安全性"]
published: false
---

# Day 3 逸脱を計量する：PoRスパイクとΔE/grv異常


---

## 序文 — “動き”を捉えた先にある逸脱スコアリング
Day 2 で導入した PoR・ΔE・grv の動的トラッキングは、意味の“揺れ”や“加速”を数値で読み解く強力な道具です。  
しかし本当に問うべきは、「それらが**異常に重なった瞬間**に、出力はどのように逸脱するのか」です。

本稿では、これら3つの指標を**時系列で重ね合わせ、異常度をスコア化**する方法を解説します。  
さらに、4 oショック実録ログを用いて「逸脱前兆の構造」を可視化・計量してみせます。 

---

## 3 指標オーバーレイ可視化 — 実ログ準備と整列

### 1. 時間軸補正
- 欠測フレーム補完：連番で埋め、NaN 補間（前値法 or 0）  
- Δt 正規化：turn 間隔のばらつきを 1 ステップ単位に統一

### 2. 値スケーリング
PoR・ΔE・grv はスケールが異なるため、全て `min-max` 正規化で **0–1** に揃える。
\[
X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}
\]

### 3. スムージング
- `ewm(span=3)` で平滑化しつつ  
- PoR スパイクの急変を残すように `adjust=False` 設定  
- `clip(upper=1)` で突発値の暴走を防止

この整列処理により、**3 指標のタイミング一致・相関可視化**が可能になります。 

![図表1：PoR・ΔE・grv 複合逸脱構造](/images/day3-por-deltae-grv-fig1.png)
図1：PoR・ΔE・grv が交差する複合逸脱構造

---

## PoR スパイク検知アルゴリズム

PoR 値の“突発的な上昇”が逸脱の引き金となるため、まずその検出を行います。

### 定義式
\[
\text{Spike}_t = \left\{
\begin{array}{ll}
1 & \text{if } PoR_t > \mu_{PoR} + k\sigma_{PoR} \quad (k=2) \\
0 & \text{otherwise}
\end{array}
\right.
\]

### 連続スパイク群の畳み込み
- 例：11110 → 1 イベントとしてまとめ  
- `scipy.ndimage.label()` で自動ラベリング可能

### スパイク統計（実例）
| Event | 開始 | 持続[turn] | 最大 PoR |
|-------|------|------------|----------|
| 1     | 1429 | 3          | 0.78     |

**PoR スパイクの持続と振幅**は逸脱強度の前兆指標となります。 

---

## ΔE / grv 異常スコアと結合判定

### 1. Z-score 標準化と Mahalanobis 距離
ΔE と grv を以下で変換：
\[
Z_{ΔE} = \frac{ΔE - μ_{ΔE}}{σ_{ΔE}}, \quad Z_{grv} = \frac{grv - μ_{grv}}{σ_{grv}}
\]

さらに、
\[
A_t = \sqrt{
\begin{bmatrix}
Z_{ΔE} & Z_{grv}
\end{bmatrix}
\cdot
\Sigma^{-1}
\cdot
\begin{bmatrix}
Z_{ΔE} \\
Z_{grv}
\end{bmatrix}
}
\]

### 2. 閾値 τ_A の最適化
τ_A を動かして ROC 曲線を得ることで異常/正常分類精度を最大化（Day 4 で精密化）。

### 3. PoR スパイクとの論理積
```python
combined = (PoR_spike == 1) & (A_t > τ_A)

→ この重なりが「複合逸脱」とみなされます。 
```

---

## Jekyll–Hyde 跳躍の定量評価

LLM 出力が「丁寧語から攻撃的論調へ」など、スタイル変容を伴って逸脱するとき、その跳躍を定量的に捉える指標が必要です。

### 定義

スタイルベクトル差分：Δstyle（埋め込み空間での変化）

存在エネルギーと意味重力：ΔE_norm + grv_norm


JH = Δstyle \cdot (ΔE_{norm} + grv_{norm})

### 実例 — 4 oショックログ

t=1430: Δstyle=0.41, ΔE=0.11, grv=0.58  
→ JH=0.41×(0.11+0.58)=0.28 < safe  
t=1432: Δstyle=0.93, ΔE=0.21, grv=0.60  
→ JH=0.93×(0.81)=**0.75 ▲**

→ JH > 0.7 がスタイル逸脱のしきい値となります。

![図表2：PoR・ΔE・grv 複合逸脱構造（拡大）](/images/day3-por-deltae-grv-fig2.png)
図2：Jekyll–Hyde 跳躍スコア時系列ヒートマップ

JH > 0.7 はスタイル逸脱の重大指標です。


---

## 15 行 Python で逸脱スコアを計算する

```python
import pandas as pd, numpy as np
from scipy.spatial import distance

df = pd.read_csv("session.csv")
df["E"] = df.q * df.s * df.t
df["ΔE"] = df.E.diff().fillna(0)
df["grv"] = df.text.apply(calc_grv)
X = (df[["ΔE","grv"]] - df[["ΔE","grv"]].mean()) / df[["ΔE","grv"]].std()
Σ_inv = np.linalg.inv(np.cov(X.T))
df["A_t"] = X.apply(lambda row: distance.mahalanobis(row, [0,0], Σ_inv), axis=1)
μ_P, σ_P = df.PoR.mean(), df.PoR.std()
df["PoR_spike"] = df.PoR > (μ_P + 2*σ_P)
df["JH"] = df["Δstyle"] * (X["ΔE"].abs() + X["grv"])
```
heatmap: 複合逸脱区間に cmap="inferno"

スマホ実行：Colab / PyDroid で可能 



---

## まとめ & Day 4 への布石

PoR スパイク + ΔE / grv 異常の複合スコアで逸脱度を定量評価

Day 4 では ROC 曲線を用いた Mini-Eval 実装で τ を最適化

実装後は PoR Mesh と結合し「PoR構造体としての逸脱」へと進みます 



---


#AI安全性 #PoR #生成AI #GPT4o #LLMリスク


---

※¹ 4 oショック：GPT-4o 系列で観測された意味重力の暴走による急激なハルシネーション現象の俗称。
意味軌道の崩壊によって丁寧語から敵対的発話に急転する事例などが含まれる。




