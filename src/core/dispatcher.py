from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.admin_handlers import add_order, add_server, admin_menu, send_to_user
from handlers.user_handlers import (
    buy_vpn_handlers,
    go_back,
    main_menu_handlers,
    start,
    status_handlers,
)

dp = Dispatcher()
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start.router)
dp.include_router(main_menu_handlers.router)
dp.include_router(buy_vpn_handlers.router)
dp.include_router(go_back.router)
dp.include_router(admin_menu.router)
dp.include_router(status_handlers.router)
dp.include_router(send_to_user.router)
dp.include_router(add_server.router)
dp.include_router(add_order.router)
