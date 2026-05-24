"""
This module contains utility functions for
making HTTP requests and parsing the HTML responses.
"""


import logging
import random
from typing import List

import requests
from bs4 import BeautifulSoup


def get_unique_uris(seed_uri: str, total_uri: int, time: int = 5) -> List[str]:
    """Get the unique URIs from the seed URI and recursively search them
    for more unique URIs until the upper threshold has been hit or no more can
    be found.

    Parameters:
        seed_uri (str): The starting URI to make requests on.
        total_uri (int): The total number of unique URIs to search for.
        time (int): The time before a HTTP request times out.

    Returns:
        A list containing strings of unique URIs.
    """
    logging.debug("Searching for %s links on %s", total_uri, seed_uri)
    response = requests.get(seed_uri, timeout=time)

    links = list(set(extract_links(response, time)))
    logging.debug("%s unique links found", len(links))

    if len(links) == 0:
        logging.debug("No links found on %s", seed_uri)
        return []

    while len(links) < total_uri:
        new_seed = random.choice(links)
        logging.debug("Searching for links on %s", new_seed)
        logging.debug("Looking for %s links", total_uri - len(links))
        links.remove(new_seed)  # Prevent duplicate requests
        new_links = extract_links(requests.get(new_seed, timeout=time))
        links.extend(new_links)
        links = list(set(links))

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
        try:
            if _validate_link(link["href"], time) is True:
                logging.info("Link found: %s", link["href"])
                links.append(link["href"])
        except KeyError:
            logging.debug("Skipping anchor with no href: %s", link)

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
    except requests.exceptions.RequestException as exc:
        logging.debug("Request failed for %s: %s", uri, exc)
        return False

    try:
        content_type = response.headers["Content-Type"]
        size_in_bytes = int(response.headers["Content-Length"])
    except KeyError:
        return False

    if "text/html" not in content_type or size_in_bytes < length:
        return False

    return True
