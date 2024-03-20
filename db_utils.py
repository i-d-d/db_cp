import psycopg2
import db
from datetime import datetime


def client_exists(client_id):
    cursor = db.connection.cursor()
    cursor.execute("""SELECT COUNT(*) FROM clients WHERE card_id = {};""".format(client_id))
    return cursor.fetchone()[0] > 0


def get_client(client_id):
    cursor = db.connection.cursor()
    cursor.execute("""SELECT * FROM clients WHERE card_id = {};""".format(client_id))
    return cursor.fetchone()


def get_chosen_courses(client_id):
    cursor = db.connection.cursor()
    cursor.execute("""SELECT course_name, apply_discount({0}, cost) AS cost_discounted, week_day, start_time FROM 
                   clients_courses JOIN courses ON clients_courses.group_id = courses.group_id
                   WHERE card_id = {0};""".format(client_id))
    return cursor.fetchall()


def get_all_selected_teachers(client_id):
    cursor = db.connection.cursor()
    cursor.execute("""SELECT course_name, teacher_name, phone_number, email, experience FROM clients_courses 
                      JOIN courses ON clients_courses.group_id = courses.group_id
                      JOIN courses_teachers ON courses.group_id = courses_teachers.group_id
                      JOIN teachers ON courses_teachers.teacher_id = teachers.teacher_id
                      WHERE card_id = {};""".format(client_id))
    return cursor.fetchall()


def get_closest_course(client_id):
    cursor = db.connection.cursor()
    cursor.execute("""SELECT course_name, apply_discount({0}, cost) AS cost_discounted, week_day, start_time FROM 
                   clients_courses JOIN courses ON clients_courses.group_id = courses.group_id
                   WHERE card_id = {0};""".format(client_id))
    courses = cursor.fetchall()
    min = 7 * 24 * 60
    now = datetime.time(datetime.now())
    week_day = datetime.now().weekday()
    days = {'ПН': 0, 'ВТ': 1, 'СР': 2, 'ЧТ': 3, 'ПТ': 4, 'СБ': 5, 'ВС': 6}
    result = courses[0]
    for course in courses:
        dist = (days[course[2]] - week_day) * 24 * 60
        dist += (course[3].hour - now.hour) * 60 + (course[3].minute - now.minute)
        if dist < 0:
            dist += 7 * 24 * 60
        if dist < min:
            min = dist
            result = course
    return result


def list_all_courses():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM courses")
    return cursor.fetchall()


def signup_for_new_course(client_id, course_name):
    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL sign_up({0}, '{1}')".format(client_id, course_name))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Поздравляем! Вы успешно записались на курс"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]


def quit_course(client_id, course_name):
    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL quit_course({0}, '{1}')".format(client_id, course_name))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Вы успешно покинули курс"
        
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]


def create_client(client_id, client_name, client_phone_number):
    cursor = db.connection.cursor()
    try:
        cursor.execute("INSERT INTO clients VALUES ({0}, '{1}', '{2}');".format(client_id, client_name, client_phone_number))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Пользователь успешно добавлен"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]
    

def delete_client(client_id):
    cursor = db.connection.cursor()
    try:
        cursor.execute("DELETE FROM clients WHERE card_id = {0};".format(client_id))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Пользователь успешно удалён"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]


def list_all_clients():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM clients")
    return cursor.fetchall()


def list_all_teachers():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM teachers")
    return cursor.fetchall()


def add_course(course_id, course_name, cost, week_day, start_time):
    cursor = db.connection.cursor()
    try:
        cursor.execute("INSERT INTO courses VALUES ({0}, '{1}', {2}, '{3}', '{4}');".format(course_id, course_name, cost, week_day, start_time))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Новый курс успешно добавлен"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]
    

def add_teacher(teacher_id, teacher_name, phone_number, email, experience, salary):
    cursor = db.connection.cursor()
    try:
        cursor.execute("INSERT INTO teachers VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5});".format(teacher_id, teacher_name, phone_number, email, experience, salary))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Преподаватель успешно добавлен"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]
    

def get_weekly_income():
    cursor = db.connection.cursor()
    cursor.execute('SELECT calc_income()')
    return cursor.fetchone()[0]


def fire_teacher(teacher_id):
    cursor = db.connection.cursor()
    try:
        cursor.execute("DELETE FROM teachers WHERE teacher_id = {0};".format(teacher_id))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Пользователь успешно удалён"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]
    

def delete_course(course_id):
    cursor = db.connection.cursor()
    try:
        cursor.execute("DELETE FROM courses WHERE course_id = {0};".format(course_id))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Мастер-класс успешно удалён"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]


def give_raise(teacher_id, raise_amount):
    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL give_raise({0}, {1});".format(teacher_id, raise_amount))
        db.connection.commit()
        db.connection.close()
        db.connection = db.connect()
        return "Зарплата преподавателя повышена!"
    except Exception as e:
        db.connection.close()
        db.connection = db.connect()
        return str(e).split('\n')[0]