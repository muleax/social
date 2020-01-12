import asyncio
import pymysql
import logging
from db_schema import *


async def open_connection(host, port, user, password):
    connection = None
    for i in range(10):
        await asyncio.sleep(5)
        try:
            # TODO: some clever auth
            connection = pymysql.connect(host=host, port=port, user=user, password=password,
                                         charset=CHARSET, cursorclass=pymysql.cursors.DictCursor)
        except:
            logging.info(f"Couldn't connect to db on {i + 1} attempt")
        else:
            break

    if connection.open:
        logging.info(f"Connected to db at {host}:{port}")
        return connection
    else:
        logging.error("Couldn't connect to db")
        return None
