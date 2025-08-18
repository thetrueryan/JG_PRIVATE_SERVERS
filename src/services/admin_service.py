import asyncio
from datetime import datetime, timedelta
from typing import Optional

from core.settings import ADMIN_TG_ID
from core.logger import logger
from repositories.bot_repository import BotRepo
from core.decorators import log_call
from core.bot import bot
from models.models import OrdersOrm


@log_call
async def check_orders_time_loop():
    try:
        while True:
            orders = await BotRepo.get_orders_list()
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
    except asyncio.CancelledError as e:
        logger.warning(f"Фоновая проверка ордеров остановлена {e}")
        raise


@log_call
async def send_order_info_to_admin(
    order_info: Optional[str] = None, user_info: Optional[str] = None
):
    if order_info:
        if user_info:
            await bot.send_message(chat_id=ADMIN_TG_ID, text=order_info + user_info)
        else:
            await bot.send_message(chat_id=ADMIN_TG_ID, text=order_info)


async def send_order_warning_to_user(order: OrdersOrm, time_left: int):
    user_id = order.user_id
    user = await BotRepo.get_user_by_id(user_id)
    if user:
        telegram_id = user.telegram_id
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<u>❗️Уважаемый пользователь!</u>\n\n⌛️ Аренда одного из ваших серверов истекает через <b>{time_left} дней!</b>\n\n💰 Оплатите его во вкладке <u>status</u>, если хотите продолжать им пользоваться по истечении срока.",
        )
