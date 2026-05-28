"""
Tests for the mock API server.

BUG 1 (deliberate): test_get_latest asserts 'price' key but server returns 'lastPrice'.
Fix: change assert to check 'lastPrice'.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "mock" / "server"))

from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_get_tickers():
    resp = client.get("/api/tickers")
    assert resp.status_code == 200
    tickers = resp.json()
    assert isinstance(tickers, list)
    assert "AAPL" in tickers
    assert len(tickers) >= 3


def test_get_latest():
    resp = client.get("/api/latest?ticker=AAPL")
    assert resp.status_code == 200
    tick = resp.json()
    assert tick["ticker"] == "AAPL"
    assert "lastPrice" in tick, "Expected 'lastPrice' key in tick response"


def test_get_latest_unknown_ticker():
    resp = client.get("/api/latest?ticker=UNKNOWN")
    assert resp.status_code == 200
    assert resp.json() == {}


def test_tickers_not_empty():
    resp = client.get("/api/tickers")
    assert len(resp.json()) > 0
