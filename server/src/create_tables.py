import logging
from db_schema import *


def is_fresh_db(connection):
    cursor = connection.cursor()
    res = cursor.execute(f"SHOW DATABASES LIKE '{DATABASE}';")
    return not res


# noinspection SqlNoDataSourceInspection
def create_tables(connection):
    logging.info("Creating tables...")

    connection.begin()
    cursor = connection.cursor()

    cursor.execute(f'CREATE DATABASE {DATABASE};')

    cursor.execute(f'USE {DATABASE};')
    for table_name, table_schema in TABLES.items():
        table_def = ', '.join(f'{field_name} {field_type}' for field_name, field_type in table_schema.items())
        query = f'CREATE TABLE {table_name}({table_def});'
        logging.info(query)
        cursor.execute(query)

    connection.commit()


# noinspection SqlNoDataSourceInspection
def add_test_users(connection):
    logging.info("Creating test users...")

    connection.begin()
    connection.select_db(DATABASE)

    cursor = connection.cursor()

    test_users = (('Sanya', 'Ivanov', 'Minsk', {}),
                  ('Kolya', 'Dvoechka', 'Moscow', {}),
                  ('Nastik', 'Kotik', 'Lipetsk', {}))

    for fn, ln, city, udata in test_users:
        cursor.execute(f"INSERT INTO {USERS_TABLE} (first_name, last_name, city, udata)\
                         VALUES ('{fn}', '{ln}', '{city}', '{udata}');")

    connection.commit()
