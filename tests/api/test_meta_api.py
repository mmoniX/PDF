"""Tests for the root service-info endpoint."""

from tests.api.conftest import client


def test_root_info():
    res = client.get("/")
    assert res.status_code == 200
    body = res.json()
    assert body["name"] == "PDF Editor MVP"
    assert body["version"] == "0.1.0"
    assert "/pdf/split" in body["endpoints"]
    assert "/pdf/merge" in body["endpoints"]
