from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from bot.keyboards.user_keyboard.keyboard_captions import captions
from bot.keyboards.user_keyboard.status_keyboard import status_menu, continue_menu
from bot.keyboards.user_keyboard.back_keyboard import back_button
from bot.keyboards.user_keyboard.buy_vpn_keyboard import select_period_menu, select_payment_menu, inline_payment_menu
from datetime import datetime
from db.repositories.core import AsyncCore
from bot.states import VPNOrder
from payment.crypto_invoice import get_crypto_invoice
from payment.calculate import calculate_extend_order_price, calculate_duration
from payment.check_invoice_status import check_invoice_status_loop
from scripts.admin import send_order_info_to_admin

router = Router()

@router.message(F.text == "ℹ️ Статус")
async def cmd_status_menu(message: Message, state: FSMContext):
    await state.update_data(prev="main_menu")
    if message.from_user:
        tg_id = message.from_user.id
        result = await AsyncCore.get_orders_by_tg_id(tg_id)
        await message.answer("<b>Статус пользователя</b>")
        if result:
            orders_id_list = []
            message_text = []
            for user in result:
                    for order in user.paid_orders:
                        orders_id_list.append(order.id)
                        
                        current_date = datetime.utcnow()
                        days_to_expire = (order.expires_at - current_date).days
                        current_date.strftime("%d.%m.%Y")
                        exires_date = order.expires_at.strftime("%d.%m.%Y")
                        paid_date = order.paid_at.strftime("%d.%m.%Y")
                        message_text.append(f"Цена: {order.price} Руб.\nДата оплаты: {paid_date}\nДата окончания: {exires_date}\nДней до истечения: {days_to_expire}")
            order_number = 1
            for order in message_text:
                await message.answer(f"<u>✅Заказ #{order_number}:</u>\n{order}")
                order_number += 1
            await message.answer(text="❗️Вы можете продлить срок действия заказа нажав оплатить❗️",reply_markup=status_menu())
        else:
            await message.answer("❗️Приобретите сервера для просмотра статуса❗️")
    await state.update_data(orders_ids=orders_id_list)
    await state.set_state(VPNOrder.status)

@router.message(VPNOrder.status, F.text != "↩️ Назад")
async def cmd_select_order_to_pay(message: Message, state: FSMContext):
    await state.update_data(prev=VPNOrder.status)
    if message.from_user:
        tg_id = message.from_user.id
        result = await AsyncCore.get_orders_by_tg_id(tg_id)
        if result:
            orders_id_list = []
            for user in result:
                for order in user.paid_orders:
                    orders_id_list.append(order.id)
            await message.answer(text="Введите номер заказа для оплаты (например 1)", reply_markup=back_button())
            await state.set_state(VPNOrder.select_order)

@router.message(VPNOrder.select_order, F.text != "↩️ Назад")
async def cmd_select_order_number_in_status_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    orders = data.get("orders_ids")

    if not orders:
        await message.answer("❌ Список заказов не найден.")
        return
    
    if not message.text:
        await message.answer("❌ Заказ для оплаты не найден")
        return
    
    user_input = message.text.strip()
     
    if not user_input.isdigit():
        await message.answer("❌ Введите корректный номер заказа (например: 1).")
        return   
    
    index = int(user_input) - 1
    if index < 0 or index >= len(orders):
        await message.answer("❌ Заказ с таким номером не найден.")
        return

    order_id = orders[index]
    await state.update_data(selected_order_id=order_id)
    await message.answer(f"Заказ #{user_input} выбран.\nНажмите <b>Продлжить</b> для выбора срока", reply_markup=continue_menu())
    await state.update_data(order_number=user_input)
    await state.set_state(VPNOrder.check_select_order)

@router.message(VPNOrder.check_select_order, F.text != "↩️ Назад")
async def cmd_select_extend_period(message: Message, state: FSMContext):
    await state.update_data(prev=VPNOrder.select_order)
    await message.answer(text=captions["vpn_select_period"], reply_markup=select_period_menu())
    await state.set_state(VPNOrder.extend_period)

@router.message(VPNOrder.extend_period, F.text != "↩️ Назад")
async def cmd_select_extend_payment(message: Message, state: FSMContext):
    await state.update_data(period=message.text)
    await state.update_data(prev=VPNOrder.extend_period)
    await message.answer(text="Выберите тип оплаты", reply_markup=select_payment_menu())
    await state.set_state(VPNOrder.extend_payment)

@router.message(VPNOrder.extend_payment, F.text != "↩️ Назад")
async def cmd_crypto_invoice(message: Message, state: FSMContext):
    await state.update_data(extend_payment=message.text)
    await state.update_data(prev=VPNOrder.extend_payment)
    if message.from_user:
        telegram_id = message.from_user.id
        data = await state.get_data()
        order_id = data.get("selected_order_id")
        order_number = data.get("order_number")
        if isinstance(order_id, int):
            order = await AsyncCore.get_order_by_id(order_id)
            if order:
                old_price = order.price
                old_months = order.duration_months
                new_price = await calculate_extend_order_price(old_price, old_months, data)
                new_months = await calculate_duration(data)
                if new_price:
                    invoice = await get_crypto_invoice(new_price)
                    if invoice:
                        invoice_id = invoice.invoice_id
                        order_id = order.id
                        payment_url = invoice.bot_invoice_url
                        await state.set_state(VPNOrder.extend_waiting_payment)
                        await message.answer(text=f"Заказ # {order_number}: Продление аренды")
                        await message.answer(text=f"Всего к оплате: {new_price:.2f} руб.")
                        await message.answer("👇 Нажмите, чтобы перейти к оплате (после совершения оплаты нажмите проверить оплату):", reply_markup=inline_payment_menu(payment_url, invoice_id))
                        await message.answer("❗️<b>Оплатите заказ в течении 15 минут </b>❗️", reply_markup=back_button())
                        success_status = await check_invoice_status_loop(invoice)
                        if success_status == "paid":
                            await AsyncCore.updaid_expired_order(order_id, new_price, invoice_id, "paid", True, new_months)
                            await message.answer(text=f"✅ Оплата прошла успешно!\nАренда сервера продлена на {new_months} месяца!\nДля связи: @ttryan")
                            await send_order_info_to_admin(
                                f"<u>Заказ # {order_id} Продлен</u>: Сумма оплаты: {new_price}, срок: {new_months}\n",
                                f"invoice_id: {invoice_id}\ntelegram_user_id: {telegram_id}\n",
                                )
                        else:      
                            await message.answer(text="❌ Срок оплаты просрочен!")
        else:
            await message.answer("❌ Не удалось получить ссылку для оплаты")