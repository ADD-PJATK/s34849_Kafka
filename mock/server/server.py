#!/usr/bin/env python3
"""
Mock stock API server — local offline substitute for the instructor SSE API.

Endpoints:
  GET /api/tickers             — list of synthetic tickers
  GET /api/latest?ticker=AAPL  — latest tick from fixtures
  GET /api/stream?ticker=AAPL  — SSE stream of synthetic ticks
"""

import asyncio
import json
import random
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"

app = FastAPI(title="Mock Stock API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_tickers():
    with open(FIXTURES_DIR / "tickers.json", encoding="utf-8") as f:
        return json.load(f)


def _load_ticks():
    with open(FIXTURES_DIR / "ticks.json", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/tickers")
def get_tickers():
    return _load_tickers()


@app.get("/api/latest")
def get_latest(ticker: str):
    ticks = _load_ticks()
    matching = [t for t in ticks if t["ticker"] == ticker]
    return matching[-1] if matching else {}


@app.get("/api/stream")
async def stream(ticker: str):
    base_ticks = _load_ticks()
    base = next((t for t in base_ticks if t["ticker"] == ticker), None)
    base_price = base["lastPrice"] if base else 100.0

    async def event_generator():
        price = base_price
        while True:
            price += round(random.uniform(-1.5, 1.5), 2)
            tick = {
                "ticker": ticker,
                "lastPrice": round(price, 2),
                "volume": random.randint(500, 5000),
                "trader_email": random.choice(["alice@trading.test", "bob@trading.test"]),
                "operator_name": random.choice(["Alice Smith", "Bob Jones"]),
                "comment": "Live synthetic tick",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            yield f"data: {json.dumps(tick)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
