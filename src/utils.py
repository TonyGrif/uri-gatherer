"""
This module contains utility functions for
making HTTP requests and parsing the HTML responses.
"""


import logging
from typing import List

import requests
from bs4 import BeautifulSoup


def get_unique_uris(seed_uri: str, total_uri: int, time: int = 5) -> List[str]:
    """Get the unique URIs from the seed URI and recursively search them
    for more unique URIs until the upper bound has been hit or no more can
    be found.

    Parameters:
        seed_uri (str): The starting URI to make requests on.
        total_uri (int): The total number of unique URIs to search for.
        time (int): The time before a HTTP request times out.

    Returns:
        A list containing strings of unique URIs.
    """
    response = requests.get(seed_uri, timeout=time)
    # Ensure valid content type; If not ...
    links = extract_links(response)
    logging.debug("%s links found on %s", len(links), seed_uri)
    # Check if ready to return (collection >= total)
    # If so return as list/dictionary
    # Else, pick random URI
    # Call function again with new seed

    return links


def extract_links(response: requests.Response) -> List[str]:
    """Extract the links from an HTTP request.

    Parameters:
        response (Response): A valid response object.

    Returns:
        A list containing strings of unique URIs.
    """
    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    for link in soup.find_all("a"):
        links.append(link["href"])

    return list(set(links))
