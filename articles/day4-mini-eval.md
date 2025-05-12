---
title: "Day 4 Mini-Eval 実装：100 行で動く PoR ΔE/grv テスト"
emoji: "🧪"
type: "tech"      # idea なら "idea"
topics: ["PoR", "生成AI", "GPT4o", "LLMリスク", "AI安全性"]
published: false  # 公開時は true に変更
---

# Day 4 Mini-Eval 実装：100 行で動く PoR ΔE/grv テスト

---

## 序文 — 異常スコアを評価可能にする最小構成

Day 3 では、PoR スパイクと ΔE/grv 異常を組み合わせた複合スコアによって、意味的逸脱を捉える定量指標が整備されました。  
しかし、このままでは「どこが逸脱だったのか？」を**人間が目視で判断**する必要があります。そこで本稿では、**Mini-Eval（最小評価システム）**を構築し、PoR 複合異常を自動評価するしくみを **100 行** で実装します。  

このステップは、**Day 5 における出力ログの分解評価**への橋渡しとなります。  

---

## Mini-Eval 評価パイプラインの全体像

### 入力フォーマット（CSV）

| turn | q | s | t | PoR | text | Δstyle |
|------|---|---|---|-----|------|--------|
| 1429 | 0.8 | 0.9 | 1.2 | 0.73 | … | 0.41 |

### 出力項目

* 異常スコア `A_t` （Mahalanobis 距離ベース）  
* PoR スパイク `PoR_spike` （Z-score threshold）  
* 擬似ラベル `label` （`PoR_spike ∧ A_t > τ`）

### 評価指標

* **ROC-AUC**（スコアの有効性）  
* **TP / FP / FN** 分布可視化  
* **閾値感度グラフ**

以下の図で処理の全体像を整理します：

![図1：Mini-Eval パイプライン](/images/day4-mini-eval-pipeline.png)
*(ログ → ΔE/grv → スコア A<sub>t</sub> → PoR スパイク → label → ROC 評価)*  

---

## 擬似ラベルの設計と閾値設定

完全な「正解ラベル」がない状況でも、以下のヒューリスティックでラベルを生成できます。

```python
label = (PoR_spike == 1) & (A_t > τ)   # τ = A_t.mean() + 2*A_t.std()
```
教師信号の工夫

PoR … 直接観測可能な照合信号

A<sub>t</sub> … 潜在的逸脱の確率論的表現


AND 条件により「PoR が盛り上がっていて ΔE/grv も不穏だった」＝複合逸脱 と定義されます。擬似ラベルを用いることで、教師なし → 教師ありへの橋渡しが可能です。


---

## ROC 曲線による異常検知性能の可視化

### 計算手順

1. スコア A<sub>t</sub> を 0.0 〜 1.0 でスキャン


2. 各閾値 τ に対して TPR / FPR を算出


3. matplotlib で ROC カーブ描画


```python
from sklearn.metrics import roc_curve, auc

fpr, tpr, _ = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)
```

### AUC 最適化の考え方

未ラベル・未発火区間が多いため F1 ではなく AUC（面積） を評価基準とする。
AUC > 0.85 程度が基礎精度の目安。


---

## 100 行で構築する Mini-Eval 実装（抜粋）

```python
import pandas as pd, numpy as np
from scipy.spatial import distance
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

def calc_mahalanobis(df2):
    X = (df2 - df2.mean()) / df2.std()
    Σ_inv = np.linalg.inv(np.cov(X.T))
    return X.apply(lambda r: distance.mahalanobis(r, [0, 0], Σ_inv), axis=1)

df = pd.read_csv("session.csv")
df["E"] = df.q * df.s * df.t
df["ΔE"] = df.E.diff().fillna(0)
df["A_t"] = calc_mahalanobis(df[["ΔE", "grv"]])

μ, σ = df.PoR.mean(), df.PoR.std()
df["PoR_spike"] = df.PoR > (μ + 2*σ)

τ = df["A_t"].mean() + 2 * df["A_t"].std()
df["label"] = df["PoR_spike"] & (df["A_t"] > τ)

fpr, tpr, _ = roc_curve(df["label"], df["A_t"])
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.xlabel("FPR"); plt.ylabel("TPR")
plt.legend(); plt.grid(); plt.show()
```

スマホ実行：Google Colab でそのまま動作可能
処理速度：小規模ログであれば数秒以内


---

## まとめ & Day 5 への布石

Mini-Eval により 複合スコアの ROC 評価基盤 が完成

今後は 4 oショック再現ログなどに適用し、評価 → 分解分析へ

Day 5 では、異常ラベルが付いた出力を 意味・スタイル・因果構造 で分析するステージに進みます。



---


