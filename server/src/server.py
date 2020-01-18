import logging
import db_connection
import json
import jwt
import datetime
from aiohttp import web
from db_schema import *
from constants import *
from itertools import *


def get_auth_token(user_id):
    return jwt.encode({user_id: AUTH.JWT_SALT}, AUTH.JWT_SECRET, algorithm='HS256').decode('utf-8')


def check_auth_token(user_id, token):
    return token == get_auth_token(user_id)


def format_user_data(user_data):
    # TODO: reconsider
    if 'birth_date' in user_data:
        user_data['birth_date'] = user_data['birth_date'].isoformat()
    return user_data


def build_response(status, data=None):
    return web.Response(text=f"{json.dumps(data)}\n", status=status)


def calculate_birth_date(age, today_date):
    try:
        return today_date.replace(year=(today_date.year - age))
    except ValueError:
        return today_date.replace(year=(today_date.year - age), month=3, day=1)


async def create_account(request):
    payload = await request.json()
    logging.info(f'Create account {payload}')

    try:
        login = payload['login']
        password = payload['password']
    except KeyError:
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

    try:
        user_id = payload['user_id']
        if not check_auth_token(user_id, payload['auth_token']):
            return build_response(STATUS.BAD_REQUEST)
    except KeyError:
        return build_response(STATUS.BAD_REQUEST)

    assignments = (f"{fn} = '{payload[fn]}'" for fn in EDITABLE_USER_FIELDS if fn in payload)
    set_statement = ', '.join(assignments)
    if not set_statement:
        return build_response(STATUS.BAD_REQUEST)

    try:
        cursor = request.app.db.cursor()
        sql = f"UPDATE {USERS_TABLE} SET {set_statement} WHERE user_id = {user_id}"
        cursor.execute(sql)
        # enrich updated data with return updated data
        return build_response(STATUS.SUCCESS)

    except Exception as err:
        logging.exception(err)
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
    params = request.rel_url.query
    logging.info(f'Find users {params}')

    try:
        user_id = params['user_id']
        if not check_auth_token(user_id, params['auth_token']):
            return build_response(STATUS.BAD_REQUEST)

        limit = min(FIND_USERS_LIMIT, int(params['limit']))
        offset = int(params['offset'])

        eq_search_order = ('first_name', 'last_name', 'city')
        constraints_sql = [f"{fn}='{params[fn]}'" for fn in eq_search_order if fn in params]

        today_date = datetime.date.today()
        age_from = params.get('age_from')
        if age_from:
            upper_bound = calculate_birth_date(int(age_from), today_date).isoformat()
            constraints_sql.append(f"birth_date <= '{upper_bound}'")
        age_to = params.get('age_to')
        if age_to:
            lower_bound = calculate_birth_date(int(age_to) + 1, today_date).isoformat()
            constraints_sql.append(f"birth_date > '{lower_bound}'")

    except (ValueError, KeyError) as err:
        logging.debug(f"Find users bad request: {err}")
        return build_response(STATUS.BAD_REQUEST)

    if not constraints_sql:
        return build_response(STATUS.BAD_REQUEST)

    constraints_sql.append(f"user_id != {user_id}")
    search_condition = ' AND '.join(constraints_sql)

    try:
        cursor = request.app.db.cursor()
        preview_fields = ', '.join(PREVIEW_USER_FIELDS)
        sql = f"SELECT {preview_fields} FROM {USERS_TABLE} WHERE {search_condition} LIMIT {limit} OFFSET {offset}"
        logging.debug(f"Find users sql: {sql}")
        cursor.execute(sql)

        records = list(map(format_user_data, cursor.fetchall()))
        return build_response(STATUS.SUCCESS, records)

    except Exception as err:
        logging.exception(err)
        return build_response(STATUS.SERVER_ERROR)


async def user_list(request):
    params = request.rel_url.query
    logging.info(f'Get user list {params}')

    try:
        offset = min(GET_USER_LIST_LIMIT, int(params['offset']))
        limit = int(params['limit'])
    except (ValueError, KeyError):
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
    params = request.rel_url.query
    logging.info(f'Get user by Id {params}')

    try:
        user_id = params['user_id']
    except KeyError:
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
