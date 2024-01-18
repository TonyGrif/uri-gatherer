import pytest
import requests

from src.utils import extract_links, get_unique_uris


@pytest.fixture
def seed_uri():
    return "https://weiglemc.github.io/"


@pytest.fixture
def seed_request(seed_uri):
    return requests.get(seed_uri, timeout=5)


class TestUtils:
    def test_get_uris(self, seed_uri):
        uris = get_unique_uris(seed_uri, 50)
        assert len(uris) > 0

        uris = get_unique_uris("https://api.github.com", 5)
        assert len(uris) == 0

    def test_extract_links(self, seed_request):
        assert seed_request.status_code == 200
        assert "text/html" in seed_request.headers["Content-Type"]

        links = extract_links(seed_request)
        assert len(links) > 0
