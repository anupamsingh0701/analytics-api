from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Analytics API")

# CORS - allow all origins so the grader browser page can hit it directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_3alfte11qgttbm8r558f0rqf"
EMAIL = "anupamsingh0701@gmail.com"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class EventBatch(BaseModel):
    events: List[Event]


@app.options("/analytics")
async def analytics_options():
    """Handle CORS preflight"""
    return {}


@app.post("/analytics")
async def analytics(
    batch: EventBatch,
    x_api_key: Optional[str] = Header(default=None),
):
    # Auth check
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid or missing API key")

    events = batch.events

    total_events = len(events)
    unique_users = len({e.user for e in events})

    # revenue = sum of amounts where amount > 0
    revenue = sum(e.amount for e in events if e.amount > 0)

    # top_user = user whose positive-amount total is highest
    user_totals: dict[str, float] = {}
    for e in events:
        if e.amount > 0:
            user_totals[e.user] = user_totals.get(e.user, 0.0) + e.amount

    top_user = max(user_totals, key=lambda u: user_totals[u]) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": round(revenue, 10),  # preserve precision
        "top_user": top_user,
    }


@app.get("/")
async def root():
    return {"status": "ok", "message": "Analytics API is running"}
