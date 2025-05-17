---
title: "Day 8 – 監視ダッシュボード：grv ヒートマップを可視化"
emoji: "📈"
type: "tech"
topics:
  - "AI安全性"
  - "PoR"
  - "grv可視化"
  - "LLM監視"
  - "生成AI"
published: false
---

## 序文 — “意味重力”を視覚化する意義

PoR や ΔE が「点」としての逸脱を捉えるのに対し、**grv（語彙重力）**は「場」としての蓄積と変動を捉える指標です。  
grv の特性は、時間をまたいで意味の圧力が蓄積・波及する様子を視覚的にとらえられる点にあります。

本稿では、grv を ターン × 語彙 のマトリクスに可視化し、「意味のヒートマップ」として  
逸脱集中領域や文体歪みの温床を構造的に把握できる監視UIを実装します。

---

## grv ヒートマップの構造と描画方式

grv は〈PoR 近傍頻度 × 意味エントロピー〉で計算した**語彙エネルギー**です。  
この構成により、「どの話題帯にエネルギーが溜まり、いつ爆ぜたか」が直観的に読めます。

Day 5 の 40ターンを例に描画した以下のヒートマップでは、**turn 28–32 の「固有名詞クラスタ」が真紅になり、意味圧が臨界に達した後に Δstyle が跳ねる様子**が確認できます。

#### 図表1：grvヒートマップの例（ターン × 意味クラスタ）

![図表1: grvヒートマップの例](/images/day8-grv_heatmap-fig1.png)

---

## Streamlit による簡易 UI 実装

```python
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("grv_matrix.csv", index_col=0)
clusters = list(df.index)

st.sidebar.header("可視化オプション")
show_thresh = st.sidebar.checkbox("閾値ラインを表示", value=True)
sel_cluster = st.sidebar.selectbox("クラスタ", ["ALL"] + clusters)
turn_min, turn_max = st.slider("ターン範囲", 0, df.shape[1], (0, df.shape[1]))
vmin, vmax = st.slider("レンジ", 0.3, 1.0, (0.4, 0.9))

data = df if sel_cluster == "ALL" else df.loc[[sel_cluster]]
data = data.iloc[:, turn_min:turn_max]

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(data, vmin=vmin, vmax=vmax, cmap="plasma", ax=ax, cbar=False)
if show_thresh:
    ax.axhline(0.5, ls="--", lw=1, color="white")

st.pyplot(fig)
```

Sidebar UI でクラスタ切替と閾値表示 On/Off をワンタップ操作

st.experimental_memo でキャッシュすれば再描画は 0.2 秒以下

st.dataframe(df.describe().T) を追加すればリアルタイムのエネルギー統計も確認可能


---

## grv ベースの異常アラート条件

実運用では「連続性」を重視します。
次のロジックでは 3ターン以上連続して grv が跳ね上がり、かつ文体変化が同相で増幅した場合にのみアラートを発火します。

```pytho
from scipy import ndimage
from collections import Counter
import numpy as np

spike = df_grv > (df_grv.mean() + 2 * df_grv.std())
label, num = ndimage.label(spike)
long_spike = np.isin(label, [i for i, c in Counter(label).items() if c >= 3])
alert = long_spike & (df_dstyle > 0.6)
```
#### 図表2：grv 異常エリア強調ヒートマップ（閾値超過＋文体変化）

![図表2: grv異常エリア強調ヒートマップ](/images/day8-grv_alert_heatmap-fig2.png)

- アラート発火ターンを赤枠で囲み  
- Slack には `session_id`, `turn`, `cluster`, `grv_value` を JSON で通知

---

## Grafana連携による運用監視への展開

1. Prometheus Exporter
```python
curl -XPOST http://localhost:9091/metrics/job/grv \
  -d "grv{cluster=\"noun\"} 0.62"
```
2. Grafana パネル設定ポイント

#### 図表3：Grafana ダッシュボードでの grv・ΔE・PoR 監視例

![図表3: grvダッシュボード構成](/images/day8-grafana_dashboard-fig3.png)

- Heatmap パネル：X(bucket)=turn, Y(bucket)=cluster, カラースケール＝plasma  
- Highlight Outliers＝ON、Transform → Group By で 5min 平均を可視化  
- PoRスパイク（赤点）と grv の空間圧分布が並列可視化され、  
  Slack/PagerDuty への連携も `max_over_time()` により簡易に実現


Heatmap パネル：X(bucket)=turn, Y(bucket)=cluster, カラースケール＝plasma

Highlight Outliers＝ON、Transform → Group By で 5min 平均を可視化

PoRスパイク（赤点）と grv の空間圧分布が並列可視化され、
Slack/PagerDuty への連携も max_over_time() により簡易に実現


---

## 導入から得られた気づき

grv は PoR よりも空間圧が可視化されやすく、逸脱の“場”を把握しやすい

ヒートマップは「意味のトレイル」としてログ後追い分析にも有効

PoR や ΔE と異なり、grv はモデル個性や語彙傾向により差異が大きいため、UI 上での閾値チューニング支援が極めて重要



---

## まとめ & Day 9 への布石

本稿では grv をヒートマップとして可視化し、逸脱が“どこに蓄積したか”を構造的に追えるようになりました。
アラート条件の導入により、**監視対象セッションの「文体崩壊前の圧縮ポイント」**も把握可能です。

次回 Day 9 では、OSS LLM や商用 API モデルにこの仕組みを適用し、汎用性と実装容易性の検証へ進みます。

#AI安全性 #PoR #grv可視化 #LLM監視 #生成AI

---

