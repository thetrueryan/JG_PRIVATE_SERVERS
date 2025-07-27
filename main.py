import asyncio
import logging

from dp_init import dp
from bot_init import bot


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())