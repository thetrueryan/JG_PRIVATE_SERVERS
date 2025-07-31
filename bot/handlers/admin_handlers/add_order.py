from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import VPNOrder
from config.settings import ADMIN_TG_ID
from bot.keyboards.admin_keyboard.admin_menu_keyboard import admin_menu_keyboard, admin_waiting_keyboard, admin_continue_keyboard, admin_order_add_type_keyboard
from bot.keyboards.user_keyboard.back_keyboard import back_button
from db.repositories.core import AsyncCore

router = Router()


@router.message(VPNOrder.admin_menu, F.text == "Добавить ордер")
async def select_add_type(message: Message, state: FSMContext):
    await message.answer("Выберите, добавить новый ордер или обновить существующий", reply_markup=admin_order_add_type_keyboard())
    await state.set_state(VPNOrder.select_order_add_type)

@router.message(VPNOrder.select_order_add_type, F.text == "Добавить новый ордер")
async def info_new_order(message: Message, state: FSMContext):
    await message.answer("Скопируйте информацию для добавления из сообщения которое было отправлено вам после оформления ордера пользователем", reply_markup=back_button())
    await state.set_state(VPNOrder.add_order)

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
                        await AsyncCore.add_order(user_id, price, duration)
                        await AsyncCore.update_paid_status(user_id=user_id, status_name="paid", paid_at=True, expired_at=True)
                        await message.answer("Ордер успешно добавлен!")
            except Exception as e:
                await message.answer(f"Не получилось добавить ордер по причине {e}")
                