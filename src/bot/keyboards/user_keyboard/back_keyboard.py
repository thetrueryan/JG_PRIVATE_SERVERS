from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def back_button():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="↩️ Назад"))
    return builder.as_markup(resize_keyboard=True)
