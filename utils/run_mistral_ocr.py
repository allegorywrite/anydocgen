#!/usr/bin/env python3
"""
Mistral OCRを使用してPDFを処理するスクリプト
"""

import sys
import os
import traceback
from pathlib import Path
import dotenv

# 環境変数の読み込み
dotenv.load_dotenv(Path(__file__).parent / '.env')

# Mistral APIキーの確認
api_key = os.getenv("MISTRALAI_API_KEY")
if not api_key:
    print("エラー: MISTRALAI_API_KEYが設定されていません。")
    sys.exit(1)

print(f"APIキー: {api_key[:5]}...{api_key[-5:]}")

try:
    from mistralai import Mistral, DocumentURLChunk
    print("Mistralクライアントをインポートしました。")
except ImportError as e:
    print(f"エラー: Mistralクライアントのインポートに失敗しました。{e}")
    sys.exit(1)

def process_pdf_with_mistral(pdf_path, output_dir=None):
    """
    Mistral OCRを使用してPDFを処理する
    
    Args:
        pdf_path (str or Path): PDFファイルのパス
        output_dir (str or Path, optional): 出力ディレクトリ
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"エラー: ファイルが見つかりません: {pdf_path}")
        return
    
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # 出力ファイル名
    json_file = output_dir / f"{pdf_path.stem}_ocr_result.json"
    markdown_file = output_dir / f"{pdf_path.stem}_ocr_result.md"
    
    try:
        # Mistralクライアントの作成
        print("Mistralクライアントを作成しています...")
        client = Mistral(api_key=api_key)
        print("Mistralクライアントを作成しました。")
        
        # PDFファイルをアップロード
        print(f"PDFファイルをアップロードしています: {pdf_path}")
        uploaded_file = client.files.upload(
            file={
                "file_name": pdf_path.stem,
                "content": pdf_path.read_bytes(),
            },
            purpose="ocr",
        )
        print(f"PDFファイルをアップロードしました: {uploaded_file.id}")
        
        # アップロードしたファイルに対して、署名付きURLを取得
        print("署名付きURLを取得しています...")
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
        print(f"署名付きURLを取得しました: {signed_url.url[:30]}...")
        
        # PDFファイルをOCR
        print("OCR処理を開始しています...")
        pdf_response = client.ocr.process(
            document=DocumentURLChunk(document_url=signed_url.url),
            model="mistral-ocr-latest",
            include_image_base64=False
        )
        print("OCR処理が完了しました。")
        
        # Markdown形式のテキストを生成
        print("Markdownを生成しています...")
        markdowns = []
        for page in pdf_response.pages:
            # 画像参照を削除
            markdown_str = page.markdown
            markdowns.append(markdown_str)
        
        markdown_string = "\n\n".join(markdowns)
        print("Markdownを生成しました。")
        
        # 結果を保存
        print(f"結果を保存しています: {markdown_file}")
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown_string)
        print(f"結果を保存しました: {markdown_file}")
        
        return markdown_string
        
    except Exception as e:
        print(f"エラー: {e}")
        print("詳細なエラー情報:")
        traceback.print_exc()
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法: python run_mistral_ocr.py <pdf_path> [output_dir]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_pdf_with_mistral(pdf_path, output_dir)

if __name__ == "__main__":
    main()
