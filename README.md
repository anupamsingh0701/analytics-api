# Analytics API

A stateless FastAPI service that exposes `POST /analytics` for event batch aggregation.

## Endpoint

`POST /analytics`

### Authentication
Requires header: `X-API-Key: ak_3alfte11qgttbm8r558f0rqf`

Missing or wrong key returns HTTP 401.

### Request Body
```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    ...
  ]
}
```

### Response
```json
{
  "email": "anupamsingh0701@gmail.com",
  "total_events": 10,
  "unique_users": 4,
  "revenue": 123.45,
  "top_user": "alice"
}
```

## Aggregation Rules
- `total_events` — count of all events
- `unique_users` — distinct user count
- `revenue` — sum of amounts where `amount > 0`
- `top_user` — user with highest positive-amount total

## Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploy on Render
1. Push this folder as a GitHub repo
2. Connect on [render.com](https://render.com) → New Web Service
3. Set root directory to this folder
4. Render auto-detects `render.yaml`
