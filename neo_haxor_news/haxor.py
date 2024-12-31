import os
import platform
import subprocess
import sys

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.application import Application
from prompt_toolkit.filters import Always
from prompt_toolkit import layout
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from neo_haxor_news.__init__ import __version__
from neo_haxor_news.completer import Completer
from neo_haxor_news.hacker_news_cli import HackerNewsCli
from neo_haxor_news.keys import KeyManager
from neo_haxor_news.style import StyleFactory
from neo_haxor_news.utils import TextUtils


class Haxor:
    """Encapsulate the Hacker News CLI.

    :type cli: :class:`prompt_toolkit.CommandLineInterface`
    :param cli: An instance of `prompt_toolkit.CommandLineInterface`.

    :type CMDS_ENABLE_PAGINATE: list (const)
    :param CMDS_ENABLE_PAGINATE: A list of commands that kick off pagination.

    :type CMDS_NO_PAGINATE: list (const)
    :param CMDS_NO_PAGINATE: A list of commands that disable pagination.

    :type completer: :class:`prompt_toolkit.completer`
    :param completer: An instance of `prompt_toolkit.completer`.

    :type hacker_news_cli: :class:`hacker_news_cli.HackerNewsCli`
    :param hacker_news_cli: An instance of `hacker_news_cli.HackerNewsCli`.

    :type key_manager: :class:`prompt_toolkit.key_binding.manager.
        KeyBindingManager`
    :param key_manager: An instance of `prompt_toolkit.key_binding.manager.
        KeyBindingManager`.

    :type PAGINATE_CMD: str (const)
    :param PAGINATE_CMD: The command to enable pagination.

    :type paginate_comments: bool
    :param paginate_comments: Determines whether to paginate
            comments.

    :type text_utils: :class:`util.TextUtils`
    :param text_utils: An instance of `util.TextUtils`.

    :type theme: str
    :param theme: The prompt_toolkit lexer theme.
    """

    CMDS_NO_PAGINATE = [
        "-b",
        "--browser",
        ">",
        "<",
    ]
    CMDS_ENABLE_PAGINATE = [
        "-cq",
        "--comments_regex_query",
        "-c",
        "--comments",
        "-cr",
        "--comments_recent",
        "-cu",
        "--comments_unseen",
        "-ch",
        "--comments_hide_non_matching",
        "hiring",
        "freelance",
    ]
    PAGINATE_CMD = " | less -r"
    PAGINATE_CMD_WIN = " | more"

    def __init__(self):
        self.cli = None
        self.key_manager = None
        self.theme = "vim"
        self.paginate_comments = True
        self.hacker_news_cli = HackerNewsCli()
        self.text_utils = TextUtils()
        self.completer = Completer(fuzzy_match=False, text_utils=self.text_utils)
        self._create_cli()
        if platform.system() == "Windows":
            self.CMDS_ENABLE_PAGINATE.append("view")

    def _create_key_manager(self):
        """Create the :class:`KeyManager`.

        The inputs to KeyManager are expected to be callable, so we can't
        use the standard @property and @attrib.setter for these attributes.
        Lambdas cannot contain assignments so we're forced to define setters.

        :rtype: :class:`prompt_toolkit.key_binding.manager
        :return: KeyBindingManager with callables to set the toolbar options.
        """

        def set_paginate_comments(paginate_comments):
            """Setter for paginating comments mode.

            :type paginate: bool
            :param paginate: The paginate comments mode.
            """
            self.paginate_comments = paginate_comments

        return KeyManager(set_paginate_comments, lambda: self.paginate_comments)

    def _create_cli(self):
        """Create the prompt_toolkit session and application."""
        history = FileHistory(os.path.expanduser("~/.haxornewshistory"))

        kb = self._create_key_manager()

        def get_bottom_toolbar():
            return f"{'Paginate comments: ON' if self.paginate_comments else 'Paginate comments: OFF'}"

        my_layout = Layout(
            Window(
                height=1,
                content=layout.FormattedTextControl("haxor> "),
            )
        )

        style_factory = StyleFactory(self.theme)
        self.app = Application(
            layout=my_layout,
            full_screen=True,
            key_bindings=kb,
            style=style_factory.style,
            mouse_support=False,
        )

        self.session = PromptSession(
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
            completer=self.completer,
            complete_while_typing=Always(),
            key_bindings=kb,
            style=style_factory.style,
            bottom_toolbar=get_bottom_toolbar,
            message="haxor> ",
        )

        self.cli = self.session

    def _add_comment_pagination(self, document_text):
        """Add the command to enable comment pagination where applicable.

        Pagination is enabled if the command views comments and the
        browser flag is not enabled.

        :type document_text: str
        :param document_text: The input command.

        :rtype: str
        :return: the input command with pagination enabled.
        """
        if not any(sub in document_text for sub in self.CMDS_NO_PAGINATE):
            if any(sub in document_text for sub in self.CMDS_ENABLE_PAGINATE):
                if platform.system() == "Windows":
                    document_text += self.PAGINATE_CMD_WIN
                else:
                    document_text += self.PAGINATE_CMD
        return document_text

    def handle_exit(self, document):
        """Exits if the user typed exit or quit

        :type document: :class:`prompt_toolkit.document.Document`
        :param document: An instance of `prompt_toolkit.document.Document`.
        """
        if document.text in ("exit", "quit"):
            sys.exit()

    def run_command(self, document):
        """Run the given command.

        :type document: :class:`prompt_toolkit.document.Document`
        :param document: An instance of `prompt_toolkit.document.Document`.
        """
        try:
            if self.paginate_comments:
                text = document.text
                text = self._add_comment_pagination(text)
            subprocess.call(text, shell=True)
        except Exception as e:
            click.secho(e, fg="red")

    def run_cli(self):
        """Run the main loop."""
        click.echo("Version: " + __version__)
        click.echo("Syntax: hn <command> [params] [options]")
        while True:
            document = self.cli.prompt()
            self.handle_exit(document)
            self.run_command(document)
