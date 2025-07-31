from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отправить файл конфигурации или сообщение"),
    )
    builder.row(
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
        KeyboardButton(text="Отправить пользователю конфиг"),
    )
    builder.row(
        KeyboardButton(text="Отправить пользователю текстовое сообщение")
    )
    builder.row(
        KeyboardButton(text="↩️ Назад"),
    )
    return builder.as_markup(resize_keyboard=True)
