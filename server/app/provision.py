import sys
import logging
import argparse
import asyncio
from db_create_tables import *
from db_dev_utils import *
from db_replication import *
from db_connection import open_connection
import yaml


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg-file', type=str, default='')
    args = parser.parse_args()

    cfg = yaml.full_load(open(args.cfg_file).read())

    master_cfg = cfg['db']['master']
    slave_cfgs = cfg['db']['slaves']

    await make_master(master_cfg, slave_cfgs)
    for slave_cfg in slave_cfgs:
        await make_slave(master_cfg, slave_cfg)

    connection = await open_connection(master_cfg['host'], master_cfg['port'], master_cfg['user'], master_cfg['password'])
    connection.autocommit(True)

    if not connection:
        sys.exit(1)

    if is_fresh_db(connection):
        create_tables(connection)
        if IS_DEVELOPMENT:
            create_test_users(connection, INITIAL_TEST_USERS_COUNT)

        logging.info("Database initialized")
    else:
        # TODO: proper migration
        logging.info("Using existing database")

    connection.close()

    sys.exit(0)

if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.get_event_loop().run_until_complete(main())
