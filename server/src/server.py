import logging
import db_connection
from db_schema import *
from aiohttp import web
from constants import *
import json


async def create_user(request):
    user_data = await request.json()
    logging.info(f'Create user {user_data}')

    # TODO: db abstraction model
    cursor = request.app.db.cursor()
    cursor.execute(f"INSERT INTO {USERS_TABLE} (first_name, last_name, city, udata)\
                     VALUES ('{user_data['firstName']}', '{user_data['lastName']}', '{user_data['city']}', '{{}}');")

    # request.app.db.commit()
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
    app.router.add_get('/user', user)
    app.router.add_get('/user_list', user_list)
    app.router.add_post('/create_user', create_user)


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
            logging.info('Worker failed to connect to db')
            # TODO

    app.on_startup.append(on_startup)
    return app


logging.basicConfig(level=logging.DEBUG)
