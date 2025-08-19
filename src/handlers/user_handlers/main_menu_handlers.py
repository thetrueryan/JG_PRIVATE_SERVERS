from aiogram import F, Router
from aiogram.types import Message

from core.settings import ADMIN_TG_USERNAME

router = Router()


@router.message(F.text == "🗣️ Обратная связь")
async def cmd_feedback(message: Message):
    await message.answer(text=f"💬 Задавайте вопросы сюда: {ADMIN_TG_USERNAME}")
