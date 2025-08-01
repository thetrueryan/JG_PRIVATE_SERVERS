from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import VPNOrder
from config.settings import ADMIN_TG_ID
from bot.keyboards.admin_keyboard.admin_menu_keyboard import (
    admin_menu_keyboard,
    admin_waiting_keyboard,
    admin_continue_keyboard,
)
from bot.keyboards.user_keyboard.back_keyboard import back_button
from db.repositories.core import AsyncCore

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
