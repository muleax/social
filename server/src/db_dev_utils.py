import logging
import asyncio
import db_connection
from db_schema import *


# noinspection SqlNoDataSourceInspection
def create_test_users(connection, count):
    logging.info("Creating test users...")

    connection.select_db(DATABASE)
    cursor = connection.cursor()

    test_users = (('Sanya', 'Ivanov', 'Minsk', '1998-01-01', {}, 'sanya1998', 'pass'),
                  ('Kolya', 'Dvoechka', 'Moscow', '2005-04-27',  {}, 'nagibator2005', 'qwerty'),
                  ('Nastik', 'Kotik', 'Moscow', '1997-10-10', {}, 'kotik_kotik', 'kotik'))

    BATCH_SIZE = 20000
    for i in range(0, max(1, count // BATCH_SIZE)):
        values_auth = []
        values_users = []
        for j in range(1, BATCH_SIZE + 1):
            user_id = i * BATCH_SIZE + j
            first_name, last_name, city, birth_date, udata, login, password = test_users[0]
            values_auth.append(f"('{login}-{user_id}', '{password}', {user_id})")
            values_users.append(f"({user_id}, '{first_name}-{user_id}', '{last_name}-{user_id}', '{city}', '{birth_date}', '{udata}')")

        cursor.execute(f"INSERT INTO {AUTH_TABLE} (login, password, user_id) VALUES {', '.join(values_auth)}")

        cursor.execute(f"INSERT INTO {USERS_TABLE} (user_id, first_name, last_name, city, birth_date, udata)\
                         VALUES {', '.join(values_users)}")

        logging.info(f"Created {BATCH_SIZE * (i + 1)}")

    logging.info("Creation finished")


def open_connection_sync(host='localhost', port=3307, user='root', password=''):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(db_connection.open_connection(host, port, user, password))

