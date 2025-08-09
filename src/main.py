import asyncio
import logging

from bot.bot import bot
from bot.dispatcher import dp
from db.repositories.core import AsyncCore
from scripts.order_time_check import check_orders_time_loop


async def main():
    logging.basicConfig(level=logging.INFO)
    await asyncio.gather(
        check_orders_time_loop(),
        dp.start_polling(bot),
    )


if __name__ == "__main__":
    asyncio.run(main())
