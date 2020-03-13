import logging
import datetime
from constants import *
from utils import *
from db_schema import *


def calculate_birth_date(age, today_date):
    try:
        return today_date.replace(year=(today_date.year - age))
    except ValueError:
        return today_date.replace(year=(today_date.year - age), month=3, day=1)


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
        cursor = request.app.master_db_connection.cursor()
        sql = f"UPDATE {USERS_TABLE} SET {set_statement} WHERE user_id = {user_id}"
        cursor.execute(sql)
        # enrich updated data with return updated data
        return build_response(STATUS.SUCCESS)

    except Exception as err:
        logging.exception(err)
        return build_response(STATUS.SERVER_ERROR)


async def find_users(request):
    params = request.rel_url.query
    logging.info(f'Find users {params}')

    try:
        user_id = params['user_id']
        if not check_auth_token(user_id, params['auth_token']):
            logging.info('Token mismatch')
            return build_response(STATUS.BAD_REQUEST)

        limit = min(FIND_USERS_LIMIT, int(params['limit']))
        offset = int(params['offset'])

        eq_search_order = ('city', 'first_name', 'last_name')
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
        logging.info('not_constraints_sql')
        return build_response(STATUS.BAD_REQUEST)

    constraints_sql.append(f"user_id != {user_id}")
    search_condition = ' AND '.join(constraints_sql)

    try:
        slave_conns = request.app.slave_db_connections
        if slave_conns:
            # This is probably not the most efficient way to balance requests,
            # as each worker need to keep connection to each slave.
            # Instead we can dedicate each worker to single slave,
            # but this is requires a bit more of managing logic.
            slave_id = int(user_id) % len(slave_conns)
            connection = slave_conns[slave_id]
        else:
            connection = request.app.master_db_connection

        cursor = connection.cursor()
        preview_fields = ', '.join(PREVIEW_USER_FIELDS)
        sql = f"SELECT {preview_fields} FROM {USERS_TABLE} WHERE {search_condition} LIMIT {limit} OFFSET {offset}"
        # logging.debug(f"Find users sql: {sql}")
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
        limit = min(GET_USER_LIST_LIMIT, int(params['limit']))
        offset = int(params['offset'])
    except (ValueError, KeyError):
        return build_response(STATUS.BAD_REQUEST)

    public_fields = ', '.join(PUBLIC_USER_FIELDS)

    try:
        cursor = request.app.master_db_connection.cursor()
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

    cursor = request.app.master_db_connection.cursor()
    cursor.execute(f"SELECT {public_fields} FROM {USERS_TABLE} WHERE user_id={user_id}")
    record = cursor.fetchone()
    if record:
        record = format_user_data(record)

    return build_response(STATUS.SUCCESS, record)
