import mock
import platform

import unittest

from neo_haxor_news.haxor import Haxor


class HaxorTest(unittest.TestCase):
    def setUp(self):
        self.haxor = Haxor()

    def test_add_comment_pagination(self):
        text = "hn view 1"
        result = self.haxor._add_comment_pagination(text)
        assert result == text
        text = "hn view 1 -c"
        result = self.haxor._add_comment_pagination(text)
        if platform.system() == "Windows":
            assert result == text + self.haxor.PAGINATE_CMD_WIN
        else:
            assert result == text + self.haxor.PAGINATE_CMD
        text = "hn view 1 -c -b"
        result = self.haxor._add_comment_pagination(text)
        assert result == text

    @mock.patch("haxor_news.haxor.subprocess.call")
    def test_run_command(self, mock_subprocess_call):
        document = mock.Mock()
        document.text = "hn view 1 -c"
        self.haxor.run_command(document)
        mock_subprocess_call.assert_called_with("hn view 1 -c | less -r", shell=True)
        document.text = "hn view 1"
        self.haxor.run_command(document)
        mock_subprocess_call.assert_called_with("hn view 1", shell=True)

    @mock.patch("haxor_news.haxor.sys.exit")
    def test_exit_command(self, mock_sys_exit):
        document = mock.Mock()
        document.text = "exit"
        self.haxor.handle_exit(document)
        mock_sys_exit.assert_called_with()
