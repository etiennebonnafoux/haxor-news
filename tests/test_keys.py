import unittest
from prompt_toolkit.input.defaults import create_pipe_input

from neo_haxor_news.haxor import Haxor


class KeysTest(unittest.TestCase):
    def setUp(self):
        self.haxor = Haxor()
        self.pipe_input = create_pipe_input()

        self.haxor.session.app.input = self.pipe_input

    def tearDown(self):
        self.pipe_input.close()

    def test_F2(self):
        orig_paginate = self.haxor.paginate_comments

        self.pipe_input.send_text("\x1b[12~")

        self.haxor.session.app.run_async(sleep=0)

        self.assertNotEqual(orig_paginate, self.haxor.paginate_comments)

    def test_F10(self):
        with self.assertRaises(EOFError):
            self.pipe_input.send_text("\x1b[21~")

            self.haxor.session.app.run_async(sleep=0)
