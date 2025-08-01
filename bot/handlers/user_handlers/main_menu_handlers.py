from aiogram import F, Router
from aiogram.types import FSInputFile, Message

router = Router()


@router.message(F.text == "🗣️ Обратная связь")
async def cmd_feedback(message: Message):
    banner = FSInputFile("./bot/images/feedback_banner.png")
    await message.answer_photo(banner, caption="💬 Задавайте вопросы сюда: @ttryan")
