class Rule:
    """すべてのルールの基底クラス

    全てのサブクラスがtypeという属性を持ち、文字列でタイプ名を格納している前提
    """
    def action(self, block, handler):
        """ブロックの変換処理を定義する関数"""
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        # 他のルールは試す必要がないのでTrueを返す
        return True


class HeadingRule(Rule):
    """
    見出しとは、最長70文字で、最後の文字が「:」でも「.」でも「。」でもない単一の行。
    """
    # テキストブロックのtypeを定義
    type = 'heading'

    def condition(self, block):
        """ブロックが'見出し'の定義に合致しているかを定義する関数

        Args:
            block: テキストブロック

        Returns:
            boolean: そのブロックが'見出し'であるか否かのTrue/False
        """
        # 見出しの条件
        is_heading = (
            '\n' not in block
            and len(block) <= 70
            and not (block[-1] == ':'
                     or block[-1] == '.'
                     or block[-1] == '。')
        )

        return is_heading


class TitleRule(HeadingRule):
    """
    タイトルとは、文書の最初のブロックで、かつ見出しであるもの。
    """
    # テキストブロックのtypeを定義
    type = 'title'
    first = True

    def condition(self, block):
        """ブロックが'タイトル'の定義に合致しているかを定義する関数

        Args:
            block: テキストブロック

        Returns:
            boolean: そのブロックが'タイトル'であるか否かのTrue/False
        """
        # タイトルの条件
        # 文章の最初のブロックかどうかを判定(最初のブロックでなければFalseを返す)
        if not self.first:
            return False

        # 最初のブロック以外は文章の最初のブロックかどうかの判定で弾くようにfirstをFalseにする
        self.first = False

        # 最初のブロックなら、ヘッダかどうかを判定
        is_header = HeadingRule.condition(self, block)

        return is_header


class ListItemRule(Rule):
    """
    リスト項目とは、「-」で始まるブロック。
    書式付け処理の一環として、「-」は削除する。
    """
    # テキストブロックのtypeを定義
    type = 'listitem'

    def condition(self, block):
        """ブロックが'リスト項目'の定義に合致しているかを定義する関数

        Args:
            block: テキストブロック

        Returns:
            boolean: そのブロックが'リスト項目'であるか否かのTrue/False
        """
        # リスト項目の条件
        is_listitem = (block[0] == '-')

        return is_listitem

    def action(self, block, handler):
        """
        'リスト項目'ブロックの変換処理を定義する関数
        """
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True


class ListRule(ListItemRule):
    """
    リストは、リスト項目ではないブロックとリスト項目の間から始まり、
    連続したリスト項目の最後のものが終わるところまで。
    """
    # テキストブロックのtypeを定義
    type = 'list'
    inside = False

    def condition(self, block):
        """ブロックが'リスト'の定義に合致しているかを定義する関数

        Args:
            block: テキストブロック

        Returns:
            boolean: そのブロックが'リスト'であるか否かのTrue/False
        """
        # リストの条件
        is_list = True

        return is_list

    def action(self, block, handler):
        """
        'リスト'ブロックの変換処理を定義する関数
        """
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False


class ParagraphRule(Rule):
    """
    パラグラフとは単に他のどのルールにも当てはまらないブロック。
    """
    # テキストブロックのtypeを定義
    type = 'paragraph'

    @staticmethod
    def condition(block):
        """ブロックが'パラグラフ'の定義に合致しているかを定義する関数

        Args:
            block: テキストブロック

        Returns:
            boolean: そのブロックが'パラグラフ'であるか否かのTrue/False
        """
        # パラグラフの条件
        is_paragraph = True

        return is_paragraph
