from prompt_toolkit.completion import Completer as ClCompleter

from neo_haxor_news.completions import SUBCOMMANDS, ARGS_OPTS_LOOKUP
from neo_haxor_news.utils import TextUtils

class Completer(ClCompleter):

    def __init__(self, fuzzy_match : bool, text_utils : TextUtils):
        """Completer for haxor-news.

        Args:
            fuzzy_match (bool): Determines whether to use fuzzy matching.
            text_utils (TextUtils): An instance of `utils.TextUtils`.
        """
        self.fuzzy_match = fuzzy_match
        self.text_utils = text_utils

    def completing_command(self, words : list[str], word_before_cursor : str) -> bool:
        """Determine if we are currently completing the hn command.

        Args:
            words (list[str]): The input text broken into word tokens.
            word_before_cursor (str): The current word before the cursor,
            which might be one or more blank spaces.

        Returns:
            bool: Specifies whether we are currently completing the hn command.
        """

        return (len(words) == 1 and word_before_cursor != "")


    def completing_subcommand(self, words:list[str], word_before_cursor:str) -> bool:
        """Determine if we are currently completing a subcommand.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing a subcommand.
        """
        return (len(words) == 1 and word_before_cursor == "") or (len(words) == 2 and word_before_cursor != "")

    def completing_arg(self, words:list[str], word_before_cursor:str) -> bool:
        """Determine if we are currently completing an arg.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing an arg.
        """
        return (len(words) == 2 and word_before_cursor == "") or (len(words) == 3 and word_before_cursor != "")

    def completing_subcommand_option(self, words : list[str]):
        """Determine if we are currently completing an option.

        :type words: list
        :param words: The input text broken into word tokens.

        :rtype: list
        :return: A list of options.
        """
        options = []
        for subcommand in ARGS_OPTS_LOOKUP.keys():
            if subcommand in words and (
                words[-2] == subcommand
                or self.completing_subcommand_option_util(subcommand, words)
            ):
                options.extend(ARGS_OPTS_LOOKUP[subcommand]["opts"])
        return options

    def completing_subcommand_option_util(self, option : str, words :list[str]) -> bool:
        """Determine if we are currently completing an option.

        Called by completing_subcommand_option as a utility method.

        :type option: str
        :param option: The subcommand in the elements of ARGS_OPTS_LOOKUP.

        :type words: list
        :param words: The input text broken into word tokens.

        :rtype: bool
        :return: Specifies whether we are currently completing an option.
        """
        # Example: Return True for: hn view 0 --comm
        if len(words) > 3:
            if option in words:
                return True
        return False

    def arg_completions(self, words:list[str]) -> list[str]:
        """Generates arguments completions based on the input.

        :type words: list
        :param words: The input text broken into word tokens.

        :rtype: list
        :return: A list of completions.
        """
        if "hn" not in words:
            return []
        for subcommand in ARGS_OPTS_LOOKUP.keys():
            if subcommand in words:
                return [ARGS_OPTS_LOOKUP[subcommand]["args"]]
        return ["10"]

    def get_completions(self, document, _):
        """Get completions for the current scope.

        :type document: :class:`prompt_toolkit.Document`
        :param document: An instance of `prompt_toolkit.Document`.

        :type _: :class:`prompt_toolkit.completion.Completion`
        :param _: (Unused).

        :rtype: generator
        :return: Yields an instance of `prompt_toolkit.completion.Completion`.
        """
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands = []
        if len(words) == 0:
            return commands
        if self.completing_command(words, word_before_cursor):
            commands = ["hn"]
        else:
            if "hn" not in words:
                return commands
            if self.completing_subcommand(words, word_before_cursor):
                commands = list(SUBCOMMANDS.keys())
            else:
                if self.completing_arg(words, word_before_cursor):
                    commands = self.arg_completions(words, word_before_cursor)
                else:
                    commands = self.completing_subcommand_option(
                        words, word_before_cursor
                    )
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=self.fuzzy_match
        )
        return completions
