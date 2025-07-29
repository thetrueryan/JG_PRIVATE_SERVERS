from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from bot.states import VPNOrder
from bot.keyboards.user_keyboard.buy_vpn_keyboard import (
    select_country_menu, 
    select_vpn_type_menu,
    select_traffic_menu,
    select_period_menu,
    select_payment_menu,
    inline_payment_menu,
    back_menu,
    )
from bot.keyboards.user_keyboard.keyboard_captions import captions
from payment.calculate import calculate_price, calculate_duration
from payment.check_invoice_status import check_invoice_status_loop
from payment.crypto_init import crypto
from payment.crypto_invoice import get_crypto_invoice
from db.repositories.core import AsyncCore
from scripts.admin import send_order_info_to_admin

router = Router()

@router.message(F.text == "🛒 Купить сервер")
async def cmd_select_vpn_country(message: Message, state: FSMContext):
    banner=FSInputFile("./bot/images/country_banner.png")
    await state.update_data(prev="main_menu")
    await message.answer_photo(banner, caption=captions["vpn_country"], reply_markup=select_country_menu())
    await state.set_state(VPNOrder.country)

@router.message(VPNOrder.country,  F.text != "↩️ Назад")
async def cmd_select_vpn_type(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    banner=FSInputFile("./bot/images/vpn_type_banner.png")
    await state.update_data(prev=VPNOrder.country)
    await message.answer_photo(banner, caption=captions["vpn_type"], reply_markup=select_vpn_type_menu())
    await state.set_state(VPNOrder.vpn_type)

@router.message(VPNOrder.vpn_type, F.text != "↩️ Назад")
async def cmd_select_traffic(message: Message, state: FSMContext):
    await state.update_data(vpn_type=message.text)
    banner = FSInputFile("./bot/images/traffic_banner.png")
    await state.update_data(prev=VPNOrder.vpn_type)
    await message.answer_photo(banner, caption=captions["vpn_traffic"], reply_markup=select_traffic_menu())
    await state.set_state(VPNOrder.traffic)

@router.message(VPNOrder.traffic, F.text != "↩️ Назад")
async def cmd_select_period(message: Message, state: FSMContext):
    await state.update_data(traffic=message.text)
    banner = FSInputFile("./bot/images/period_banner.png")
    await state.update_data(prev=VPNOrder.traffic)
    await message.answer_photo(banner, caption=captions["vpn_select_period"], reply_markup=select_period_menu())
    await state.set_state(VPNOrder.period)

@router.message(VPNOrder.period, F.text != "↩️ Назад")
async def cmd_select_payment(message: Message, state: FSMContext):
        await state.update_data(period=message.text)
        banner = FSInputFile("./bot/images/payment_banner.png")
        await state.update_data(prev=VPNOrder.period)
        await message.answer_photo(banner, caption=captions["vpn_select_payment"], reply_markup=select_payment_menu())
        await state.set_state(VPNOrder.payment)

@router.message(VPNOrder.payment, F.text == "💎 Cryptobot")
async def cmd_crypto_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)
    await state.update_data(prev=VPNOrder.payment)
    data = await state.get_data()
    payment_type = data.get("payment")
    duration = await calculate_duration(data)
    total_price = await calculate_price(data)
    await message.answer(text=f"Всего к оплате: {total_price:.2f} руб.")
    if payment_type == "💎 Cryptobot":
        if isinstance(total_price, float) and isinstance(duration, int):
            if message.from_user:
                invoice = await get_crypto_invoice(total_price)
                invoice_id = invoice.invoice_id
                telegram_id = message.from_user.id
                if telegram_id:
                    user_id = await AsyncCore.get_user_by_tg_id(telegram_id)
                    if user_id:
                        await AsyncCore.add_order(user_id, invoice_id, total_price, duration)
                        payment_url = invoice.bot_invoice_url
                        if payment_url:
                            await state.update_data(payment_start_time=datetime.now().isoformat())
                            await state.set_state(VPNOrder.waiting_payment)
                            await message.answer(text=f"<u>Ваш заказ:</u>\n<b>Страна:</b> {data["country"]}\n<b>Тип VPN:</b> {data["vpn_type"]}\n<b>Трафик:</b> {data["traffic"]}\n<b>Срок аренды:</b> {data["period"]}")
                            await message.answer("👇 Нажмите, чтобы перейти к оплате (после совершения оплаты нажмите проверить оплату):", reply_markup=inline_payment_menu(payment_url, invoice.invoice_id))
                            await message.answer("❗️<b>Оплатите заказ в течении 15 минут </b>❗️", reply_markup=back_menu())
                            success_status = await check_invoice_status_loop(invoice)
                            if success_status == "paid":
                                await AsyncCore.update_paid_status(invoice_id, status_name="paid", paid_at=True, expired_at=True)
                                await message.answer(text="✅ Оплата прошла успешно!\nФайл подключения будет присалан в течении часа\nДля связи: @ttryan")
                                await send_order_info_to_admin(
                                    f"<u>Заказ</u>:\nСтрана: {data["country"]}\nТип VPN: {data["vpn_type"]}\nТрафик: {data["traffic"]}\nСрок аренды: {data["period"]}\n",
                                    f"invoice_id: {invoice_id}\ntelegram_user_id: {telegram_id}\npayment_type: {payment_type}\ntotal_price: {total_price:.2f}\n",
                                )
                            else:
                                await AsyncCore.update_paid_status(invoice_id, status_name="expired")        
                                await message.answer(text="❌ Срок оплаты просрочен!")
        else:              
            await message.answer("Не удалось получить ссылку на оплату")
     
@router.callback_query(F.data.startswith("check_payment:"))
async def cmd_check_crypto_payment_status(callback: CallbackQuery):
    if callback.data:
        try:
            invoice_id = int(callback.data.split(":")[1])
            invoices = await crypto.get_invoices(invoice_ids=[invoice_id])

            if not invoices:
                await callback.answer(f" Инвойс {invoice_id} не найден.")
                await callback.answer()
                return

            if isinstance(invoices, list):
                invoice = invoices[0]

            if invoice.status == "paid":
                await callback.answer(" Оплата подтверждена!")
            elif invoice.status == "expired":
                await callback.answer(" Инвойс просрочен.")
            else:
                await callback.answer(" Оплата пока не получена.")

            await callback.answer()

        except Exception as e:
            print(f"Ошибка при проверке инвойса: {e}")
            await callback.answer("Произошла ошибка при проверке оплаты ")

@router.message(VPNOrder.payment, F.text == "💵 Fiat")
async def cmd_fiat_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)
    await state.update_data(prev=await state.get_state())
    data = await state.get_data()
    payment_type = data.get("payment")
    total_price = await calculate_price(data)
    if payment_type == "💵 Fiat":
        await message.answer(text=f"Всего к оплате: {total_price:.2f}")
        await message.answer(text="Внимание, оплата в фиате сейчас в разработке\nДля оплаты фиатом просьба связяться со мной: @ttryan\n", reply_markup=back_menu())
