import logging
from db_schema import *
from db_connection import open_connection


async def make_master(master_cfg, slave_cfgs):
    logging.info(f"Configuring master {master_cfg['host']}:{master_cfg['port']}")

    connection = await open_connection(master_cfg['host'], master_cfg['port'], master_cfg['user'], master_cfg['password'])
    connection.autocommit(True)

    if not connection:
        return False

    cursor = connection.cursor()

    for slave_cfg in slave_cfgs:
        sql = f"CREATE USER '{slave_cfg['slave_user']}'@'%' \
                IDENTIFIED WITH mysql_native_password BY '{slave_cfg['slave_password']}';"
        # TODO: error check
        cursor.execute(sql)

        sql = f"GRANT REPLICATION SLAVE ON *.* TO '{slave_cfg['slave_user']}'@'%';"
        cursor.execute(sql)

    return True


async def make_slave(master_cfg, slave_cfg):
    logging.info(f"Configuring slave {slave_cfg['host']}:{slave_cfg['port']}")

    connection = await open_connection(slave_cfg['host'], slave_cfg['port'], slave_cfg['user'], slave_cfg['password'])
    connection.autocommit(True)

    if not connection:
        return False

    cursor = connection.cursor()

    sql = f"CHANGE MASTER TO MASTER_HOST='{master_cfg['host']}', MASTER_PORT={master_cfg['port']},\
            MASTER_USER='{slave_cfg['slave_user']}', MASTER_PASSWORD='{slave_cfg['slave_password']}';"
    cursor.execute(sql)

    # TODO: error check
    cursor.execute('START SLAVE;')

    return True
