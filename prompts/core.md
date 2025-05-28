# Build Command Prompt

def Build

argument:
target_code: ドキュメント化するコード部分
docgen_prompt: ドキュメント化についてのprompt
reference_content: 参考にするファイル
mistralai_api_key: mistralaiのAPIキー

**呼び出しに上記の引数が不足している場合は満たされるまで実行せず要求すること．**

以下の手順に従って、ソースコードのドキュメント化を行ってください。

## 実行するbuildコマンド

以下の処理を順次実行してください：

### 1. PDF参考資料のOCR処理

`anydocgen/utils/.env`を作成してapiキーを登録
```
MISTRALAI_API_KEY={mistralai_api_key}
```

以下スクリプトを使用して、`anydocgen/refs/materials/`内のPDFファイルをすべてMarkdown化

```bash
./anydocgen/utils/process_pdfs.sh
```

このスクリプトは以下を自動実行します：
- Python仮想環境の作成・アクティベート
- 必要なパッケージ（mistralai, python-dotenv）のインストール
- `anydocgen/refs/materials/`内のすべてのPDFファイルのOCR処理
- 結果を`anydocgen/refs/build/`ディレクトリに`{ファイル名}_ocr_result.md`として保存

<!-- 現在は不要
### 2. OCR結果の整形

`anydocgen/refs/build/`に生成されたMarkdownファイルを読み込み、以下の整形処理を行ってください：

- 不要な改行や空白の除去
- セクション見出しの統一（# ## ### の階層構造）
- 表やリストの整形
- 図表キャプションの整理
- 目次の生成

整形されたファイルは同じく`anydocgen/refs/build/`に`{ファイル名}_formatted.md`として保存してください。 -->

### 3. ソースコードの解析

`{target_code}`ディレクトリ内のソースコードを解析し、以下の情報を抽出してください：

- ファイル構造とディレクトリ階層
- 各ファイルの概要と役割
- 関数・クラス・メソッドの定義と説明
- 依存関係とインポート構造
- 主要なアルゴリズムやロジック

### 4. 統合ドキュメントの生成

{docgen_prompt}を目的として，ソースコードのドキュメントを作成します．ドキュメント内の全オブジェクトはソースコード内の具体的な実装との対応関係を示したうえで重厚かつ可読性の高いドキュメントを作成して下さい．
記法については，`{reference_content}`を参考にすること．

## 期待される最終成果物

このbuildコマンドの実行により、以下が完成することを期待します：

- `anydocgen/refs/build/`: OCR処理・整形済みの参考資料
- `anydocgen/docs/~.md`: 目的のドキュメント

これらのドキュメントにより、ソースコードの理解と利用が容易になることを目指してください。
