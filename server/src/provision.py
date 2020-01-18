import sys
import logging
import argparse
import asyncio
from db_create_tables import *
from db_dev_utils import *
from db_connection import open_connection


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-host', type=str, default='localhost')
    parser.add_argument('--db-port', type=int, default=3306)
    parser.add_argument('--db-user', type=str, default='root')
    parser.add_argument('--db-password', type=str, default='')
    args = parser.parse_args()

    print(args)

    connection = await open_connection(args.db_host, args.db_port, args.db_user, args.db_password)
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
