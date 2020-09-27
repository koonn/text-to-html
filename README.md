# text-to-html

「Python基礎&実践プログラミング」20章

## 基本実装版の機能の使い方

```shell script
python3 text_to_html/simple_markup.py < test_input.txt > test_output.html 
```

## 2回目の実装版の機能の使い方

```shell script
python3 text_to_html/markup.py < test_input.txt > test_output.html 
```

## TODO

モジュール化を進める

- パーサー
    - テキストを読み込むオブジェクトの追加
    - 他のクラスの管理
- ルール
    - ブロックの種類ごとに1つのルールを作る
    - 適用対象のブロックの種類を識別
    - それに対して書式を設定
- フィルタ
    - 正規表現をラップしたフィルタで、インライン要素を処理する
- ハンドラ
    - パーサがハンドラを使って出力を生成
    - 各ハンドラは種類の異なるマークアップを生成