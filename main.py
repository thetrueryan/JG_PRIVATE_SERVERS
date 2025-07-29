import asyncio
import logging

from bot.dispatcher import dp
from bot.bot import bot
from db.repositories.core import AsyncCore

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())