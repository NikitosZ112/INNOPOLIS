from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request
from config import TOKEN

app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher()

@app.post("/webhook")
async def webhook_handler(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}