import asyncio
import logging
from contextlib import suppress

from core.bot import bot
from core.dispatcher import dp
from services.admin_service import check_orders_time_loop


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
