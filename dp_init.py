from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, main_menu_handlers, buy_vpn_handlers, go_back

dp = Dispatcher()
dp = Dispatcher(storage=MemoryStorage()) 
dp.include_router(start.router)
dp.include_router(main_menu_handlers.router)
dp.include_router(buy_vpn_handlers.router)
dp.include_router(go_back.router)