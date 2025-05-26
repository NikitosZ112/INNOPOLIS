import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import user_handler
from database import Database

load_dotenv()

TOKEN = os.getenv('TOKEN')
PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN')

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_handler.router)

db = Database()

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())