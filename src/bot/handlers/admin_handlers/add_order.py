from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.admin_keyboard.admin_menu_keyboard import (
    admin_order_add_type_keyboard,
)
from bot.keyboards.user_keyboard.back_keyboard import back_button
from bot.states import VPNOrder
from config.settings import ADMIN_TG_ID
from db.repositories.core import AsyncCore

router = Router()


@router.message(VPNOrder.admin_menu, F.text == "Добавить ордер")
async def select_add_type(message: Message, state: FSMContext):
    await message.answer(
        "Выберите, добавить новый ордер или обновить существующий",
        reply_markup=admin_order_add_type_keyboard(),
    )
    await state.set_state(VPNOrder.select_order_add_type)


@router.message(VPNOrder.select_order_add_type, F.text == "Добавить новый ордер")
async def info_new_order(message: Message, state: FSMContext):
    await message.answer(
        "Скопируйте информацию для добавления из сообщения которое было отправлено вам после оформления ордера пользователем",
        reply_markup=back_button(),
    )
    await state.set_state(VPNOrder.add_order)


@router.message(VPNOrder.select_order_add_type, F.text == "Обновить существующий")
async def info_old_order(message: Message, state: FSMContext):
    await message.answer(
        "Скопируйте информацию для обновления из сообщения которое было отправлено вам после продления ордера пользователем",
        reply_markup=back_button(),
    )
    await state.set_state(VPNOrder.update_order)


@router.message(VPNOrder.add_order, F.text != "↩️ Назад")
async def add_new_order(message: Message, state: FSMContext):
    if message.from_user:
        if message.text:
            try:
                order_params = message.text.split()
                if len(order_params) == 3:
                    telegram_id = int(order_params[0])
                    price = float(order_params[1])
                    duration = int(order_params[2])
                    user_id = await AsyncCore.get_user_by_tg_id(telegram_id)
                    if user_id:
                        order_id = await AsyncCore.add_order(
                            user_id, price, duration, return_id=True
                        )
                        await AsyncCore.update_paid_status(
                            order_id=order_id,
                            status_name="paid",
                            paid_at=True,
                            expired_at=True,
                        )
                        await message.answer("Ордер успешно добавлен!")
            except Exception as e:
                await message.answer(f"Не получилось добавить ордер по причине {e}")


@router.message(VPNOrder.update_order, F.text != "↩️ Назад")
async def update_old_order(message: Message, state: FSMContext):
    if message.from_user:
        if message.text:
            try:
                order_params = message.text.split()
                if len(order_params) == 4:
                    order_id = int(order_params[0])
                    new_price = float(order_params[1])
                    status = order_params[2]
                    new_duration = int(order_params[3])
                    await AsyncCore.updaid_expired_order(
                        order_id=order_id,
                        new_price=new_price,
                        status_name=status,
                        paid_at=True,
                        new_duration=new_duration,
                    )
                    await message.answer("Ордер успешно обновлен!")
            except Exception as e:
                await message.answer(f"Не получилось обновить ордер по причине {e}")
