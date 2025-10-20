from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time

app = FastAPI(title="Day Agent API")

@app.get("/callback/approve")
def approve(item: str):
    return JSONResponse({"status": "approved", "item": item, "ts": int(time.time())})

@app.get("/callback/decline")
def decline(item: str):
    return JSONResponse({"status": "declined", "item": item, "ts": int(time.time())})
