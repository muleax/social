import sys
import time
import pymysql
from constants import *


def init_db(connection):
    connection.begin()
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE %s;" % DATABASE)

    cursor.execute("USE %s;" % DATABASE)
    cursor.execute("CREATE TABLE %s(first_name varchar(255), last_name varchar(255), city varchar(255));" % USERS_TABLE)

    connection.commit()


def add_test_users(connection):
    connection.begin()
    connection.select_db(DATABASE)

    cursor = connection.cursor()

    cursor.execute("INSERT INTO %s VALUES ('Some', 'Test', 'Minsk');" % USERS_TABLE)
    cursor.execute("INSERT INTO %s VALUES ('Aaaa', 'Bbbb', 'Seattle');" % USERS_TABLE)
    cursor.execute("INSERT INTO %s VALUES ('Cccc', 'DDDddd', 'Moscow');" % USERS_TABLE)

    connection.commit()


if __name__ == "__main__":
    connection = None
    for i in range(10):
        time.sleep(5)
        try:
            # TODO: some clever auth
            connection = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                         charset=MYSQL_CHARSET, cursorclass=pymysql.cursors.DictCursor)
        except:
            print("INFO: Couldn't connect to db on %i attempt" % (i + 1))
        else:
            break

    if connection and connection.open:
        print("INFO: Connected to db at %s:%s" % (MYSQL_HOST, MYSQL_PORT))
    else:
        print("ERROR: Couldn't connect to db")
        sys.exit(1)

    try:
        # TODO: proper migration
        connection.select_db(DATABASE)
        print("INFO: Database migrated to the latest version")
    except:
        print("INFO: Initializing database...")
        init_db(connection)
        add_test_users(connection)
        print("INFO: Database initialized")

    connection.close()

    sys.exit(0)
