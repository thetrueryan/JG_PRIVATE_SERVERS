from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "🗣️ Обратная связь")
async def cmd_feedback(message: Message):
    await message.answer(text="💬 Задавайте вопросы сюда: @ttryan")
