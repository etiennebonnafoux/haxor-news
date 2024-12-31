import unittest

from pygments.token import Token

from neo_haxor_news.haxor import Haxor
from neo_haxor_news.toolbar import Toolbar


class ToolbarTest(unittest.TestCase):
    def setUp(self):
        self.haxor = Haxor()
        self.toolbar = Toolbar(lambda: self.haxor.paginate_comments)

    def test_toolbar_on(self):
        self.haxor.paginate_comments = True
        expected = [
            # (Token.Toolbar.On,
            #  ' [F2] Paginate Comments: {0} '.format('ON')),
            (Token.Toolbar, " [F10] Exit ")
        ]
        assert expected == self.toolbar.handler(None)

    def test_toolbar_off(self):
        self.haxor.paginate_comments = False
        expected = [
            # (Token.Toolbar.Off,
            #  ' [F2] Paginate Comments: {0} '.format('OFF')),
            (Token.Toolbar, " [F10] Exit ")
        ]
        assert expected == self.toolbar.handler(None)
