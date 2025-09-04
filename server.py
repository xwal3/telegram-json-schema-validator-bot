from fastapi import FastAPI
import os

import asyncio
from bot.main import run_bot


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Skima bot start running"}

@app.on_event("startup")
async def start_bot():
    asyncio.create_task(run_bot())


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)