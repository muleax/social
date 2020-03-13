import logging
import asyncio
import db_connection
import random
import datetime
from db_schema import *
from dev_utils import *


# noinspection SqlNoDataSourceInspection
def create_test_users(connection, count):
    logging.info("Creating test users...")

    city_sample_space = get_city_sample_space()
    logging.info(f"Cities sampled")
    names_sample_space = get_names_sample_space(size=min(100000, count * 2))
    logging.info(f"Names sampled")
    age_sample_space = get_age_sample_space()
    today_date = datetime.date.today()

    connection.select_db(SOCIAL_DATABASE)
    cursor = connection.cursor()

    sql_batch_size = 20000
    for i in range(0, max(1, count // sql_batch_size)):
        values_auth = []
        values_users = []
        for j in range(1, sql_batch_size + 1):
            user_id = i * sql_batch_size + j
            login = f"login{user_id}"
            password = f"password{user_id}"
            city = random.choice(city_sample_space)
            first_name, last_name = random.choice(names_sample_space)
            birth_date = sample_birth_date(age_sample_space, today_date=today_date).isoformat()
            udata = '{}'

            values_auth.append(f"('{login}', '{password}', {user_id})")
            values_users.append(f"({user_id}, '{first_name}', '{last_name}', '{city}', '{birth_date}', '{udata}')")

        auth_sql = f"INSERT INTO {AUTH_TABLE} (login, password, user_id) VALUES {', '.join(values_auth)}"
        cursor.execute(auth_sql)

        users_sql = f"INSERT INTO {USERS_TABLE} (user_id, first_name, last_name, city, birth_date, udata)\
                      VALUES {', '.join(values_users)}"
        cursor.execute(users_sql)

        logging.info(f"Inserted {sql_batch_size * (i + 1)}")

    logging.info("Creation finished")


def open_connection_sync(host='localhost', port=3307, user='root', password=''):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(db_connection.open_connection(host, port, user, password))
