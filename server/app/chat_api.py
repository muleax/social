import logging
from constants import *
from utils import *
from db_schema import *





def get_messages(request):
    params = request.rel_url.query
    logging.info(f'Get messages {params}')

    try:
        user_id = params['user_id']
        if not check_auth_token(user_id, params['auth_token']):
            logging.info('Token mismatch')
            return build_response(STATUS.BAD_REQUEST)

        other_user_id = params['other_user_id']
        bucket_offset = int(params['bucket_offset'])



    except (ValueError, KeyError) as err:
        logging.debug(f"Get messages bad request: {err}")
        return build_response(STATUS.BAD_REQUEST)

    # request.app.chat_shard_db_connections[]


def post_message(request):
    pass
