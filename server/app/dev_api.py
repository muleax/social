import logging
from constants import *
from utils import *
from db_schema import *


async def user_list_full(request):
    if not IS_DEVELOPMENT:
        build_response(STATUS.BAD_REQUEST)

    payload = await request.json()
    logging.info(f'[DEV] User list full {payload}')

    requested_ids = payload['user_ids']

    requested_ids_sql = ', '.join(map(str, requested_ids))

    cursor = request.app.master_db_connection.cursor()
    cursor.execute(f"SELECT * FROM {USERS_TABLE} WHERE user_id IN ({requested_ids_sql})")
    user_records = cursor.fetchall()

    cursor.execute(f"SELECT * FROM {AUTH_TABLE} WHERE user_id IN ({requested_ids_sql})")
    auth_records = cursor.fetchall()

    d = dict((e['user_id'], format_user_data(e)) for e in user_records)
    for e in auth_records:
        record = d[e['user_id']]
        record.update(e)
        record['auth_token'] = get_auth_token(e['user_id'])

    return build_response(STATUS.SUCCESS, list(d.values()))


async def max_user_id(request):
    if not IS_DEVELOPMENT:
        build_response(STATUS.BAD_REQUEST)

    logging.info(f'[DEV] Get max user_id')

    cursor = request.app.master_db_connection.cursor()
    cursor.execute(f"SELECT max(user_id) FROM {AUTH_TABLE}")
    record = cursor.fetchone()

    return build_response(STATUS.SUCCESS, {'user_id': next(iter(record.values()))})


async def test_no_db(request):
    if not IS_DEVELOPMENT:
        build_response(STATUS.BAD_REQUEST)

    logging.info(f'[DEV] Test no db')

    value = max(range(100))
    return build_response(STATUS.SUCCESS)
