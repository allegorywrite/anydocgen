#!/bin/bash

# PDFをOCRでMarkdown化するスクリプト
# 使用方法: ./utils/process_pdfs.sh

set -e  # エラーが発生したら停止

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# ディレクトリパス
MATERIALS_DIR="$PROJECT_ROOT/refs/materials"
BUILD_DIR="$PROJECT_ROOT/refs/build"
VENV_DIR="$PROJECT_ROOT/venv"
UTILS_DIR="$PROJECT_ROOT/utils"

echo "=== PDF OCR処理スクリプト ==="
echo "プロジェクトルート: $PROJECT_ROOT"
echo "材料ディレクトリ: $MATERIALS_DIR"
echo "出力ディレクトリ: $BUILD_DIR"

# 必要なディレクトリを作成
mkdir -p "$BUILD_DIR"

# Python仮想環境の作成・アクティベート
if [ ! -d "$VENV_DIR" ]; then
    echo "Python仮想環境を作成しています..."
    python3 -m venv "$VENV_DIR"
fi

echo "仮想環境をアクティベートしています..."
source "$VENV_DIR/bin/activate"

# 必要なパッケージのインストール
echo "必要なパッケージをインストールしています..."
pip install --upgrade pip
pip install mistralai python-dotenv

# .envファイルの確認
ENV_FILE="$UTILS_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "警告: $ENV_FILE が見つかりません。"
    echo "MISTRALAI_API_KEYを設定してください。"
    echo "例: echo 'MISTRALAI_API_KEY=your_api_key_here' > $ENV_FILE"
    exit 1
fi

# PDFファイルの処理
PDF_COUNT=0
PROCESSED_COUNT=0

echo "PDFファイルを検索しています..."
if [ ! -d "$MATERIALS_DIR" ]; then
    echo "エラー: $MATERIALS_DIR が存在しません。"
    exit 1
fi

# PDFファイルを検索して処理
for pdf_file in "$MATERIALS_DIR"/*.pdf; do
    if [ -f "$pdf_file" ]; then
        PDF_COUNT=$((PDF_COUNT + 1))
        echo ""
        echo "=== PDFファイル $PDF_COUNT を処理中 ==="
        echo "ファイル: $(basename "$pdf_file")"
        
        # OCR処理を実行
        if python3 "$UTILS_DIR/run_mistral_ocr.py" "$pdf_file" "$BUILD_DIR"; then
            PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
            echo "✓ 処理完了: $(basename "$pdf_file")"
        else
            echo "✗ 処理失敗: $(basename "$pdf_file")"
        fi
    fi
done

# 結果の表示
echo ""
echo "=== 処理結果 ==="
if [ $PDF_COUNT -eq 0 ]; then
    echo "PDFファイルが見つかりませんでした。"
    echo "$MATERIALS_DIR にPDFファイルを配置してください。"
else
    echo "総PDFファイル数: $PDF_COUNT"
    echo "処理成功数: $PROCESSED_COUNT"
    echo "処理失敗数: $((PDF_COUNT - PROCESSED_COUNT))"
    
    if [ $PROCESSED_COUNT -gt 0 ]; then
        echo ""
        echo "生成されたMarkdownファイル:"
        ls -la "$BUILD_DIR"/*.md 2>/dev/null || echo "Markdownファイルが見つかりません。"
    fi
fi

echo ""
echo "処理が完了しました。" 