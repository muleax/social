import sys
import logging
import argparse
import asyncio
from db_init import *
from db_dev_utils import *
from db_replication import *
from db_connection import open_connection
import yaml


async def social_db_provision(cfg):
    master_cfg = cfg['social_db']['master']
    slave_cfgs = cfg['social_db']['slaves']

    connection = await open_connection(master_cfg['host'], master_cfg['port'], master_cfg['user'], master_cfg['password'])
    connection.autocommit(True)

    if not connection:
        logging.error(f"Failed to connect to {SOCIAL_DATABASE}")
        return

    if is_fresh_db(connection, SOCIAL_SCHEMA):
        await make_master(master_cfg, slave_cfgs)
        for slave_cfg in slave_cfgs:
            await make_slave(master_cfg, slave_cfg)

        create_tables(connection, SOCIAL_SCHEMA)
        create_indexes(connection, SOCIAL_SCHEMA)
        if IS_DEVELOPMENT:
            create_test_users(connection, INITIAL_TEST_USERS_COUNT)

        logging.info(f"Database {SOCIAL_DATABASE} initialized")
    else:
        # TODO: proper migration
        logging.info(f"Using existing database {SOCIAL_DATABASE}")

    connection.close()


async def chat_db_provision(cfg):
    chat_shard_cfgs = cfg['chat_db']

    for shard_cfg in chat_shard_cfgs:
        connection = await open_connection(shard_cfg['host'], shard_cfg['port'], shard_cfg['user'], shard_cfg['password'])
        connection.autocommit(True)

        if not connection:
            logging.error(f"Failed to connect to {SOCIAL_CHAT_DATABASE}")
            continue

        if is_fresh_db(connection, SOCIAL_CHAT_SCHEMA):
            create_tables(connection,  SOCIAL_CHAT_SCHEMA)
            create_indexes(connection, SOCIAL_CHAT_SCHEMA)

            logging.info(f"Database {SOCIAL_CHAT_DATABASE} initialized")
        else:
            # TODO: proper migration
            logging.info(f"Using existing database {SOCIAL_CHAT_DATABASE}")

        connection.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg-file', type=str, default='')
    args = parser.parse_args()

    cfg = yaml.full_load(open(args.cfg_file).read())

    await social_db_provision(cfg)

    await chat_db_provision(cfg)

    sys.exit(0)

if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.get_event_loop().run_until_complete(main())
