import asyncio
from datetime import datetime, timedelta

from loggers.logger import logger
from db.repositories.core import AsyncCore
from decorators.logging_decorator import log_call
from scripts.admin import send_order_info_to_admin
from scripts.send_orders_warning import send_order_warning_to_user


@log_call
async def check_orders_time_loop():
    while True:
        orders = await AsyncCore.get_orders_list()
        if orders:
            now_time = datetime.utcnow()
            for order in orders:
                expire_time = order.expires_at
                if now_time + timedelta(days=3) >= expire_time:
                    time_left = (expire_time - now_time).days
                    await send_order_warning_to_user(order, time_left)
                    order_id = order.id
                    user_id = order.user_id
                    price = order.price
                if now_time >= expire_time:
                    await send_order_info_to_admin(
                        f"Ордер с id: {order_id} истек.\n id пользователя: {user_id} \n Цена ордера: {price}"
                    )
            logger.info("Круг проверки срока аренды завершен. Ожидаем 12 часов.")
        else:
            logger.info("Не найдено ордеров для проверки")

        await asyncio.sleep(43200)
