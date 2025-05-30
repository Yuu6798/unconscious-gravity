cat <<EOF > PoR_heuristics_v1.md
# PoR 判定ヒューリスティクス v1

本ドキュメントでは、PoR (Point of Risk) 判定を行う際のヒューリスティクス v1 について説明します。

## 1. 背景
対話ログを解析し、不適切と思われる箇所を早期検出・フラグ付けするための初期的な手法を定義します。

## 2. ヒューリスティクス概要
- \`cosine_shift > 0.35\` **または** 応答文中にトークン \`[Q]\` が含まれている場合、**\`PoR_flag = 1\`** とする。
- 強度スコア **\`intensity\`** は下記の式により算出する。

\[
  \text{intensity} = \sigma(\text{cosine_shift}) 
  \quad \text{（ただし } \sigma \text{ はシグモイド関数）}
\]

ここで、
- **\`cosine_shift\`**: 連続する2ターン（あるいはユーザ発話とシステム応答）の埋め込みベクトル同士を比較し、類似度変化を測る値。  
- **シグモイド関数**:  
\[
  \sigma(x) = \frac{1}{1 + e^{-x}}
\]

## 3. 入出力とプロセス概要
1. **入力**: 連続する対話ログペア、もしくは埋め込みベクトルから算出した \`cosine_shift\` 値、およびテキスト情報。  
2. **出力**: 各ターン(行)に対して  
   - \`PoR_flag\` (0/1)  
   - \`intensity\` (0〜1 の値)

## 4. 運用上の注意点
- \`cosine_shift\` の閾値 \`0.35\` は暫定値です。モデルや用途により適切に調整してください。  
- \`[Q]\` トークンが含まれるかどうかの判定は非常に単純な文字列マッチングであるため、誤検出や見逃しもあり得ます。

## 5. 改善ポイント
- 閾値やシグモイド関数による単純実装なので、精度向上のためにはニューラルネットなど別のモデルを比較検証する余地があります。
- ユーザ発話の時系列情報や追加の特徴量を取り入れるなど、さらなる拡張性が考えられます。

EOF