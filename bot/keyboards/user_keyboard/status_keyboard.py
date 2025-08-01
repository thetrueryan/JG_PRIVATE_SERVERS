from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def status_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="💰 Оплатить"), KeyboardButton(text="↩️ Назад"))
    return builder.as_markup(resize_keyboard=True)


def continue_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ Продолжить"), KeyboardButton(text="↩️ Назад"))
    return builder.as_markup(resize_keyboard=True)
