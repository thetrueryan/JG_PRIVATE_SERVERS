from db.models.models import OrdersOrm
from bot.bot import bot
from db.repositories.core import AsyncCore


async def send_order_warning_to_user(order: OrdersOrm, time_left: int):
    user_id = order.user_id
    user = await AsyncCore.get_user_by_id(user_id)
    if user:
        telegram_id = user.telegram_id
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<u>❗️Уважаемый пользователь!</u>\n\n⌛️ Аренда одного из ваших серверов истекает через <b>{time_left} дней!</b>\n\n💰 Оплатите его во вкладке <u>status</u>, если хотите продолжать им пользоваться по истечении срока.",
        )
