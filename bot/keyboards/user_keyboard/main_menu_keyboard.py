from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🛒 Купить сервер"),
    )
    builder.row(
        KeyboardButton(text="ℹ️ Статус"),
        KeyboardButton(text="🗣️ Обратная связь")
    )
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Кто такой Джон Голт?")