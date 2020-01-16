import logging
import db_connection
from db_schema import *
from aiohttp import web
from constants import *
import json
import jwt


def get_auth_token(user_id):
    return jwt.encode({user_id: AUTH.JWT_SALT}, AUTH.JWT_SECRET, algorithm='HS256').decode('utf-8')


def check_auth_token(user_id, token):
    return token == get_auth_token(user_id)


def build_response(status, data=None):
    return web.Response(text=f"{json.dumps(data)}\n", status=status)


async def create_account(request):
    credentials = await request.json()
    logging.info(f'Create account {credentials}')

    # TODO: async db abstraction model
    conn = request.app.db
    try:
        conn.begin()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {AUTH_TABLE} (login, password)\
                         VALUES ('{credentials['login']}', '{credentials['password']}')")

        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()['LAST_INSERT_ID()']

        cursor.execute(f"INSERT INTO {USERS_TABLE} (user_id, first_name, last_name, city, udata)\
                         VALUES ('{user_id}', '', '', '', '{{}}')")

    except Exception as err:
        logging.exception(err)
        conn.rollback()
        return build_response(STATUS.SERVER_ERROR)

    else:
        conn.commit()
        return build_response(STATUS.SUCCESS)


async def update_user(request):
    payload = await request.json()
    logging.info(f'Update user {payload}')

    user_id = payload['user_id']
    if not check_auth_token(user_id, payload['auth_token']):
        return build_response(STATUS.BAD_REQUEST)

    user_data = payload['data']

    try:
        cursor = request.app.db.cursor()
        cursor.execute(f"UPDATE {USERS_TABLE}\
                         SET\
                            first_name = '{user_data['first_name']}',\
                            last_name = '{user_data['last_name']}',\
                            city = '{user_data['city']}',\
                            udata = '{user_data['udata']}'\
                         WHERE\
                            user_id = {user_id}")

    except Exception as err:
        logging.exception(err)
        return build_response(STATUS.SERVER_ERROR)

    else:
        return build_response(STATUS.SUCCESS, user_data)


async def auth(request):
    credentials = request.rel_url.query
    logging.info(f'Auth {credentials}')
    login = credentials.get('login')
    password = credentials.get('password')

    if login and password:
        try:
            cursor = request.app.db.cursor()
            cursor.execute(f"SELECT user_id, password FROM {AUTH_TABLE} WHERE login='{login}'")

            fetched = cursor.fetchone()
            if fetched['password'] == password:
                data = {
                    'user_id': fetched['user_id'],
                    'auth_token': get_auth_token(fetched['user_id'])
                }
                return build_response(STATUS.SUCCESS, data)

        except Exception as err:
            logging.exception(err)
            return build_response(STATUS.SERVER_ERROR)

    return build_response(STATUS.BAD_REQUEST)


async def user_list(request):
    data = request.rel_url.query
    offset = int(data.get('offset', 0))
    limit = min(GET_USERS_LIMIT, int(data.get('limit', GET_USERS_LIMIT)))

    cursor = request.app.db.cursor()
    cursor.execute(f'SELECT * FROM {USERS_TABLE} LIMIT {limit} OFFSET {offset}')
    records = cursor.fetchall()

    return build_response(STATUS.SUCCESS, records)


async def user(request):
    data = request.rel_url.query
    user_id = int(data.get('user_id', 0))

    cursor = request.app.db.cursor()
    cursor.execute(f'SELECT first_name, last_name, city, udata FROM {USERS_TABLE} WHERE user_id={user_id}')
    record = cursor.fetchone()

    return build_response(STATUS.SUCCESS, record)


def create_routes(app):
    app.router.add_post('/create_account', create_account)
    app.router.add_post('/update_user', update_user)
    app.router.add_get('/auth', auth)
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
