import os
import httpx
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

GOOGLE_KEY = os.getenv("GOOGLE_MAPS_KEY")
GOOGLE_BASE = "https://maps.googleapis.com/maps/api"

app = FastAPI(title="TravelPlanner Proxy", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/geocode")
async def geocode(address: str = Query(...)):
    url = f"{GOOGLE_BASE}/geocode/json"
    params = {"address": address, "key": GOOGLE_KEY}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
    return JSONResponse(r.json())

@app.get("/places/text")
async def places_text(
    query: str,
    location: Optional[str] = None,
    radius: Optional[int] = 3000
):
    url = f"{GOOGLE_BASE}/place/textsearch/json"
    params = {"query": query, "key": GOOGLE_KEY}
    if location:
        params["location"] = location
    if radius:
        params["radius"] = radius
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
    return JSONResponse(r.json())

@app.get("/directions")
async def directions(origin: str, destination: str, mode: str = "walking"):
    url = f"{GOOGLE_BASE}/directions/json"
    params = {"origin": origin, "destination": destination, "mode": mode, "key": GOOGLE_KEY}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
    return JSONResponse(r.json())
