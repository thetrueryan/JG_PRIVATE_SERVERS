from aiogram.fsm.state import State, StatesGroup

class VPNOrder(StatesGroup):
    country = State()
    vpn_type = State()
    traffic = State()
    period = State()
    payment = State()
    confirm = State()
    price = State()
    waiting_payment = State()