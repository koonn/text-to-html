class Handler:
    """スーパークラスHandler

    Parserからのメソッド呼び出しを処理するオブジェクト

    Parserは各ブロックの開始時点で、ブロックに応じた名前を引数として、start()とend()を呼び出す。subメソッドは正規表現の置換に使われる。
    'emphasis'などの名前を引数として呼び出されると、それに応じた置換関数を返す。
    """
    def callback(self, prefix, name, *args):
        """接頭辞と名前を受け取って、適切なメソッドを見つけるためのメソッド

        Args:
            prefix(str): 接頭辞
            name(str):
            *args: 可変長引数リスト

        Returns:

        """
        # 'prefix + name'の名前の属性オブジェクトをgetattrで呼び出す
        # 指名された属性が存在しない場合にAttributeErrorではなくNoneを返すようにdefault引数に指定
        method = getattr(self, prefix + name, None)

        # 取り出したmethodオブジェクトが呼び出し可能なら、それを呼び出して、残りの引数を全て渡す。
        if callable(method):
            return method(*args)

    def start(self, name):
        """
        接頭辞'start_'を引数としてcallbackメソッドを呼び出すヘルパーメソッド
        """
        self.callback('start_', name)

    def end(self, name):
        """
        接頭辞'end_'を引数としてcallbackメソッドを呼び出すヘルパーメソッド
        """
        self.callback('end_', name)

    def sub(self, name):
        """新しい関数を返すメソッド

        substitution関数は、re.subのなかで置換関数として使われる
        """
        def substitution(match):
            """置換関数"""
            result = self.callback('sub_', name, match)

            # 置換関数が見つからない場合は、元の一致文字列を返す
            if result is None:
                match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    """
    HTMLのレンダリング用ハンドラ
    HTMLRendererのメソッドはスーパークラスを通じて利用する。
    ハンドラのメソッドstart()、end()、sub()は、HTML文書で
    使われる基本的なマークアップを行う。
    """
    @staticmethod
    def start_document():
        print('<html>')
        print('<head>')
        print('<title>...</title>')
        print('<meta http-equiv="content-type" charset="utf-8">')
        print('</head>')
        print('<body>')

    @staticmethod
    def end_document():
        print('</body></html>')

    @staticmethod
    def start_paragraph():
        print('<p>')

    @staticmethod
    def end_paragraph():
        print('</p>')

    @staticmethod
    def start_heading():
        print('<h2>')

    @staticmethod
    def end_heading():
        print('</h2>')

    @staticmethod
    def start_list():
        print('<ul>')

    @staticmethod
    def end_list():
        print('</ul>')

    @staticmethod
    def start_listitem():
        print('<li>')

    @staticmethod
    def end_listitem():
        print('</li>')

    @staticmethod
    def start_title():
        print('<h1>')

    @staticmethod
    def end_title():
        print('</h1>')

    @staticmethod
    def sub_emphasis(match):
        return f'<span style="font-weight: bold;">{match.group(1)}</span>'

    @staticmethod
    def sub_url(match):
        return f'<a href="{match.group(1)}">{match.group(1)}</a>'

    @staticmethod
    def sub_mail(match):
        return f'<a href="mailto:{match.group(1)}">{match.group(1)}</a>'

    @staticmethod
    def feed(data):
        print(data)
