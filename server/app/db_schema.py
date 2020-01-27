from constants import *

CHARSET = 'utf8mb4'

DATABASE = 'social'
USERS_TABLE = 'users'
AUTH_TABLE = 'auth'

TABLES = {
    USERS_TABLE: {
        'user_id': 'INT NOT NULL PRIMARY KEY',
        'first_name': f'VARCHAR({USER_NAME.FIRST_NAME_MAX_SIZE}) DEFAULT ""',
        'last_name': f'VARCHAR({USER_NAME.LAST_NAME_MAX_SIZE}) DEFAULT ""',
        'city': f'VARCHAR({CITY.MAX_SIZE}) DEFAULT ""',
        'birth_date': 'DATE DEFAULT "1970-01-01"',
        'udata': 'JSON NOT NULL'
    },
    AUTH_TABLE: {
        'login': f'VARCHAR({AUTH.LOGIN_MAX_SIZE}) NOT NULL PRIMARY KEY',
        'user_id': 'INT NOT NULL AUTO_INCREMENT UNIQUE',
        'password': f'VARCHAR({AUTH.LOGIN_MAX_SIZE}) NOT NULL'
    }
}

ALL_USER_FIELDS = TABLES[USERS_TABLE].keys()
PUBLIC_USER_FIELDS = ('user_id', 'first_name', 'last_name', 'city', 'birth_date', 'udata')
PREVIEW_USER_FIELDS = ('user_id', 'first_name', 'last_name', 'city', 'birth_date')
EDITABLE_USER_FIELDS = ('first_name', 'last_name', 'city', 'birth_date', 'udata')
