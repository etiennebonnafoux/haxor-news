#!/usr/bin/env python


from neo_haxor_news.haxor import Haxor


def cli():
    """Creates and calls Haxor."""
    try:
        haxor = Haxor()
        haxor.run_cli()
    except (EOFError, KeyboardInterrupt):
        haxor.cli.set_return_value(None)


if __name__ == "__main__":
    cli()
