import logging
import asyncio
import db_connection
from db_schema import *


# noinspection SqlNoDataSourceInspection
def create_test_users(connection):
    logging.info("Creating test users...")

    connection.select_db(DATABASE)
    cursor = connection.cursor()

    test_users = (('Sanya', 'Ivanov', 'Minsk', {}, '1998-01-01', 'sanya1998', 'pass'),
                  ('Kolya', 'Dvoechka', 'Moscow', {}, '2005-04-27', 'nagibator2005', 'qwerty'),
                  ('Nastik', 'Kotik', 'Moscow', {}, '1997-10-10', 'kotik_kotik', 'kotik'))

    for first_name, last_name, city, udata, birth_date, login, password in test_users:
        cursor.execute(f"INSERT INTO {AUTH_TABLE} (login, password) VALUES ('{login}', '{password}')")

        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()['LAST_INSERT_ID()']

        cursor.execute(f"INSERT INTO {USERS_TABLE} (user_id, first_name, last_name, city, birth_date, udata)\
                         VALUES ({user_id}, '{first_name}', '{last_name}', '{city}', '{birth_date}', '{udata}');")


def open_connection_sync(host='localhost', port=3307, user='root', password=''):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(db_connection.open_connection(host, port, user, password))

