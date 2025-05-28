# Build Command Prompt (Revised – “DeepDoc Edition”)

def Build

argument:
  target_code:        ドキュメント化するコードベースのパス
  docgen_prompt:      ドキュメントのねらい・想定読者・利用シーン
  reference_content:  スタイルや記法の例として参照するPDF
  mistralai_api_key:  MistralAI の API キー
  output_mode:        "single" | "multi"        # 追加 ― 省略時は "multi"

# --- 必須引数検証 ---
**上記4+1 引数のうち必須4項 (output_mode は任意) が欠けている場合は実行せず、欠落を提示して再入力を要求すること。**

## パイプライン

呼び出された際は以下の処理を順次実行してください

### 1. 参考資料のOCR
1.1 `.env` 生成  
```bash
echo "MISTRALAI_API_KEY={mistralai_api_key}" > anydocgen/utils/.env
````

1.2 OCR 実行

```bash
./anydocgen/utils/process_pdfs.sh
```

> 生成先: `anydocgen/refs/build/{file}_ocr_result.md`

### 2. 静的解析 & メトリクス収集

対象: `{target_code}`
取得すべきデータ（最低限）

* **ファイル/ディレクトリ階層ツリー**
* **依存グラフ**（import, include, require 解析）
* **コールグラフ**（関数・メソッド呼出し関係）
* **複雑度指標**（CC, NCLOC, fan-in/out 等）
* **変更履歴**（Git log から最新50コミットを要約）
* **外部ライブラリ一覧**（バージョン含む）

### 3. コードオブジェクト抽出

各ファイルごとに以下を抽出・整形:

| 要素          | 抽出内容             |
| ----------- | ---------------- |
| モジュール/パッケージ | 目的・公開 API        |
| クラス         | 継承関係・フィールド・責務    |
| 関数/メソッド     | シグネチャ・説明・戻り値・副作用 |
| 重要定数 / Enum | 意味と利用箇所          |
| 例外          | 発生条件・呼び出し元       |

> すべてに **ソース位置 (ファイル:行)** を付与すること。

### 4. 統合ドキュメント生成
`output_mode` に応じて **以下 2 つのレイアウト戦略** を取る。  

| output_mode | 生成物 | 目的 |
|-------------|---------|------|
| `"single"`  | `anydocgen/docs/deepdoc.md` | 一括閲覧・印刷用途 |
| `"multi"` *(default)* | `anydocgen/docs/` 配下に **章単位** または **モジュール単位** で複数 `.md` を生成し、トップレベルに `README.md` (目次) を置く | 巨大コードベースや変更頻度が高いプロジェクトでの差分管理・並列編集に最適 |

#### “multi” 生成規約
1. **章レベル分割**  
   - 章 1 ～ 3 を `00_Overview/`, 章 4 以降を `01_Detail/` など、  
     *ディレクトリ＋ファイル名プリフィクス “XX_”* でソート順を保持。  
2. **サブシステム分割**（モノレポなど）  
   - `pkg_<package名>/doc/` にパッケージ固有ドキュメントを配置。  
3. **共通資産**  
   - 図・PlantUML ソース・Mermaid ファイルは `assets/` 以下に集約。  
4. **リンク**  
   - 相対パス `./01_Detail/04_API_Reference.md` のように書き、CI でリンク切れチェックを行う。  
5. **自動 TOC**  
   - ルート `README.md` は章立てだけでなく **各ファイルの更新日・行数** を表形式で列挙。  

> **選択基準**  
> *行数が 800 行超* または *クラス/関数数が 300 を超える* モノリス的プロジェクトは “multi” を推奨し、自動判定でも “multi” を採用する。  

#### 章立て & 最低ボリューム
（前回提示と同一：Executive Summary ≥40行 … Appendices まで）

### 5. 品質チェックリスト
- “single” / “multi” どちらでも **最低行数と章網羅** を満たすこと  
- “multi” の場合:  
  - `README.md` が存在し、すべての章ファイルへリンクしている  
  - 図・コードリンクの相対パスが正しい  
  - GitHub Action 等で `markdown-link-check` をパス  


## 成果物

```
anydocgen/
    ├─ refs/
    │   └─ build/ # OCR & 整形済み資料
    └─ docs/
    ├─ README.md # 目次 & 概要
    ├─ 00_Overview/
    │   ├─ 01_Executive_Summary.md
    │   └─ 02_Architecture_Overview.md
    ├─ 01_Detail/
    │   ├─ 03_Module_Reference.md
    │   └─ 04_API_Reference.md
    └─ assets/
    ├─ diagrams/
    └─ images/
> `output_mode="single"` の場合は `docs/deepdoc.md` のみ生成。
```

```bash
Build \
  --target_code ./my_project \
  --docgen_prompt "オンボーディング用ドキュメントを生成" \
  --reference_content ./style_guide.md \
  --mistralai_api_key $MISTRAL_KEY \
  --output_mode multi
```