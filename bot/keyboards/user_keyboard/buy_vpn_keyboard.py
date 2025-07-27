from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def select_country_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🇫🇮 Финляндия"),
        KeyboardButton(text="🇫🇷 Франция"),
    )
    builder.row(
        KeyboardButton(text="🇺🇸 США"),
        KeyboardButton(text="🇮🇳 Индия")
    )
    builder.row(
        KeyboardButton(text="↩️ Назад")
    )
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Кто такой Джон Голт?")


def select_vpn_type_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🛡️ OpenVPN"),
    )
    builder.row(
        KeyboardButton(text="↩️ Назад")
    )
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Кто такой Джон Голт?")


def select_traffic_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="⚡ 50 mb/s"),
        KeyboardButton(text="🚀 1.0 gb/s")
    )
    builder.row(
        KeyboardButton(text="↩️ Назад")
    )
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Кто такой Джон Голт?")


def select_period_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="⏳ 1 месяц"),
        KeyboardButton(text="⏳ 3 месяца"),
        KeyboardButton(text="⏳ 6 месяцев"),
    )
    builder.row(
        KeyboardButton(text="↩️ Назад")
    )
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Кто такой Джон Голт?")


def select_payment_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="💎 Cryptobot"),
        KeyboardButton(text="💵 Fiat")
    )
    builder.row(
        KeyboardButton(text="↩️ Назад")
    )
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Кто такой Джон Голт?")


def back_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="↩️ Назад")
    )
    return builder.as_markup(resize_keyboard=True)


def inline_payment_menu(payment_url: str, invoice_id: int):
    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💰 Оплатить", url=payment_url)
            ],
            [
                InlineKeyboardButton(text="Проверить оплату",
                                     callback_data=f"check_payment:{invoice_id}"
                                     ),
            ]
        ]
    )
    
    return builder