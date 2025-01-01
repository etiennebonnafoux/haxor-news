from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

from neo_haxor_news.completions import SUBCOMMANDS, ARGS_OPTS_LOOKUP
from neo_haxor_news.utils import TextUtils
from collections.abc import Iterable


class CustomCompleter(Completer):
    def __init__(self, fuzzy_match: bool, text_utils: TextUtils):
        """Completer for haxor-news.

        Args:
            fuzzy_match (bool): Determines whether to use fuzzy matching.
            text_utils (TextUtils): An instance of `utils.TextUtils`.
        """
        self.fuzzy_match = fuzzy_match
        self.text_utils = text_utils

    def _is_completing_command(self, words: list[str], word_before_cursor: str) -> bool:
        """Determine if we are currently completing the hn command.

        Args:
            words (list[str]): The input text broken into word tokens.
            word_before_cursor (str): The current word before the cursor,
            which might be one or more blank spaces.

        Returns:
            bool: Specifies whether we are currently completing the hn command.
        """

        return len(words) == 1 and word_before_cursor != ""

    def _is_completing_subcommand(
        self, words: list[str], word_before_cursor: str
    ) -> bool:
        """Determine if we are currently completing a subcommand.

        Args:
            words (list[str]): The input text broken into word tokens.
            word_before_cursor (str): The current word before the cursor,
            which might be one or more blank spaces.

        Returns:
            bool: Specifies whether we are currently completing a subcommand.
        """
        return (len(words) == 1 and word_before_cursor == "") or (
            len(words) == 2 and word_before_cursor != ""
        )

    def _is_completing_arg(self, words: list[str], word_before_cursor: str) -> bool:
        """Determine if we are currently completing an arg.
        Args:
            words (list[str]): The input text broken into word tokens.
            word_before_cursor (str): The current word before the cursor,
            which might be one or more blank spaces.

        Returns:
            bool: Specifies whether we are currently completing an arg.
        """
        return (len(words) == 2 and word_before_cursor == "") or (
            len(words) == 3 and word_before_cursor != ""
        )

    def _completing_subcommand_option(self, words: list[str]) -> list[str]:
        """Determine the current options.

        Args:
            words (list[str]): The input text broken into word tokens.

        Returns:
            list[str]: A list of options.
        """
        options: list[str] = []
        for subcommand in ARGS_OPTS_LOOKUP.keys():
            if subcommand in words and (
                words[-2] == subcommand
                or self._is_completing_subcommand_option_util(subcommand, words)
            ):
                options.extend(ARGS_OPTS_LOOKUP[subcommand].opts)
        return options

    def _is_completing_subcommand_option_util(
        self, option: str, words: list[str]
    ) -> bool:
        """Determine if we are currently completing an option.

        Called by completing_subcommand_option as a utility method.
        Example: Return True for: hn view 0 --comm

        Args:
            option (str): The subcommand in the elements of ARGS_OPTS_LOOKUP.
            words (list[str]): The input text broken into word tokens.

        Returns:
            bool: Specifies whether we are currently completing an option.
        """
        return len(words) > 3 and option in words

    def _arg_completions(self, words: list[str]) -> list[str]:
        """Generates arguments completions based on the input.

        Args:
            words (list[str]): The input text broken into word tokens.

        Returns:
            list[str]: A list of completions.
        """
        if "hn" not in words:
            return []
        for subcommand in ARGS_OPTS_LOOKUP.keys():
            if subcommand in words:
                return [ARGS_OPTS_LOOKUP[subcommand].args]
        return ["10"]

    def get_completions(self, document: Document, _) -> Iterable[Completion]:
        """Get completions for the current scope.

        Args:
            document (Document): An instance of `prompt_toolkit.Document`.
            _ (Any): Unused

        Returns:
            Iterable[Completion]: a list of `prompt_toolkit.completion.Completion`.
        """
        word_before_cursor: str = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands: list[Completion] = []
        if len(words) == 0:
            return commands
        if self._is_completing_command(words, word_before_cursor):
            commands = [Completion("hn")]
        else:
            if "hn" not in words:
                return commands
            if self._is_completing_subcommand(words, word_before_cursor):
                commands = [Completion(sub_com) for sub_com in SUBCOMMANDS.keys()]
            else:
                if self._is_completing_arg(words, word_before_cursor):
                    commands = [Completion(arg) for arg in self._arg_completions(words)]
                else:
                    commands = [
                        Completion(arg)
                        for arg in self._completing_subcommand_option(words)
                    ]
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=self.fuzzy_match
        )
        return completions
