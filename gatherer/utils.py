"""This module contains utility functions for
making HTTP requests and parsing the HTML responses.
"""

import logging
import random

import requests
from bs4 import BeautifulSoup


def get_unique_uris(seed_uri: str, total_uri: int, timeout: int = 5) -> list[str]:
    """Get the unique URIs from the seed URI and recursively search them
    for more unique URIs until the upper threshold has been hit or no more can
    be found.

    Args:
        seed_uri: The starting URI to make requests on.
        total_uri: The total number of unique URIs to search for.
        timeout: The time in seconds before a HTTP request times out.

    Returns:
        A list containing strings of unique URIs.
    """
    logging.debug("Searching for %s links on %s", total_uri, seed_uri)

    with requests.Session() as session:
        response = session.get(seed_uri, timeout=timeout)

        links = list(set(extract_links(response, session, timeout)))
        logging.debug("%s unique links found", len(links))

        if len(links) == 0:
            logging.debug("No links found on %s", seed_uri)
            return []

        while links and len(links) < total_uri:
            new_seed = random.choice(links)
            logging.debug("Searching for links on %s", new_seed)
            logging.debug("Looking for %s links", total_uri - len(links))
            links.remove(new_seed)  # Prevent duplicate requests
            new_response = session.get(new_seed, timeout=timeout)
            new_links = extract_links(new_response, session, timeout)
            links.extend(new_links)
            links = list(set(links))

    return links


def extract_links(
    response: requests.Response,
    session: requests.Session | None = None,
    timeout: int = 5,
) -> list[str]:
    """Extract the links from an HTTP request. Only links containing
    "text/html" content headers will be returned.

    Args:
        response: A valid response object.
        session: The HTTP session to use for validation requests. A new
            session is created if not provided.
        timeout: The time in seconds before a request will time out.

    Returns:
        A list containing strings of unique URIs.
    """
    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    close_session = session is None
    s = session if session is not None else requests.Session()

    try:
        for link in soup.find_all("a"):
            try:
                if _validate_link(link["href"], s, timeout) is True:
                    logging.info("Link found: %s", link["href"])
                    links.append(link["href"])
            except KeyError:
                logging.debug("Skipping anchor with no href: %s", link)
    finally:
        if close_session:
            s.close()

    return links


def _validate_link(
    uri: str,
    session: requests.Session,
    timeout: int = 5,
    length: int = 1000,
) -> bool:
    """Validate the URI has a valid text/html content type header
    and has a valid number of bytes.

    Args:
        uri: The URI to validate.
        session: The HTTP session to use for the request.
        timeout: The time in seconds before a HTTP request will time out.
        length: The minimum number of bytes for a response to be valid.

    Returns:
        A boolean value signifying if it is a valid URI.
    """
    try:
        response = session.get(uri, timeout=timeout, allow_redirects=True)
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
