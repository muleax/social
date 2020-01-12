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
        cursor.execute(f'CREATE TABLE {table_name}({table_def});')

    connection.commit()


# noinspection SqlNoDataSourceInspection
def add_test_users(connection):
    logging.info("Creating test users...")

    connection.begin()
    connection.select_db(DATABASE)

    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {USERS_TABLE} VALUES ('Sanya', 'Ivanov', 'Minsk', '{{}}');")
    cursor.execute(f"INSERT INTO {USERS_TABLE} VALUES ('Kolya', 'Dvoechka', 'Moscow', '{{}}');")
    cursor.execute(f"INSERT INTO {USERS_TABLE} VALUES ('Nastik', 'Kotik', 'Lipetsk', '{{}}');")

    connection.commit()
