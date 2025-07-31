from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отправить файл конфигурации"),
        KeyboardButton(text="Написать пользователю по TG_ID"),
        KeyboardButton(text="↩️ Назад"),
    )
    return builder.as_markup(resize_keyboard=True)

def admin_waiting_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="✅ ОТПРАВИТЬ"),
        KeyboardButton(text="↩️ Назад"),
    )
    return builder.as_markup(resize_keyboard=True)

def admin_continue_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="✅ ПРОДОЛЖИТЬ"),
        KeyboardButton(text="↩️ Назад"),
    )
    return builder.as_markup(resize_keyboard=True)
