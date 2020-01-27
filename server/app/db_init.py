import logging
from db_schema import *


def is_fresh_db(connection):
    cursor = connection.cursor()
    res = cursor.execute(f"SHOW DATABASES LIKE '{DATABASE}';")
    return not res


# noinspection SqlNoDataSourceInspection
def create_tables(connection):
    logging.info("Creating tables...")

    cursor = connection.cursor()

    cursor.execute(f'CREATE DATABASE {DATABASE}')
    cursor.execute(f'USE {DATABASE};')
    for table_name, table_schema in TABLES.items():
        table_def = ', '.join(f'{field_name} {field_type}' for field_name, field_type in table_schema.items())
        query = f'CREATE TABLE {table_name}({table_def})'
        logging.info(query)
        cursor.execute(query)


def create_indexes(connection):
    logging.info("Creating indexes...")

    cursor = connection.cursor()

    for table_name, index_defs in INDEXES.items():
        for index_name, index_def in index_defs.items():
            fields = ', '.join(index_def)
            cursor.execute(f'CREATE INDEX {index_name} ON {table_name} ({fields})')
