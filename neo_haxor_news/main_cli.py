#!/usr/bin/env python


from neo_haxor_news.hacker_news_cli import HackerNewsCli


def cli():
    """Creates and calls Haxor."""
    haxor_news = HackerNewsCli()
    haxor_news.cli()


if __name__ == "__main__":
    cli()
