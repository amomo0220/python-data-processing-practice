# python-data-processing-practice
はじめての技術選考（課題）を受ける前の練習

# 課題内容
## お題
「CSVファイルを読み込み、条件に合うデータを集計してJSONで出力する」

## 仕様
- 入力：CSV（例：標準入力 or ファイル）
- 各行には以下の列がある
    - user_id
    - amount（数値）
    - category
- やること：
1. category ごとに amount を合計
2. 合計が 1000 以上の category だけ残す
3. 結果を JSON で出力

## 制約
- Pythonのみ
- フレームワークなし（標準ライブラリOK）
- 実行はコマンド1つでできること

# 実装

## 実装方針
0. はじめる前のルール
    1. エラー出力には logging を使用する（``import logging``）
    2. 各関数に「何をしている関数か」コメントを加える
    3. 可読性の高いコードを意識する
1. コマンド``python main.py data/input.csv``で main.py を実行
    1. csv ファイルはヘッダ必須である
    2. もし data ディレクトリに csv ファイルが存在しない場合は、その旨を伝えるエラーを出力し終了する
    3. input.csvは、input001.csv という名前などに変わる場合もあるが、コマンドで指定されたcsvファイルを読み込むようにする（``python main.py data/input001.csv``の場合は input001.csv を読み込む）
2. input.csv の内容を1行ずつ読み込みながら、 category ごとに amount を合計する
    1. ただし、input.csv のはじめの行はヘッダなので合計の計算には使用しない。2行目以降が合計の対象となる。
3. 合計が 1000 以上の category だけを残す
    1. もし、1000 以上の category が無い場合は、その旨を、その旨を伝えるエラーを出力し終了する
4. 3.の結果を data/output.json に出力する
    1. data ディレクトリは既に存在するため作成不要。
        1. data ディレクトリ内に既に output.json が存在する場合は、上書きする（記載されている内容は削除し、今回の結果のみが記載されているようにする）
        2. data ディレクトリ内に output.json が存在しない場合は、新たに作成する
    2. category をキーに、amount の合計が値となるように出力する
    3. 出力先は data/output.json で固定とする