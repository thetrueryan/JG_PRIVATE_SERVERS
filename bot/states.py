from aiogram.fsm.state import State, StatesGroup

class VPNOrder(StatesGroup):
    status = State()
    select_order = State()
    check_select_order = State()
    extend_period = State()
    extend_payment = State()
    extend_waiting_payment = State()


    country = State()
    vpn_type = State()
    traffic = State()
    period = State()
    payment = State()
    confirm = State()
    price = State()
    waiting_payment = State()