#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 簡単なマークアップスクリプト"""
import sys
import re
from util import *

if __name__ == '__main__':
    # htmlのbodyを開く
    print('<html>')
    print('<head>')
    print('<title>...</title>')
    print('<meta http-equiv="content-type" charset="utf-8">')
    print('<body>')


    # 見出しをつけるための初期設定
    title = True

    # メイン処理
    for block in blocks(sys.stdin):
        # 「*」で囲まれたテキストは強調テキストに置き換える
        block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)

        # 1行目は、h1タグで見出しづけ
        if title:
            print('<h1>')
            print(block)
            print('</h1>')
            title = False
        # 2行目以降は、pタグで囲む
        else:
            print('<p>')
            print(block)
            print('</p>')

    # htmlを閉じる
    print('</body>')
    print('</html>')
