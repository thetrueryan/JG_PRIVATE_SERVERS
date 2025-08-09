from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.admin_keyboard.admin_menu_keyboard import admin_add_server_keyboard
from bot.keyboards.user_keyboard.back_keyboard import back_button
from bot.states import VPNOrder
from db.repositories.core import AsyncCore

router = Router()


@router.message(VPNOrder.admin_menu, F.text == "Добавить сервер")
async def cmd_info_server(message: Message, state: FSMContext):
    await message.answer(
        "Введите информацию о сервере который хотите добавить\nФормат: страна тип_впн трафик стоимость_аренды_в_месяц(на хостинге) tg_user_id(необязательно)\nВводите все данные через пробел, без запятых"
    )
    await state.set_state(VPNOrder.send_server_info)


@router.message(VPNOrder.send_server_info, F.text != "↩️ Назад")
async def cmd_check_server_params(message: Message, state: FSMContext):
    if message.from_user:
        if message.text:
            try:
                params_list = message.text.split()
                if len(params_list) >= 4:
                    params = {
                        "country": params_list[0],
                        "vpn_type": params_list[1],
                        "traffic": params_list[2],
                        "price_per_day": int(params_list[3]),
                    }
                    if len(params_list) == 5:
                        params.update({"tg_user_id": int(params_list[4])})
                    await message.answer(
                        f"Данные для ввода в таблицу:\n{params}\n\n Нажмите ✅ ДОБАВИТЬ Чтобы добавить сервер в таблицу",
                        reply_markup=admin_add_server_keyboard(),
                    )
                    await state.update_data(server_params=params)
                    await state.set_state(VPNOrder.add_server)
                else:
                    await message.answer("Вы ввели не все обязательные параметры!")
                    return

            except Exception as e:
                await message.answer(
                    f"Не удалось получить данные о сервере по ошибке: <b>{e}</b>"
                )
                return


@router.message(VPNOrder.add_server, F.text == "✅ ДОБАВИТЬ")
async def cmd_add_server(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        params = data["server_params"]
        if params:
            country = params["country"]
            vpn_type = params["vpn_type"]
            traffic = params["traffic"]
            price_per_day = params["price_per_day"]
            user_id = None
            if params["tg_user_id"]:
                tg_user_id = params["tg_user_id"]
                user_id = await AsyncCore.get_user_by_tg_id(tg_user_id)
            await AsyncCore.add_server(
                country, vpn_type, traffic, price_per_day, user_id
            )
            await message.answer(
                "Сервер успешно добавлен в таблицу!", reply_markup=back_button()
            )
    except Exception as e:
        await message.answer(
            f"Не удалось добавить сервер в таблицу по ошибке: <b>{e}</b>"
        )
