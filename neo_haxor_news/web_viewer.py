# coding: utf-8


import re

import click
from markdownify import markdownify as md
import requests


class WebViewer:
    """Handle viewing of web content within the terminal.

    :type html: :class:`HTMLParser.HTMLParser`
    :param html: An instance of `HTMLParser.HTMLParser`.

    :type html_to_text: :class:`html2text.html2text.HTML2Text`
    :param html_to_text: An instance of `html2text.html2text.HTML2Text`.
    """

    def format_markdown(self, text):
        """Add color to the input markdown using click.style.

        :type text: str
        :param text: The markdown text.

        :rtype: str
        :return: The input `text`, formatted.
        """
        pattern_url_name = r"[^]]*"
        pattern_url_link = r"[^)]+"
        pattern_url = r"([!]*\[{0}]\(\s*{1}\s*\))".format(
            pattern_url_name, pattern_url_link
        )
        regex_url = re.compile(pattern_url)
        text = regex_url.sub(click.style(r"\1", fg="green"), text)
        pattern_url_ref_name = r"[^]]*"
        pattern_url_ref_link = r"[^]]+"
        pattern_url_ref = r"([!]*\[{0}]\[\s*{1}\s*\])".format(
            pattern_url_ref_name, pattern_url_ref_link
        )
        regex_url_ref = re.compile(pattern_url_ref)
        text = regex_url_ref.sub(click.style(r"\1", fg="green"), text)
        regex_list = re.compile(r"(  \*.*)")
        text = regex_list.sub(click.style(r"\1", fg="cyan"), text)
        regex_header = re.compile(r"(#+) (.*)")
        text = regex_header.sub(click.style(r"\2", fg="yellow"), text)
        regex_bold = re.compile(r"(\*\*|__)(.*?)\1")
        text = regex_bold.sub(click.style(r"\2", fg="cyan"), text)
        regex_code = re.compile(r"(`)(.*?)\1")
        text = regex_code.sub(click.style(r"\1\2\1", fg="cyan"), text)
        text = re.sub(r"(\s*\r?\n\s*){2,}", r"\n\n", text)
        return text

    def generate_url_contents(self, url):
        """Generate the formatted contents of the given item's url.

        Converts the HTML to text using HTML2Text, colors it, then displays
            the output in a pager.

        :type url: str
        :param url: The url whose contents to fetch.

        :rtype: str
        :return: The string representation of the formatted url contents.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
            } 
            raw_response = requests.get(url, headers=headers)
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            contents = "Error: " + str(e) + "\n"
            contents += "Try running hn view # with the --browser/-b flag\n"
            return contents
        text = raw_response.text
        contents = md(text)
        contents = re.sub(r"[^\x00-\x7F]+", "", contents)
        contents = self.format_markdown(contents)
        return contents
