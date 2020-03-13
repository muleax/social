import logging
from db_schema import *


def is_fresh_db(connection, schema):
    cursor = connection.cursor()
    res = cursor.execute(f"SHOW DATABASES LIKE '{schema['name']}';")
    return not res


# noinspection SqlNoDataSourceInspection
def create_tables(connection, schema):
    db_name = schema['name']
    logging.info(f"Creating tables for {db_name}...")

    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.execute(f"USE {db_name};")

    for table_name, table_desc in schema['tables'].items():
        fields = ', '.join(f'{field_name} {field_type}' for field_name, field_type in table_desc['schema'].items())
        primary_key = f"PRIMARY KEY ({', '.join(table_desc['primary_key'])})"
        query = f"CREATE TABLE {table_name}({fields}, {primary_key})"
        logging.info(query)
        cursor.execute(query)


def create_indexes(connection, schema):
    db_name = schema['name']
    logging.info(f"Creating indexes for {db_name}...")

    cursor = connection.cursor()

    cursor.execute(f"USE {db_name};")

    for table_name, table_desc in schema['tables'].items():
        for index_name, index_order in table_desc['indexes'].items():
            index_def = ', '.join(index_order)
            cursor.execute(f'CREATE INDEX {index_name} ON {table_name} ({index_def})')
