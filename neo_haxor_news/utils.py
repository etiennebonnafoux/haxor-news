import re
import shlex
from collections.abc import Generator, Iterable

from prompt_toolkit.completion import Completion

from neo_haxor_news.completions import META_LOOKUP


class TextUtils:
    """Utilities for parsing and matching text."""

    def find_matches(self, word: str, collection: Iterable[Completion], fuzzy: bool):
        """Find all matches in collection for word.

        :type word: str
        :param word: The word before the cursor.

        :type collection: iterable
        :param collection: A collection of words to match.

        :type fuzzy: bool
        :param fuzzy: Determines whether to use fuzzy matching.

        :rtype: generator
        :return: Yields an instance of `prompt_toolkit.completion.Completion`.
        """
        word = self._last_token(word).lower()
        for suggestion in self._find_collection_matches(
            word, [compl.text for compl in collection], fuzzy
        ):
            yield suggestion
        """

        :type text: str
        :param text: 

        :rtype: list
        :return: 
        """

    def get_tokens(self, text: str) -> list[str]:
        """Parse out all tokens.

        Args:
            text (str): A string to be split into tokens.

        Returns:
            list[str]: A list of strings for each word in the text.
        """
        if text is not None:
            text = text.strip()
            words = shlex.split(text)
            return words
        return []

    def _last_token(self, text: str) -> str:
        """Find the last word in text.

        Args:
            text (str): A string to parse and obtain the last word.

        Returns:
            str: The last word in the text.
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = shlex.split(text)[-1]
                word = word.strip()
                return word
        return ""

    def _fuzzy_finder(
        self, text: str, collection: Iterable[str], case_sensitive: bool = True
    ) -> Generator[str, None, None]:
        """Customized fuzzy finder with optional case-insensitive matching.

        Adapted from: https://github.com/amjith/fuzzyfinder.

        Args:
            text (str): Input string entered by user.
            collection (Iterable[str]): collection of strings which will be filtered based
            case_sensitive (bool, optional): Determines whether the find will be case. Defaults to True.

        Yields:
            Generator[str, None, None]: Yields a list of suggestions narrowed down from `collections`
            using the `text` input.
        """

        suggestions = []
        pat = ".*?".join([re.escape(ch) for ch in text])
        regex = re.compile(pat)
        for item in collection:
            if case_sensitive:
                r = regex.search(item)
            else:
                r = regex.search(item.lower())
            if r:
                suggestions.append((len(r.group()), r.start(), item))
        return (z for _, _, z in sorted(suggestions))

    def _find_collection_matches(
        self, word: str, collection: Iterable[str], fuzzy: bool
    ) -> Generator[Completion, None, None]:
        """Yield all matching names in list.

        Args:
            word (str): The word before the cursor.
            collection (Iterable[str]): A collection of words to match.
            fuzzy (bool): Determines whether to use fuzzy matching.

        Yields:
            Completion: Yields an instance of `prompt_toolkit.completion.Completion`.
        """
        word = word.lower()
        if fuzzy:
            for suggestion in self._fuzzy_finder(
                word, collection, case_sensitive=False
            ):
                yield Completion(suggestion, -len(word), display_meta="display_meta")
        else:
            for name in sorted(collection):
                if name.lower().startswith(word) or not word:
                    display = None
                    display_meta = None
                    if name in META_LOOKUP:
                        display_meta = META_LOOKUP[name]
                    yield Completion(
                        name, -len(word), display=display, display_meta=display_meta
                    )
