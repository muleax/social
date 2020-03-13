import logging
from constants import *
from utils import *
from db_schema import *


async def create_account(request):
    payload = await request.json()
    logging.info(f'Create account {payload}')

    try:
        login = payload['login']
        password = payload['password']
    except KeyError:
        return build_response(STATUS.BAD_REQUEST)

    # TODO: async db abstraction model
    conn = request.app.master_db_connection
    try:
        conn.begin()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {AUTH_TABLE} (login, password) VALUES ('{login}', '{password}')")

        # cursor.execute("SELECT LAST_INSERT_ID()")
        # user_id = cursor.fetchone()['LAST_INSERT_ID()']

        cursor.execute(f"SELECT user_id FROM {AUTH_TABLE} WHERE login = '{login}'")
        user_id = cursor.fetchone()['user_id']

        cursor.execute(f"INSERT INTO {USERS_TABLE} (user_id, udata) VALUES ('{user_id}', '{{}}')")

        conn.commit()
        return build_response(STATUS.SUCCESS)

    except Exception as err:
        logging.exception(err)
        conn.rollback()
        return build_response(STATUS.SERVER_ERROR)


async def auth(request):
    params = request.rel_url.query
    logging.info(f'Auth {params}')

    try:
        login = params['login']
        password = params['password']
    except KeyError:
        return build_response(STATUS.BAD_REQUEST)

    try:
        cursor = request.app.master_db_connection.cursor()
        cursor.execute(f"SELECT user_id, password FROM {AUTH_TABLE} WHERE login='{login}'")

        fetched = cursor.fetchone()
        if fetched['password'] != password:
            return build_response(STATUS.BAD_REQUEST)

        data = {
            'user_id': fetched['user_id'],
            'auth_token': get_auth_token(fetched['user_id'])
        }
        return build_response(STATUS.SUCCESS, data)

    except Exception as err:
        logging.exception(err)
        return build_response(STATUS.SERVER_ERROR)
