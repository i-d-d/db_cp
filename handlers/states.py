from aiogram.fsm.state import default_state, State, StatesGroup

class Mode(StatesGroup):
    choosing_admin = State()
    choosing_id = State()
    guest_chosen = State()
    client_chosen = State()
    admin_chosen = State()