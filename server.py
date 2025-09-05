import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder
from bot.main import run_bot
from config.settings import TELEGRAM_BOT_TOKEN
from contextlib import asynccontextmanager


bot = Bot(token=TELEGRAM_BOT_TOKEN)
application = ApplicationBuilder().bot(bot).build()

WEBHOOK_PATH = f"/webhook/{TELEGRAM_BOT_TOKEN}"
@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = os.environ.get("WEBHOOK_URL")  
    if not webhook_url:
        raise ValueError("WEBHOOK_URL environment variable is missing!")
    await bot.delete_webhook()
    await bot.set_webhook(webhook_url)
    print(f"Webhook set to: {webhook_url}")
    yield

app = FastAPI(lifespan=lifespan)

WEBHOOK_PATH = f"/webhook/{TELEGRAM_BOT_TOKEN}"

@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.update_queue.put(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Skima bot running with webhook!"}





if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)