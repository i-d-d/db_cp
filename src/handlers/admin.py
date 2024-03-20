from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from handlers.states import Mode
import db_utils

router = Router()

@router.message(Command("clients"), Mode.admin_chosen)
async def show_clients(message: Message):
    clients_list = db_utils.list_all_clients()
    result_message = "На данный момент курсы посещают следующие клиенты:\n\n";
    for client in clients_list:
        result_message += "Имя: {0}\nНомер карты: {1}\nНомер телефона: {2}\nУровень карты: {3}\nКоличество бонусов: {4}\n\n".format(client[1], client[0], client[2], client[3], client[4])
    await message.answer(text=result_message)


@router.message(Command("clients"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("teachers"), Mode.admin_chosen)
async def show_courses(message: Message):
    teachers_list = db_utils.list_all_teachers()
    result_message = "На данный момент наняты следующие преподаватели:\n\n";
    for teacher in teachers_list:
        result_message += "ФИО: {0}\nНомер сотрудника: {1}\nНомер телефона: {2}\nЭлектронная почта: {3}\nЗарплата: {4}\nСтаж работы: {5}\n\n".format(teacher[1], teacher[0], teacher[2], teacher[3], teacher[5], teacher[4])
    await message.answer(text=result_message)


@router.message(Command("teachers"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("add_client"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /add_client нужно передать данные клиента")
        return
    try:
        client_id, client_name, client_phone_number = command.args.split(', ')
    except ValueError:
        await message.answer(text="Ошибка: данные вводятся в формате <НомерКарты>, <Имя>, <Телефон>")
    
    result_message = db_utils.create_client(client_id, client_name, client_phone_number)
    await message.answer(text=result_message)


@router.message(Command("add_client"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("del_client"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /del_client нужно передать номер карты клиента")
        return
    client_id = command.args
    
    result_message = db_utils.delete_client(client_id)
    await message.answer(text=result_message)


@router.message(Command("del_client"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("add_course"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /add_course нужно передать данные курса")
        return
    try:
        course_id, course_name, cost, week_day, start_time = command.args.split(', ')
    except ValueError:
        await message.answer(text="Ошибка: данные вводятся в формате <НомерГруппы>, <Название>, <Цена>, <ДеньНедели>, <ВремяНачала>")
    
    result_message = db_utils.add_course(course_id, course_name, cost, week_day, start_time)
    await message.answer(text=result_message)


@router.message(Command("add_course"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")



@router.message(Command("add_teacher"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /add_teacher нужно передать данные преподавателя")
        return
    try:
        teacher_id, teacher_name, phone_number, email, experience, salary = command.args.split(', ')
    except ValueError:
        await message.answer(text="Ошибка: данные вводятся в формате <НомерПреподавателя>, <ФИО>, <Телефон>, <ЭлПочта>, <Стаж>, <Зарплата>")
    
    result_message = db_utils.add_teacher(teacher_id, teacher_name, phone_number, email, experience, salary)
    await message.answer(text=result_message)


@router.message(Command("add_teacher"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("fire"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /fire нужно передать номер преподавателя")
        return
    teacher_id = command.args
    
    result_message = db_utils.fire_teacher(teacher_id)
    await message.answer(text=result_message)


@router.message(Command("fire"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("del_course"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /del_course нужно передать номер группы")
        return
    group_id = command.args
    
    result_message = db_utils.delete_course(group_id)
    await message.answer(text=result_message)


@router.message(Command("del_course"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")



@router.message(Command("raise"), Mode.admin_chosen)
async def add_client(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: после /raise нужно передать данные преподавателя")
        return
    try:
        teacher_id, raise_amount = command.args.split(', ')
    except ValueError:
        await message.answer(text="Ошибка: данные вводятся в формате <НомерПреподавателя>, <РазмерПрибавки>")
    
    result_message = db_utils.give_raise(teacher_id, raise_amount)
    await message.answer(text=result_message)


@router.message(Command("raise"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")


@router.message(Command("income"), Mode.admin_chosen)
async def add_client(message: Message):
    result_message = "Ожидаемая прибыль за неделю составляет "
    result_message += str(db_utils.get_weekly_income()) + " руб."
    await message.answer(text=result_message)


@router.message(Command("income"))
async def cant_show_clients(message: Message):
    await message.answer("К сожалению у Вас недостаточно прав для этой команды")
