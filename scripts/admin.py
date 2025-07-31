from typing import Optional

from bot.bot import bot
from config.settings import ADMIN_TG_ID
from decorators.logging_decorator import log_call

@log_call
async def send_order_info_to_admin(order_info: Optional[str]=None, user_info: Optional[str]=None):
    if order_info:
        if user_info:
            await bot.send_message(chat_id=ADMIN_TG_ID, text=order_info+user_info)
        else:
            await bot.send_message(chat_id=ADMIN_TG_ID, text=order_info)
        
    