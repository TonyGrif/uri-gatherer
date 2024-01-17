"""
This module contains utility functions for
making HTTP requests and parsing the HTML responses.
"""


from typing import List


def get_unique_uris(seed_uri: str, total_uri: int) -> List[str]:
    """Get the unique URIs from the seed URI and recursively search them
    for more unique URIs.

    Parameters:
        seed_uri (str): The starting URI to make requests on.
        total_uri (int): The total number of unique URIs to search for.

    Returns:
        A list containing strings of unique URIs.
    """
    # Make request on seed
    # Parse for links
    # Check if ready to return (collection >= total)
    # If so return as list/dictionary
    # Else, pick random URI
    # Call function again with new seed

    return []


def extract_links() -> List[str]:
    """Extract the links from an HTTP request.

    Parameters:

    Returns:
        A list containing strings of unique URIs.
    """
    # Assume valid response
    # For each link
    # Grab content/type header
    # Disregard link if not text/html
    # Check valid size
    # Disregard if < 1000 bytes

    return []
