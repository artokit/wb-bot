import sqlite3
from datetime import datetime

connection = sqlite3.connect('wb.db')
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS clients '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone_number TEXT, reg_date DATETIME);')


def check_user(user_phone_number):
    connect = sqlite3.connect('wb.db')
    cursor = connect.cursor()

    checker = cursor.execute('SELECT user_phone_number FROM clients WHERE user_phone_number=?',
                          (user_phone_number,)).fetchone()

    if checker:
        return True

    else:
        return False


def register_user(user_id, user_phone_number):
    connection = sqlite3.connect('wb.db')
    sql = connection.cursor()
    try:
        sql.execute(
            'INSERT INTO clients (id, user_phone_number, reg_date) VALUES (?, ?, ?);',
            (user_id, user_phone_number, datetime.now())
        )

        connection.commit()
    except sqlite3.IntegrityError:
        return


def get_users_id():
    connect = sqlite3.connect('wb.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT ID FROM CLIENTS').fetchall()
