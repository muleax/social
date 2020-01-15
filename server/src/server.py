import logging
import db_connection
from db_schema import *
from aiohttp import web
from constants import *
import json


async def create_account(request):
    auth = await request.json()
    logging.info(f'Create account {auth}')

    # TODO: async db abstraction model
    conn = request.app.db
    try:
        conn.autocommit(False)

        conn.begin()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {AUTH_TABLE} (login, password)\
                         VALUES ('{auth['login']}', '{auth['password']}')")

        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()['LAST_INSERT_ID()']

        cursor.execute(f"INSERT INTO {USERS_TABLE} (id, first_name, last_name, city, udata)\
                         VALUES ('{user_id}', '', '', '', '{{}}')")

    except Exception as err:
        logging.exception(err)
        conn.rollback()
        return web.Response(text=f"{STATUS.FAIL}\n")

    else:
        conn.commit()
        return web.Response(text=f"{STATUS.OK}\n")

    finally:
        # TODO: reconsider
        conn.autocommit(True)


async def update_user(request):
    user_data = await request.json()
    logging.info(f'Update user {user_data}')

    try:
        cursor = request.app.db.cursor()
        cursor.execute(f"UPDATE {USERS_TABLE}\
                         SET\
                            first_name = '{user_data['firstName']}',\
                            last_name = '{user_data['lastName']}',\
                            city = '{user_data['city']}',\
                            udata = '{user_data['udata']}'\
                         WHERE\
                            id = {user_data['id']}")

    except Exception as err:
        logging.exception(err)
        return web.Response(text=f"{STATUS.FAIL}\n")

    else:
        return web.Response(text=f"{STATUS.OK}\n")


async def user_list(request):
    data = request.rel_url.query
    offset = int(data.get('offset', 0))
    limit = min(GET_USERS_LIMIT, int(data.get('limit', GET_USERS_LIMIT)))

    cursor = request.app.db.cursor()
    cursor.execute(f'SELECT * FROM {USERS_TABLE} LIMIT {limit} OFFSET {offset}')
    records = cursor.fetchall()

    return web.Response(text=f"{json.dumps(records)}\n")


async def user(request):
    data = request.rel_url.query
    user_id = int(data.get('id', 0))

    cursor = request.app.db.cursor()
    cursor.execute(f'SELECT * FROM {USERS_TABLE} WHERE id={user_id}')
    record = cursor.fetchone()

    return web.Response(text=f"{json.dumps(record)}\n")


def create_routes(app):
    app.router.add_post('/create_account', create_account)
    app.router.add_post('/update_user', update_user)
    app.router.add_get('/user', user)
    app.router.add_get('/user_list', user_list)


def app_factory(db_host, db_port, db_user, db_password):
    app = web.Application()

    async def on_startup(app):
        app.db = await db_connection.open_connection(db_host, db_port, db_user, db_password)

        if app.db:
            app.db.autocommit(True)
            app.db.cursor().execute(f'USE {DATABASE}')
            logging.info('Worker connected to db')
            create_routes(app)
        else:
            logging.info('Worker failed to connect to db!')
            # TODO

    app.on_startup.append(on_startup)
    return app


logging.basicConfig(level=logging.DEBUG)
