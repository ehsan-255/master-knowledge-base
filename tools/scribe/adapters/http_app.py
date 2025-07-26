from fastapi import FastAPI
from tools.scribe.adapters.http_validation import L1ValidationMiddleware

app = FastAPI()
app.add_middleware(L1ValidationMiddleware)

# Add routes below using FastAPI routers as needed (kept minimal here per boundary focus)