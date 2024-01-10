# использовать словарь, содержащий следующие ключи: фамилия, имя; знак Зодиака; дата рождения (список из трёх чисел).
# Написать программу, выполняющую следующие действия:
# ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть упорядочены по датам рождения; вывод на экран информацию о людях, родившихся под знаком, название которого введено с клавиатуры;
# если таких нет, выдать на дисплей соответствующее сообщение.
# Оформив каждую команду в виде отдельной функции.
# Дополнительно реализовать сохранение и чтение данных из файла формата JSON.
# Дополнительно реализовать интерфейс командной строки (CLI).
# Необходимо реализовать хранение данных в базе данных SQLite3. Информация в базе данных должна храниться не менее чем в двух таблицах.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3

# Функция для ввода данных с клавиатуры
def input_data():
    last_name = input("Введите фамилию: ")
    first_name = input("Введите имя: ")
    zodiac_sign = input("Введите знак Зодиака: ")
    day = int(input("Введите день рождения: "))
    month = int(input("Введите месяц рождения: "))
    year = int(input("Введите год рождения: "))
    return {
        'фамилия': last_name,
        'имя': first_name,
        'знак Зодиака': zodiac_sign,
        'дата рождения': [day, month, year]
    }

# Функция для сортировки списка по датам рождения
def sort_by_birthday(people):
    return sorted(people, key=lambda x: x['дата рождения'])

# Функция для вывода информации о людях с заданным знаком Зодиака
def print_people_by_zodiac(people, zodiac):
    found = False
    for person in people:
        if person['знак Зодиака'] == zodiac:
            print(person)
            found = True
    if not found:
        print("Нет людей с таким знаком Зодиака")

# Функция для сохранения данных в файл формата JSON
def save_to_json(people, file_name):
    with open(file_name, 'w') as file:
        json.dump(people, file)

# Функция для чтения данных из файла формата JSON
def load_from_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

# Функция для создания таблиц в базе данных SQLite3
def create_tables(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS People
                (last_name text, first_name text, zodiac_sign text, day integer, month integer, year integer)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Zodiacs
                (zodiac_sign text)''')

# Функция для сохранения данных в базу данных SQLite3
def save_to_database(people, conn):
    c = conn.cursor()
    c.execute('DELETE FROM People')
    c.execute('DELETE FROM Zodiacs')
    for person in people:
        c.execute('INSERT INTO People VALUES (?,?,?,?,?,?)', (
            person['фамилия'], person['имя'], person['знак Зодиака'],
            person['дата рождения'][0], person['дата рождения'][1], person['дата рождения'][2]))
        c.execute('INSERT OR IGNORE INTO Zodiacs VALUES (?)', (person['знак Зодиака'],))
    conn.commit()

# Функция для чтения данных из базы данных SQLite3
def load_from_database(conn):
    c = conn.cursor()
    people = []
    for row in c.execute('SELECT * FROM People'):
        person = {
            'фамилия': row[0],
            'имя': row[1],
            'знак Зодиака': row[2],
            'дата рождения': [row[3], row[4], row[5]]
        }
        people.append(person)
    return people

# Функция для работы с интерфейсом командной строки
def cli():
    conn = sqlite3.connect('database.db')
    create_tables(conn)

    while True:
        print("1. Ввести данные в список")
        print("2. Сохранить данные в файл JSON")
        print("3. Загрузить данные из файла JSON")
        print("4. Вывести людей с заданным знаком Зодиака")
        print("5. Вывести сохраненные людей с заданным знаком Зодиака из базы данных")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            people = []
            count = int(input("Введите количество людей: "))
            for _ in range(count):
                people.append(input_data())
            people = sort_by_birthday(people)
            save_to_database(people, conn)
        elif choice == '2':
            file_name = input("Введите имя файла: ")
            people = load_from_database(conn)
            save_to_json
if __name__ == "__main__":
    main()
