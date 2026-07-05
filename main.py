from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Analytics API")

# CORS - allow all origins so the grader browser page can hit it directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_3alfte11qgttbm8r558f0rqf"
EMAIL = "24f2008630@ds.study.iitm.ac.in"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "*",
}


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class EventBatch(BaseModel):
    events: List[Event]


@app.options("/analytics")
async def analytics_options():
    """Handle CORS preflight"""
    return JSONResponse(content={}, headers=CORS_HEADERS)


@app.post("/analytics")
async def analytics(
    request: Request,
    batch: EventBatch,
    x_api_key: Optional[str] = Header(default=None),
):
    # Auth check - return 401 with CORS headers so browser grader sees it
    if x_api_key is None or x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: invalid or missing API key"},
            headers=CORS_HEADERS,
        )

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

    return JSONResponse(
        content={
            "email": EMAIL,
            "total_events": total_events,
            "unique_users": unique_users,
            "revenue": revenue,
            "top_user": top_user,
        },
        headers=CORS_HEADERS,
    )


@app.get("/")
async def root():
    return {"status": "ok", "message": "Analytics API is running"}
