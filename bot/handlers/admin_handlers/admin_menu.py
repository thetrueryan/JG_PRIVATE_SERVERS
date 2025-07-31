from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import VPNOrder
from config.settings import ADMIN_TG_ID
from bot.keyboards.admin_keyboard.admin_menu_keyboard import admin_menu_keyboard, admin_waiting_keyboard, admin_continue_keyboard
from bot.keyboards.user_keyboard.back_keyboard import back_button
from db.repositories.core import AsyncCore

router = Router()

@router.message(Command("admin"))
async def cmd_admin_menu(message: Message, state: FSMContext):
    if message.from_user:
            telegram_id = message.from_user.id
            admin_id_int = int(ADMIN_TG_ID)
            if telegram_id == admin_id_int:
                await state.update_data(prev="main_menu")
                await message.answer(text="🔑 <u><b>Админ меню</b></u>\n\nВыберите команду", reply_markup=admin_menu_keyboard())
                await state.set_state(VPNOrder.admin_menu)
            else:
                pass

@router.message(VPNOrder.admin_menu, F.text == "Отправить файл конфигурации")
async def cmd_send_telegram_id(message: Message, state: FSMContext):
    await message.answer("Пришлите telegram_id пользователя которому хотите отправить файл конфигурации", reply_markup=back_button())
    await state.set_state(VPNOrder.send_tg_id)

@router.message(VPNOrder.send_tg_id, F.text != "↩️ Назад")
async def cmd_check_sended_tg_id(message: Message, state: FSMContext):
    if message.from_user:
        tg_id = message.text
        if tg_id:
            try:
                tg_id_int = int(tg_id)
                if tg_id_int:
                    user = await AsyncCore.get_user_by_tg_id(tg_id_int)
                    if user:
                        await state.update_data(prev=VPNOrder.admin_menu)
                        await state.update_data(tg_id_to_send_config=tg_id_int)
                        await state.set_state(VPNOrder.send_conf)
                        await message.answer(text=f"Пользователь с i {tg_id_int} успешно найден! Нажмите продолжить чтобы перейти к загрузке файла", reply_markup=admin_continue_keyboard())
                    else:
                        await message.answer(text=f"Пользователь с id {tg_id_int} не найден!")
                        return
            except:
                await message.answer(text="telegram id пользователя должен быть числом!")
                return
        else:
            await message.answer(text="Сообщение с id пользователя не найдено!")
            return
        
@router.message(VPNOrder.send_conf, F.text != "↩️ Назад")
async def cmd_send_config_file(message: Message, state: FSMContext):
    await message.answer("Отправьте файл конфигурации для пользователя", reply_markup=back_button())
    await state.update_data(prev=VPNOrder.send_conf)
    await state.set_state(VPNOrder.check_conf)
    
@router.message(VPNOrder.check_conf, F.text != "↩️ Назад")
async def cmd_check_config_file(message: Message, state: FSMContext):
    if message.from_user:
        if message.document:
            if message.document.file_name:
                if message.document.file_name.endswith(('.ovpn')):
                    if message.document.file_size:
                        if message.document.file_size > 5 * 1024 * 1024:
                            await message.answer("Файл слишком большой. Максимальный размер - 5MB")
                            return
                        else:
                            await state.update_data(
                                file_id=message.document.file_id,
                                file_name=message.document.file_name
                            )   
                            await state.set_state(VPNOrder.waiting_for_continue)
                            await message.answer("Файл конфигурации успешно принят! Нажмите продолжить чтобы перейти к отправке", reply_markup=admin_continue_keyboard())
                else:
                    await message.answer("Недопустимый формат файла")
                    return
        else:
            await message.answer("Отправьте конфиг файл!")    
            return


@router.message(VPNOrder.waiting_for_continue, F.text != "↩️ Назад")
async def cmd_wait_for_continue(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Нажмите <b>'отправить'</b>, чтобы отправить файл конфигурации пользовтелю с telegram_id: {data["tg_id_to_send_config"]}", reply_markup=admin_waiting_keyboard())
    await state.update_data(prev=VPNOrder.send_conf)
    await state.set_state(VPNOrder.send_file_to_user)

@router.message(VPNOrder.send_file_to_user, F.text == "✅ ОТПРАВИТЬ")
async def cmd_send_file_to_user(message: Message, state: FSMContext):
    data = await state.get_data()
    file_id = data["file_id"]
    tg_id = data["tg_id_to_send_config"]
    try:
        if message.bot:
            await message.bot.send_document(chat_id=tg_id, document=file_id, caption=f"🔑 <b>Ваш файл конфигурации</b>\n")
            await message.answer("Файл успешно отправлен!")
    except Exception as e:
        await message.answer(f"Произошла ошибка при отправке файла: {e}")
    await state.clear()