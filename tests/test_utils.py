from unittest.mock import MagicMock

import pytest
import requests

from gatherer import extract_links, get_unique_uris
from gatherer.utils import _validate_link

HTML_WITH_LINKS = b"""
<html><body>
  <a href="https://example.com/page1">Page 1</a>
  <a href="https://example.com/page2">Page 2</a>
  <a>No href</a>
</body></html>
"""

HTML_NO_LINKS = b"<html><body><p>Nothing here</p></body></html>"


def _mock_response(
    content=b"", content_type="text/html", content_length="2000", status=200
):
    """Build a minimal mock requests.Response."""
    resp = MagicMock(spec=requests.Response)
    resp.content = content
    resp.status_code = status
    resp.headers = {"Content-Type": content_type, "Content-Length": content_length}
    return resp


class TestExtractLinks:
    def test_returns_valid_links(self):
        response = _mock_response(content=HTML_WITH_LINKS)
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(
            content_type="text/html", content_length="2000"
        )

        links = extract_links(response, session)

        assert "https://example.com/page1" in links
        assert "https://example.com/page2" in links

    def test_skips_anchors_without_href(self):
        response = _mock_response(content=HTML_WITH_LINKS)
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(
            content_type="text/html", content_length="2000"
        )

        links = extract_links(response, session)

        assert None not in links

    def test_returns_empty_for_no_links(self):
        response = _mock_response(content=HTML_NO_LINKS)
        session = MagicMock(spec=requests.Session)

        links = extract_links(response, session)

        assert links == []


class TestValidateLink:
    def test_valid_html_link(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(
            content_type="text/html; charset=utf-8", content_length="5000"
        )

        assert _validate_link("https://example.com", session) is True

    def test_rejects_non_html_content_type(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(
            content_type="application/json", content_length="5000"
        )

        assert _validate_link("https://api.example.com", session) is False

    def test_rejects_response_below_minimum_size(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(
            content_type="text/html", content_length="500"
        )

        assert _validate_link("https://example.com/tiny", session) is False

    def test_rejects_on_network_error(self):
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = requests.exceptions.ConnectionError("unreachable")

        assert _validate_link("https://unreachable.example.com", session) is False

    def test_rejects_missing_content_length_header(self):
        session = MagicMock(spec=requests.Session)
        resp = MagicMock(spec=requests.Response)
        resp.headers = {"Content-Type": "text/html"}
        session.get.return_value = resp

        assert _validate_link("https://example.com", session) is False


SEED_URI = "https://weiglemc.github.io/"


@pytest.fixture
def seed_request():
    return requests.get(SEED_URI, timeout=5)


@pytest.mark.integration
class TestIntegration:
    def test_get_uris(self):
        uris = get_unique_uris(SEED_URI, 50)
        assert len(uris) >= 50

        uris = get_unique_uris("https://api.github.com", 5)
        assert len(uris) == 0

    def test_extract_links(self, seed_request):
        assert seed_request.status_code == 200
        assert "text/html" in seed_request.headers["Content-Type"]

        links = extract_links(seed_request)
        assert len(links) > 0
