#!/usr/bin/env python3

"""Main module for the URI Gatherer."""

import argparse
import logging
from datetime import datetime

from gatherer import get_unique_uris


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
        metavar="timeout",
        dest="timeout",
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
    # TODO: Optional flag to turn this back on
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    uris = get_unique_uris(args.seed_uri, args.unique_count, args.timeout)

    with open(
        f"{datetime.now().strftime('%Y-%m-%d')}-uris.txt", "w", encoding="UTF-8"
    ) as file:
        for link in uris:
            file.write(f"{link}\n")

            # Print to console
            print(link)


if __name__ == "__main__":
    main()
