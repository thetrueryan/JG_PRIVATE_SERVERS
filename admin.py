from bot_init import bot


async def send_order_info_to_admin(order_info: str, user_info: str):
    await bot.send_message(chat_id=7270003150, text=order_info+user_info)