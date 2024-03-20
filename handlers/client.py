from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from handlers.states import Mode
import db_utils

router = Router()

@router.message(Command("courses"))
async def show_courses(message: Message, state: FSMContext):
    courses_list = db_utils.list_all_courses()
    result_message = "На данный момент доступны следующие курсы:\n\n";
    for course in courses_list:
        result_message += "Название: {0}\nЦена: {1}\nДень недели: {2}\nВремя начала: {3}\n\n".format(course[1], course[2], course[3], str(course[4]))
    await message.answer(text=result_message)



@router.message(Command("me"), Mode.client_chosen)
async def show_me(message: Message, state: FSMContext):
    user_data = await state.get_data()
    client = db_utils.get_client(user_data["client_id"])
    result_message = "Вы вошли как:\n\n"
    result_message += "Имя: {0}\nНомер карты: {1}\nНомер телефона: {2}\nУровень карты: {3}\nКоличество бонусов: {4}\n\n".format(client[1], client[0], client[2], client[3], client[4])
    await message.answer(text=result_message)


@router.message(Command("me"))
async def cant_show_me(message: Message):
    await message.answer("Для этой команды нужно войти как посетитель")


@router.message(Command("my_courses"), Mode.client_chosen)
async def show_chosen_courses(message: Message, state: FSMContext):
    user_data = await state.get_data()
    courses_list = db_utils.get_chosen_courses(user_data["client_id"])
    if not courses_list:
        result_message = "На данный момент вы не записаны на курсы"
    else:
        result_message = "На данный момент вы записаны на следующие курсы (цена указана со скидкой):\n\n"
        for course in courses_list:
            result_message += "Название: {0}\nЦена: {1}\nДень недели: {2}\nВремя начала: {3}\n\n".format(course[0], course[1], course[2], str(course[3]))
    await message.answer(text=result_message)


@router.message(Command("my_courses"))
async def cant_show_me(message: Message):
    await message.answer("Для этой команды нужно войти как посетитель")


@router.message(Command("next"), Mode.client_chosen)
async def show_chosen_courses(message: Message, state: FSMContext):
    user_data = await state.get_data()
    course = db_utils.get_closest_course(user_data["client_id"])
    if not course:
        result_message = "На данный момент вы не записаны на курсы"
    else:
        result_message = "Ближайшее занятие (цена указана со скидкой):\n\n";
        result_message += "Название: {0}\nЦена: {1}\nДень недели: {2}\nВремя начала: {3}\n\n".format(course[0], course[1], course[2], str(course[3]))
    await message.answer(text=result_message)


@router.message(Command("next"))
async def cant_show_me(message: Message):
    await message.answer("Для этой команды нужно войти как посетитель")


@router.message(Command("my_teachers"), Mode.client_chosen)
async def show_chosen_teachers(message: Message, state: FSMContext):
    user_data = await state.get_data()
    records = db_utils.get_all_selected_teachers(user_data["client_id"])
    if not records:
        result_message = "На данный момент вы не записаны на курсы"
    else:
        result_message = "Преподаватели ваших курсов:\n\n"
        for record in records:
            result_message += "Название курса: {0}\nФИО преподавателя: {1}\nТелефон преподавателя: {2}\nЭлектронная почта: {3}\nСтаж работы: {4}\n\n".format(record[0], record[1], record[2], record[3], record[4])
    await message.answer(text=result_message)


@router.message(Command("my_teachers"))
async def cant_show_me(message: Message):
    await message.answer("Для этой команды нужно войти как посетитель")


@router.message(Command("signup"), Mode.client_chosen)
async def show_chosen_teachers(message: Message, state: FSMContext, command: CommandObject):
    user_data = await state.get_data()
    if command.args is None:
        await message.answer("Ошибка: после /signup нужно передать название желаемого курса")
        return
    result_message = db_utils.signup_for_new_course(user_data["client_id"], command.args)
    await message.answer(text=result_message)



@router.message(Command("signup"))
async def cant_show_me(message: Message):
    await message.answer("Для этой команды нужно войти как посетитель")



@router.message(Command("quit"), Mode.client_chosen)
async def show_chosen_teachers(message: Message, state: FSMContext, command: CommandObject):
    user_data = await state.get_data()
    if command.args is None:
        await message.answer("Ошибка: после /quit нужно передать название желаемого курса")
        return
    result_message = db_utils.quit_course(user_data["client_id"], command.args)
    await message.answer(text=result_message)



@router.message(Command("quit"))
async def cant_show_me(message: Message):
    await message.answer("Для этой команды нужно войти как посетитель")