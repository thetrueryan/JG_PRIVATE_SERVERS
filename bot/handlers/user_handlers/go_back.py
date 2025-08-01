from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from bot.states import VPNOrder
from bot.handlers.user_handlers.start import cmd_start
from bot.handlers.user_handlers.buy_vpn_handlers import (
    cmd_select_vpn_country,
    cmd_select_vpn_type,
    cmd_select_traffic,
    cmd_select_period,
    cmd_select_payment,
    cmd_crypto_payment,
)
from bot.handlers.user_handlers.status_handlers import (
    cmd_status_menu,
    cmd_select_order_number_in_status_menu,
    cmd_select_order_to_pay,
    cmd_select_extend_period,
    cmd_select_extend_payment,
)
from bot.handlers.admin_handlers.admin_menu import cmd_admin_menu

PREV_COMMANDS = {
    "main_menu": cmd_start,
    "admin_menu": cmd_admin_menu,
    VPNOrder.country.state: cmd_select_vpn_country,
    VPNOrder.vpn_type.state: cmd_select_vpn_type,
    VPNOrder.traffic.state: cmd_select_traffic,
    VPNOrder.period.state: cmd_select_period,
    VPNOrder.payment.state: cmd_select_payment,
    VPNOrder.waiting_payment.state: cmd_crypto_payment,
    VPNOrder.status.state: cmd_start,
    VPNOrder.select_order.state: cmd_status_menu,
    VPNOrder.check_select_order.state: cmd_select_order_to_pay,
    VPNOrder.extend_period.state: cmd_select_order_number_in_status_menu,
    VPNOrder.extend_payment.state: cmd_select_extend_period,
    VPNOrder.extend_waiting_payment.state: cmd_select_extend_payment,
    VPNOrder.send_tg_id.state: cmd_admin_menu,
    VPNOrder.send_conf.state: cmd_admin_menu,
    VPNOrder.check_conf.state: cmd_admin_menu,
    VPNOrder.waiting_for_continue.state: cmd_admin_menu,
    VPNOrder.send_file_to_user.state: cmd_admin_menu,
    VPNOrder.check_message.state: cmd_admin_menu,
    VPNOrder.send_message_to_user.state: cmd_admin_menu,
    VPNOrder.send_server_info: cmd_admin_menu,
    VPNOrder.add_server: cmd_admin_menu,
}
router = Router()


@router.message(F.text == "↩️ Назад")
async def cmd_go_back(message: Message, state: FSMContext):
    data = await state.get_data()
    prev = data.get("prev")
    if prev:
        await state.set_state(prev)
        bot_func = PREV_COMMANDS.get(prev)
        if bot_func:
            await bot_func(message, state)
        else:
            await cmd_start(message, state)
    else:
        await state.clear()
        cmd_start(message, state)
