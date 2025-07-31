from aiogram.fsm.state import State, StatesGroup

class VPNOrder(StatesGroup):
    # status states
    status = State()
    select_order = State()
    check_select_order = State()
    extend_period = State()
    extend_payment = State()
    extend_waiting_payment = State()

    # buy new server states
    country = State()
    vpn_type = State()
    traffic = State()
    period = State()
    payment = State()
    confirm = State()
    price = State()
    waiting_payment = State()

    # admin states users
    admin_menu = State()
    send_tg_id = State()
    send_conf = State()
    check_conf = State()
    waiting_for_continue = State()
    send_file_to_user = State()
    check_message = State()
    send_message_to_user = State()

    #admin states servers
    send_server_info = State()
    add_server = State()