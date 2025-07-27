from aiogram.types import Message, FSInputFile
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from states import VPNOrder

from handlers.start import cmd_start
from handlers.buy_vpn_handlers import (
    cmd_select_vpn_country,
    cmd_select_vpn_type,
    cmd_select_traffic,
    cmd_select_period,
    cmd_select_payment,
    cmd_crypto_payment_link,
    cmd_fiat_payment,
)

PREV_COMMANDS = {
    VPNOrder.country.state: cmd_select_vpn_country,
    VPNOrder.vpn_type.state: cmd_select_vpn_type,
    VPNOrder.traffic.state: cmd_select_traffic,
    VPNOrder.period.state: cmd_select_period,
    VPNOrder.payment.state: cmd_select_payment,
    VPNOrder.waiting_payment: cmd_crypto_payment_link,
    "main_menu": cmd_start,
}
router = Router()

@router.message(F.text == "↩️ Назад")
async def cmd_go_back(message: Message, state: FSMContext):
    data = await state.get_data()
    prev = data.get("prev")
    print(prev)
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