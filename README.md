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
import anydocgen/prompts/core.md
# anydocgen/prompts/core.mdの内容を把握してから実行すること
Build
(
target_code: ドキュメント化するコード部分
docgen_prompt: ドキュメント化についてのprompt
reference_content: 参考にするファイル
mistralai_api_key: mistralaiのAPIキー
)
```
ex. 
```bash
import anydocgen/prompts/core.md
# anydocgen/prompts/core.mdの内容を把握してから実行すること
Build
(
target_code: lacam/src/local_guide.cpp
docgen_prompt: local_guideについてのアルゴリズムを数学的に定式化して疑似コードにしてください．記法は20250508_local-guidance.pdfを参考にしてください．
reference_content: refs/materials/20250508_local-guidance.pdf
mistralai_api_key: 0pdZKpjodsEYZzTtGlNakWjReMz60ZCsr
)
```

### 4. ビューワ起動

本レポジトリは[Obsidian](https://obsidian.md/)での可視化を想定．(マークダウン表示可能であれば他ツールでも良い)