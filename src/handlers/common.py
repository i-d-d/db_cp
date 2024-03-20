from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from settings import settings
from handlers.states import Mode
import db_utils

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    kb = [
        [
            types.KeyboardButton(text="Гость"),
            types.KeyboardButton(text="Посетитель"),
            types.KeyboardButton(text="Администратор"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите режим работы'
    )
    await message.answer(
        text='Выберите, какой режим вы хотите: ',
        reply_markup=keyboard
    )


@router.message(F.text.lower() == "гость")
async def guest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_mode = message.text.lower())
    await message.answer(text="Вы выбрали гостевой режим. В нём Вам доступен лишь просмотр перечня всех курсов по команде /courses",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Mode.guest_chosen)


@router.message(F.text.lower() == "посетитель")
async def client_chosen(message: Message, state: FSMContext):
    await state.set_state(Mode.choosing_id)
    await message.answer(text="Пожалуйста, введите номер вашей членской карты",
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text.regexp('\d{4}'), Mode.choosing_id)
async def client_typed_number(message: Message, state: FSMContext):
    if db_utils.client_exists(int(message.text)):
        await state.update_data(chosen_mode = 'посетитель')
        await state.update_data(client_id = int(message.text))
        await message.answer(text="Вы выбрали режим посетителя. В нём Вы можете \n"\
                             " * посмотреть информацию о себе с помощью /me\n"
                             " * посмотреть свои курсы комадой /my_courses\n"\
                             " * увидеть перечень всех курсов с помощью /courses\n"\
                             " * узнать, когда будет следующее занятие с помощью /next\n"\
                             " * получить информацию о Ваших преподавателях, используя /my_teachers\n"\
                             " * записаться на новый курс с помощью /signup '<Название Курса>'\n"\
                             " * перестать посещать курс командой /quit '<Название Курса>'",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Mode.client_chosen)
    else:
        await message.answer(text="Пользователя с таким номером карты не существует. Попробуйте ещё раз",
                             reply_markup=ReplyKeyboardRemove())


@router.message(Mode.choosing_id)
async def client_typed_text(message: Message, state: FSMContext):
    await message.answer(text="Введите, пожалуйста, правильный номер карты (формат: XXXX)",
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == 'администратор')
async def client_chose_admin(message: Message, state: FSMContext):
    await state.set_state(Mode.choosing_admin)
    await message.answer(text="Пожалуйста, введите пароль администратора",
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text == settings.admin_pass, Mode.choosing_admin)
async def correct_password(message: Message, state: FSMContext):
    await state.set_state(Mode.admin_chosen)
    await message.answer(text="Вы вошли как администратор. Вам доступны следующие команды:\n"\
                             " - /clients - посмотреть информацию обо всех клиентах\n"\
                             " - /teachers - посмотреть информацию обо всех преподавателях\n"\
                             " - /add_client - добавить нового клиента\n"\
                             " - /del_client - удалить клиента\n"\
                             " - /add_course - добавить новый мастер-класс\n"\
                             " - /del_course - удалить мастер-класс\n"\
                             " - /add_teacher - добавить нового преподавателя\n"\
                             " - /fire - удалить преподавателя\n"\
                             " - /raise - повысить зарплату преподавателю\n"\
                             " - /income - посмотреть ожидаемый доход за неделю\n",
                         reply_markup=ReplyKeyboardRemove())


@router.message(Mode.choosing_admin)
async def incorrect_password(message: Message, state: FSMContext):
    await state.clear()
    kb = [
        [
            types.KeyboardButton(text="Гость"),
            types.KeyboardButton(text="Посетитель"),
            types.KeyboardButton(text="Администратор"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите режим работы'
    )
    await message.answer(
        text='Пароль неверный. Выберите, какой режим вы хотите: ',
        reply_markup=keyboard
    )

@router.message(StateFilter(None), Command("exit"))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("exit"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Вы вышли из режима управления данными. Можете снова начать с выбора режима с помощью /start",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    await message.answer(text = "Для начала выберите режим доступа (/start)")


@router.message(Command("help"), Mode.choosing_admin)
async def cmd_help(message: Message):
    await message.answer(text = "Введите пароль",
                         reply_markup=ReplyKeyboardRemove())
    


@router.message(Command("help"), Mode.choosing_id)
async def cmd_help(message: Message):
    await message.answer(text = "Введите номер карты",
                         reply_markup=ReplyKeyboardRemove())
    

@router.message(Command("help"), Mode.guest_chosen)
async def cmd_help(message: Message):
    await message.answer(text="Вы выбрали гостевой режим. В нём Вам доступен лишь просмотр перечня всех курсов по команде /courses",
                         reply_markup=ReplyKeyboardRemove())
    

@router.message(Command("help"), Mode.client_chosen)
async def cmd_help(message: Message):
    await message.answer(text="Вы выбрали режим посетителя. В нём Вы можете \n"\
                             " * посмотреть информацию о себе с помощью /me\n"
                             " * посмотреть свои курсы комадой /my_courses\n"\
                             " * увидеть перечень всех курсов с помощью /courses\n"\
                             " * узнать, когда будет следующее занятие с помощью /next\n"\
                             " * получить информацию о Ваших преподавателях, используя /my_teachers\n"\
                             " * записаться на новый курс с помощью /signup '<Название Курса>'\n"\
                             " * перестать посещать курс командой /quit '<Название Курса>'",
                             reply_markup=ReplyKeyboardRemove())
    


@router.message(Command("help"), Mode.admin_chosen)
async def cmd_help(message: Message):
    await message.answer(text="Вы вошли как администратор. Вам доступны следующие команды:\n"\
                             " - /clients - посмотреть информацию обо всех клиентах\n"\
                             " - /teachers - посмотреть информацию обо всех преподавателях\n"\
                             " - /add_client - добавить нового клиента\n"\
                             " - /del_client - удалить клиента\n"\
                             " - /add_course - добавить новый мастер-класс\n"\
                             " - /del_course - удалить мастер-класс\n"\
                             " - /add_teacher - добавить нового преподавателя\n"\
                             " - /fire - удалить преподавателя\n"\
                             " - /raise - повысить зарплату преподавателю\n"\
                             " - /income - посмотреть ожидаемый доход за неделю\n",
                         reply_markup=ReplyKeyboardRemove())
    




