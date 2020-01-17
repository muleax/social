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
    return user_id and token and (token == get_auth_token(user_id))


def format_user_data(user_data):
    # TODO: reconsider
    if 'birth_date' in user_data:
        user_data['birth_date'] = user_data['birth_date'].isoformat()
    return user_data


def build_response(status, data=None):
    return web.Response(text=f"{json.dumps(data)}\n", status=status)


async def create_account(request):
    credentials = await request.json()
    logging.info(f'Create account {credentials}')

    login = credentials.get('login')
    password = credentials.get('password')
    if not login or not password:
        return build_response(STATUS.BAD_REQUEST)

    # TODO: async db abstraction model
    conn = request.app.db
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


async def update_user(request):
    payload = await request.json()
    logging.info(f'Update user {payload}')

    user_id = payload.get('user_id')
    if not check_auth_token(user_id, payload.get('auth_token')):
        return build_response(STATUS.BAD_REQUEST)

    user_data = payload['data']

    params = ', '.join(f"{fn} = '{user_data[fn]}'" for fn in EDITABLE_USER_FIELDS if fn in user_data)
    if not params:
        return build_response(STATUS.BAD_REQUEST)

    try:
        cursor = request.app.db.cursor()
        q = f"UPDATE {USERS_TABLE} SET {params} WHERE user_id = {user_id}"
        cursor.execute(q)
        # enrich updated data with return updated data
        return build_response(STATUS.SUCCESS)

    except Exception as err:
        logging.exception(err)
        return build_response(STATUS.SERVER_ERROR)


async def auth(request):
    credentials = request.rel_url.query
    logging.info(f'Auth {credentials}')

    login = credentials.get('login')
    password = credentials.get('password')
    if not login or not password:
        return build_response(STATUS.BAD_REQUEST)

    try:
        cursor = request.app.db.cursor()
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


async def find_users(request):
    data = request.rel_url.query
    logging.info(f'Find users {data}')


async def user_list(request):
    data = request.rel_url.query
    logging.info(f'Get user list {data}')

    offset = data.get('offset')
    limit = data.get('limit')
    if offset is None or limit is None:
        return build_response(STATUS.BAD_REQUEST)

    public_fields = ', '.join(PUBLIC_USER_FIELDS)

    try:
        cursor = request.app.db.cursor()
        cursor.execute(f"SELECT {public_fields} FROM {USERS_TABLE} LIMIT {limit} OFFSET {offset}")

        records = list(map(format_user_data, cursor.fetchall()))
        return build_response(STATUS.SUCCESS, records)

    except Exception as err:
        logging.exception(err)
        return build_response(STATUS.SERVER_ERROR)


async def user(request):
    data = request.rel_url.query
    logging.info(f'Get user by Id {data}')

    user_id = data.get('user_id')
    if user_id is None:
        return build_response(STATUS.BAD_REQUEST)

    public_fields = ', '.join(PUBLIC_USER_FIELDS)

    cursor = request.app.db.cursor()
    cursor.execute(f"SELECT {public_fields} FROM {USERS_TABLE} WHERE user_id={user_id}")
    record = cursor.fetchone()
    if record:
        record = format_user_data(record)

    return build_response(STATUS.SUCCESS, record)


def create_routes(app):
    app.router.add_post('/create_account', create_account)
    app.router.add_post('/update_user', update_user)
    app.router.add_get('/auth', auth)
    app.router.add_get('/find_users', find_users)
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
