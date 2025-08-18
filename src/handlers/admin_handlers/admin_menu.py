from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.admin_menu_keyboard import admin_menu_keyboard
from core.states import VPNOrder
from core.settings import ADMIN_TG_ID

router = Router()


@router.message(Command("admin"))
async def cmd_admin_menu(message: Message, state: FSMContext):
    if message.from_user:
        telegram_id = message.from_user.id
        admin_id_int = int(ADMIN_TG_ID)
        if telegram_id == admin_id_int:
            await state.update_data(prev="main_menu")
            await message.answer(
                text="🔑 <u><b>Админ меню</b></u>\n\nВыберите команду",
                reply_markup=admin_menu_keyboard(),
            )
            await state.set_state(VPNOrder.admin_menu)
        else:
            pass
