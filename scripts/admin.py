from bot.bot import bot
from config.settings import ADMIN_TG_ID

async def send_order_info_to_admin(order_info: str, user_info: str):

    await bot.send_message(chat_id=ADMIN_TG_ID, text=order_info+user_info)
    