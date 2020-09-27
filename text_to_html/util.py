# -*- coding: utf-8 -*-
"""ユーティリティモジュール"""


def lines(file):
    """ファイルの最後に空行を付加するユーティリティ

    Args:
        file():　

    Returns:
        generator: fileの中身を順番に返し、最後に\nを返すジェネレータ
    """
    for line in file:
        yield line
    yield '\n'


def blocks(file):
    """

    """
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
