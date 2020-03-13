import logging
import db_connection
import yaml
import auth_api
import profile_api
import chat_api
import dev_api
from aiohttp import web
from db_schema import *
from constants import *
from utils import *


def create_routes(app):
    app.router.add_post('/create_account', auth_api.create_account)
    app.router.add_get('/auth', auth_api.auth)

    app.router.add_post('/update_user', profile_api.update_user)
    app.router.add_get('/user', profile_api.user)
    app.router.add_get('/find_users', profile_api.find_users)
    app.router.add_get('/user_list', profile_api.user_list)

    app.router.add_post('/post_message', chat_api.post_message)
    app.router.add_get('/get_messages', chat_api.get_messages)

    app.router.add_get('/test_no_db', dev_api.test_no_db)
    app.router.add_get('/user_list_full', dev_api.user_list_full)
    app.router.add_get('/max_user_id', dev_api.max_user_id)


def app_factory(cfg_file):
    app = web.Application()

    cfg = yaml.full_load(open(cfg_file).read())
    master_cfg = cfg['social_db']['master']
    slave_cfgs = cfg['social_db']['slaves']
    chat_shard_cfgs = cfg['chat_db']

    async def on_startup(app):
        master_connection = await db_connection.open_connection(
            master_cfg['host'], master_cfg['port'], master_cfg['user'], master_cfg['password'])

        if master_connection:
            master_connection.autocommit(True)
            master_connection.cursor().execute(f'USE {SOCIAL_DATABASE}')
            logging.info('Worker connected to db')
            create_routes(app)
        else:
            logging.info('Worker failed to connect to db!')
            # TODO

        app.master_db_connection = master_connection

        app.slave_db_connections = []
        for slave_cfg in slave_cfgs:
            connection = await db_connection.open_connection(
                slave_cfg['host'], slave_cfg['port'], slave_cfg['user'], slave_cfg['password'])
            connection.cursor().execute(f'USE {SOCIAL_DATABASE}')

            app.slave_db_connections.append(connection)

        app.chat_shard_db_connections = {}
        for shard_cfg in chat_shard_cfgs:
            connection = await db_connection.open_connection(
                shard_cfg['host'], shard_cfg['port'], shard_cfg['user'], shard_cfg['password'])
            connection.autocommit(True)
            connection.cursor().execute(f'USE {SOCIAL_CHAT_DATABASE}')

            app.chat_shard_db_connections[shard_cfg['shard_id']] = connection

    app.on_startup.append(on_startup)
    return app


logging.basicConfig(level=LOG_LEVEL)
