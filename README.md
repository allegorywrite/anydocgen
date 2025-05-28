# AnyDocGen

any_src内のソースコードをdocs内にmdでドキュメント化するツール

## 想定プロジェクト構造

```
any_repo/
├── any_src/                 # ソースコード
├── anydocgen/              # このリポジトリ
│   ├── docs/               # 生成されたドキュメント
│   ├── prompts/            # プロンプトテンプレート
│   ├── refs/               # 参考資料
│   │   ├── materials/      # 元のPDFファイル
│   │   └── build/          # OCR処理済みMarkdown
│   └── utils/              # ユーティリティスクリプト
```

## 前提

- [Obsidian](https://obsidian.md/)(マークダウン表示可能であれば他ツールでも良い)
- [mistralAI](https://mistral.ai/)からAPIキーを取得

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/allegorywrite/anydocgen.git
```

### 2. 参考資料の配置

```bash
# PDFファイルをrefs/materialsに配置
cp your_reference.pdf anydocgen/refs/materials/
```

### 3. ドキュメント生成

コマンド実行可能なCoding Agentを立ち上げて以下を入力
```bash
import anydocgen/prompts/improved.md
# anydocgen/prompts/improved.mdの内容を把握してから実行すること
Build \
  --target_code ドキュメント化するコードベースのパス \
  --docgen_prompt ドキュメントのねらい・想定読者・利用シーン \
  --reference_content スタイルや記法の例として参照するPDF \
  --mistralai_api_key MistralAI の API キー \
  --output_mode "single" | "multi"
```
ex. 
```bash
import anydocgen/prompts/improved.md
# anydocgen/prompts/improved.mdの内容を把握してから実行すること
Build \
  --target_code glim_ros2, glim, glim_ext \
  --docgen_prompt GLIMについてのアルゴリズムを数学的に定式化してドキュメントにしてください．記法はanydocgen/refs/materials/2407.10344v1.pdfを参考にしてください． \
  --reference_content anydocgen/refs/materials/2407.10344v1.pdf \
  --mistralai_api_key 0pdZKpjodsEYZzTtGlNakWjReMz60ZCsr \
  --output_mode "multi"
```

### 4. ビューワ起動

[Obsidian](https://obsidian.md/)でanydocgenディレクトリを開く