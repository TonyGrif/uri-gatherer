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

    links = list(set(extract_links(response, time)))
    logging.debug("%s unique links found on %s", len(links), seed_uri)
    # Check if ready to return (collection >= total)
    # If so return as list/dictionary
    # Else, pick random URI
    # Call function again with new seed

    return links


def extract_links(response: requests.Response, time: int = 5) -> List[str]:
    """Extract the links from an HTTP request. Only links containing
    "text/html" content headers will be returned.

    Parameters:
        response (Response): A valid response object.
        time (int): The time before a request will be ended.

    Returns:
        A list containing strings of unique URIs.
    """
    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    for link in soup.find_all("a"):
        if _validate_link(link["href"], time) is True:
            links.append(link["href"])

    return links


def _validate_link(uri: str, time: int = 5, length: int = 1000) -> bool:
    """Validate the URI has a valid text/html content type header
    and has a valid number of bytes.

    Parameters:
        uri (str): The URI to validate.
        time (int): The time before a HTTP request will timeout.
        length (int): The desired number of bytes for a request to be valid.

    Returns:
        A boolean value signifying if it is a valid URI.
    """
    try:
        response = requests.get(uri, timeout=time, allow_redirects=True)
    except Exception:
        return False

    if "text/html" not in response.headers["Content-Type"]:
        return False
    try:
        if int(response.headers["Content-Length"]) < length:
            return False
    except KeyError:
        return False

    return True
