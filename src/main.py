import asyncio
import logging
from contextlib import suppress

from bot.bot import bot
from bot.dispatcher import dp
from db.repositories.core import AsyncCore
from scripts.order_time_check import check_orders_time_loop


async def main():
    logging.basicConfig(level=logging.INFO)

    background_task = asyncio.create_task(check_orders_time_loop())

    try:
        await dp.start_polling(bot)
    finally:
        background_task.cancel()
        with suppress(asyncio.CancelledError):
            await background_task


if __name__ == "__main__":
    asyncio.run(main())
