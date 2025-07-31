from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers.user_handlers import (
    start, main_menu_handlers, buy_vpn_handlers, go_back,
    status_handlers,
)
from bot.handlers.admin_handlers import admin_menu, send_to_user
dp = Dispatcher()
dp = Dispatcher(storage=MemoryStorage()) 
dp.include_router(start.router)
dp.include_router(main_menu_handlers.router)
dp.include_router(buy_vpn_handlers.router)
dp.include_router(go_back.router)
dp.include_router(admin_menu.router)
dp.include_router(status_handlers.router)
dp.include_router(send_to_user.router)