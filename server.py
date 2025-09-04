from fastapi import FastAPI
import os
import threading
import asyncio
from contextlib import asynccontextmanager
from bot.main import run_bot


@asynccontextmanager
async def lifespan(app: FastAPI):

    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Skima bot start running"}




if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)