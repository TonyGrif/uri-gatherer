#!/usr/bin/env python3

"""Main module for the URI Gatherer."""

import argparse
import logging

from src.utils import get_unique_uris


def main():
    """Main driver of the URI Gatherer script."""
    parser = argparse.ArgumentParser(
        description="Gather unique URIs from links found in the seed URI."
    )

    parser.add_argument("seed_uri", help="URI to scan for other unique URIs.")

    parser.add_argument(
        "unique_count",
        nargs="?",
        type=int,
        default=500,
        help="The number of unique URIs to find (default 500).",
    )

    parser.add_argument(
        "-T",
        "--timeout",
        nargs="?",
        type=int,
        default=5,
        help="The time before a HTTP request times out.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="logging_level",
        const=logging.INFO,
        help="Output verbose info logs to console.",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="logging_level",
        const=logging.DEBUG,
        help="Output all program debug logs to console.",
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.logging_level)

    uris = get_unique_uris(args.seed_uri, args.unique_count, args.timeout)

    print(*uris, sep="\n")


if __name__ == "__main__":
    main()
