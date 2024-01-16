#!/usr/bin/env python3

"""Main module for the URI Gatherer."""

import argparse
import logging


def main():
    """Main driver of the URI Gatherer script."""
    parser = argparse.ArgumentParser(
        description="Gather unique URIs from links found in the seed URI."
    )

    parser.add_argument("seed_uri", help="URI to scan for other unique URIs.")

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output all program debug logs to console.",
    )

    args = parser.parse_args()

    if args.debug is True:
        logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    main()
