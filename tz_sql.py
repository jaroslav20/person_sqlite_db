import random
import time
from datetime import datetime as dt
from datetime import timedelta
import os
import sqlite3 as sq


def read_name_random_date(file):
    start = dt.strptime('01.01.1930', '%d.%m.%Y')
    end = dt.strptime('01.01.2022', '%d.%m.%Y')
    sex = ''
    if file == "name_w.txt":
        sex = 'woman'
    elif file == 'name_m.text':
        sex = 'man'

        with open(file, "r") as file:
            delta = end - start
            while True:
                line = file.readline()
                if not line:
                    break
                name = line.strip()
                random_date = start + timedelta(random.randint(0, delta.days))
                print(f"{name}   {random_date} {sex} ")
                insert_varible_into_table(name, random_date, sex)

    print("Добавленно 5000 записей")


def insert_varible_into_table(name, birthday, sex):

    try:
        sqlite_connection = sq.connect('myApp.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT INTO myApp
                              (name, birthday, sex)
                              VALUES (?, ?, ?);"""

        data_tuple = (name, birthday, sex)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Данные успешно вставлены в таблицу myApp")

        cursor.close()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def read_sqlite_table():
    try:
        sqlite_connection = sq.connect('myApp.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT name, birthday, sex
         FROM myApp;"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Всего записей:  ", len(records))
        print("Вывод каждой записи")
        for row in records:
            print(f"ФИО: {row[0]}, Дата рождения: {row[1]}, пол: {row[2]}", end="\n\n")

        cursor.close()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def help():
    print('Для первого запуска используйте комманду myApp 1.'
          'Для ручного добавления записи используйте команду myApp 2')
    print('Команда myApp 3 выведет список записей в консоль')
    print('Команда myApp 4 сгенерирует 5000 мужчин или женщин')


def main():
    com = input()

    if com == "myApp 1":

        if os.path.exists("myApp.db"):
            print("Такая база данных уже существует")
        else:
            with sq.connect('myApp.db') as con:
                cur = con.cursor()

                cur.execute(
                    """CREATE TABLE IF NOT EXISTS myApp (
                    name TEXT NOT NULL,
                    birthday TEXT NOT NULL,
                    sex INTEGER NOT NULL DEFAULT 1
                    )""")
            print('Новая база данных "myApp.db" успешно созданна.')


    elif com == "myApp 2":

        while com != "finish":
            name = input('Введите ФИО: ')
            birthday = input('Ведите дату рождения в формате 2020-01-12: ')
            sex = input('Введите пол мужской man или woman: ')

            insert_varible_into_table(name, birthday, sex)

            v = input('Добавить ещё запись? y/n ')
            if v == 'n':
                break



    elif com == "myApp 3":
        start = time.time()
        read_sqlite_table()
        end = time.time() - start
        print(f"Время выполнения: {end}")


    elif com == "myApp 4":
        print("Генерация случайных ФИО и даты рождения")
        sex = input('Укажите пол для генерации man/woman')
        if sex == 'man':
            read_name_random_date('name_m.txt')
        elif sex == 'woman':
            read_name_random_date('name_w.txt')

    else:
        help()


if __name__ == "__main__":
    print("""Здравствуйте я скрипт на языке Python
Для ознакомления с доступными командами ввведите help или или введите команду """)
    com = ''
    if com == 'help':
        help()
    else:
        main()
    print("конец программы")