
利用想定
- any_repo
    - any_src
    - *anydocgen(this repo)
        - docs
        - prompts
        - refs
            - materials
        - utils

any_src内のソースコードをdocs内にmdでドキュメント化する

refs/materialsにあるpdfをOCRしてrefs/buildに生成したあと，
mdで見やすい形に整形する．

Readmeに書く手順
1. clone
2. refs/materialsに参考資料入れる
3. promptsから目的にあったプロンプトを選んでconsole.mdとする
    - promptsにはbuildの記法を参照してsrcの内容のdocs作って等が書いてある
4. buildする
    - ビルドにはOCR, 整形, document化が含まれる．