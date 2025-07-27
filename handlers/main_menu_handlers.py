from aiogram.types import Message, FSInputFile
from aiogram import F, Router


router = Router()

@router.message(F.text == "🗣️ Обратная связь")
async def cmd_feedback(message: Message):
    banner = FSInputFile("./images/feedback_banner.png")
    await message.answer_photo(banner, caption="💬 Задавайте вопросы сюда: @ttryan")

@router.message(F.text == "🧾 Как пользоваться?")
async def cmd_guide_for_use(message: Message):
    banner = FSInputFile("./images/guide_banner.png")
    await message.answer_photo(banner, caption="☑️ Гайд по использованию: 'link'")

@router.message(F.text == "❓ Помощь")
async def cmd_help(message: Message):
    banner = FSInputFile("./images/help_banner.png")
    await message.answer_photo(banner, caption="☑️ ответы на вопросы: ")