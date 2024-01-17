import pytest
import requests

from src.utils import get_unique_uris, extract_links


@pytest.fixture
def seed_uri():
    return "https://weiglemc.github.io/"

@pytest.fixture
def seed_request(seed_uri):
    return requests.get(seed_uri, timeout=5)


class TestUtils:
    def test_get_uris(self, seed_uri):
        uris = get_unique_uris(seed_uri, 10)
        #assert len(uris) == 10

    def test_extract_links(self, seed_request):
        assert seed_request.status_code == 200
