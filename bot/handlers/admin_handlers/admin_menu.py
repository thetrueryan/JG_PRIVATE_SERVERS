from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config.settings import ADMIN_TG_ID

router = Router()

@router.message(Command("admin"))
async def cmd_admin_menu(message: Message, state: FSMContext):
    if message.from_user:
            telegram_id = message.from_user.id
            admin_id_int = int(ADMIN_TG_ID)
            if telegram_id == admin_id_int:
                await message.answer(text="Админ меню")
            else:
                pass