"""
This module contains utility functions for
making HTTP requests and parsing the HTML responses.
"""


from typing import List

import requests

# TODO: Change to parameter and CLI optional argument
TIMEOUT_TIME = 5


def get_unique_uris(seed_uri: str, total_uri: int) -> List[str]:
    """Get the unique URIs from the seed URI and recursively search them
    for more unique URIs until the upper bound has been hit or no more can
    be found.

    Parameters:
        seed_uri (str): The starting URI to make requests on.
        total_uri (int): The total number of unique URIs to search for.

    Returns:
        A list containing strings of unique URIs.
    """
    response = requests.get(seed_uri, timeout=TIMEOUT_TIME)
    # Ensure valid content type; If not ...
    links = extract_links(response)
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
    # For each link
    # Grab content/type header
    # Disregard link if not text/html
    # Check valid size
    # Disregard if < 1000 bytes

    return []
