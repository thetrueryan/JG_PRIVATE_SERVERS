from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from sqlalchemy.exc import IntegrityError

from bot.keyboards.user_keyboard.main_menu_keyboard import main_menu
from config.logger import logger
from db.repositories.core import AsyncCore

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(price=0)
    banner = FSInputFile("./bot/images/main_banner.png")
    if message.from_user:
        try:
            telegram_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            await AsyncCore.add_user(telegram_id, username, first_name, last_name)
        except IntegrityError as e:
            logger.info(
                f"IntegrityError: Пользователь с id: {telegram_id} уже есть в базе"
            )
    await message.answer_photo(
        banner, caption="☑️ Выберите действие", reply_markup=main_menu()
    )
    await state.update_data(prev=await state.get_state())
    await state.set_state("main_menu")
