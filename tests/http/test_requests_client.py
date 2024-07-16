"""Tests for the `requests` HTTP client."""

import pytest
import requests
import responses

from csobpg.http import HTTPTimeoutError
from csobpg.http.requests_client import RequestsHTTPClient


@responses.activate
def test_success_post_json():
    """Test successful post_json."""
    responses.add(responses.POST, "https://example.com", json={"k": "v"})
    response = RequestsHTTPClient().request(
        "post", "https://example.com", json={}
    )
    assert response.status_code == 200
    assert response.json == {"k": "v"}


@responses.activate
def test_unsuccessful_post_json():
    """Test unsuccessful post_json."""
    responses.add(
        responses.POST, "https://example.com", json={"k": "v"}, status=400
    )
    response = RequestsHTTPClient().request(
        "post", "https://example.com", json={}
    )
    assert response.status_code == 400
    assert response.json == {"k": "v"}


@responses.activate
def test_post_json_timeout():
    """Test post_json timeout."""
    responses.add(
        responses.POST,
        "https://example.com",
        body=requests.Timeout(),
        status=400,
    )

    with pytest.raises(HTTPTimeoutError):
        RequestsHTTPClient().request("post", "https://example.com", json={})


@responses.activate
def test_get_ok():
    """Test successful get."""
    responses.add(responses.GET, "https://example.com", json={"k": "v"})
    response = RequestsHTTPClient().request("get", "https://example.com")
    assert response.status_code == 200
    assert response.json == {"k": "v"}
