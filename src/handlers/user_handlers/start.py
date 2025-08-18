from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from utils.main_keyboard import main_menu
from core.logger import logger
from repositories.bot_repository import BotRepo

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(price=0)
    if message.from_user:
        try:
            telegram_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            await BotRepo.add_user(telegram_id, username, first_name, last_name)
        except IntegrityError as e:
            logger.info(
                f"IntegrityError: Пользователь с id: {telegram_id} уже есть в базе"
            )
    await message.answer(text="☑️ Выберите действие", reply_markup=main_menu())
    await state.update_data(prev=await state.get_state())
    await state.set_state("main_menu")
