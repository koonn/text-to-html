import re
import sys
from handlers import *
from rules import *
from util import *


class Parser:
    """
    Parserはテキストファイルを読み、ルールの適用とハンドラの制御を行う。
    """
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        """
        ルールリストにルールを追加する関数
        """
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        """
        フィルタを作成して、フィルタをフィルタリストに追加する関数
        """
        def filter_(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter_)

    def parse(self, file):
        """
        文章のパースを実行する関数
        """
        self.handler.start('document')
        for block in blocks(file):
            for filter_ in self.filters:
                block = filter_(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    # rule.actionはboolを返す。このブール値で、そのブロックに対するルールの適用を終了するかどうかを示す
                    is_last = rule.action(block, self.handler)
                    if is_last:
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    コンストラクタ内でルールとフィルタを追加する特定目的のParser
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.add_rule(ListRule())
        self.add_rule(ListItemRule())
        self.add_rule(TitleRule())
        self.add_rule(HeadingRule())
        self.add_rule(ParagraphRule())

        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(https://[\.a-zA-Z/]+)', 'url')
        self.add_filter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


if __name__ == '__main__':
    handler_ = HTMLRenderer()
    parser = BasicTextParser(handler_)

    parser.parse(sys.stdin)
