from constants import *

CHARSET = 'utf8mb4'

DATABASE = 'social'
USERS_TABLE = 'users'
AUTH_TABLE = 'auth'

TABLES = {
    USERS_TABLE: {
        'id': 'INT NOT NULL PRIMARY KEY',
        'first_name': 'VARCHAR(255)',
        'last_name': 'VARCHAR(255)',
        'city': 'VARCHAR(255)',
        'udata': 'JSON'
    },
    AUTH_TABLE: {
        'id': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
        'login': f'VARCHAR({AUTH.LOGIN_MAX_SIZE}) UNIQUE',
        'password': f'VARCHAR({AUTH.LOGIN_MAX_SIZE})'
    }
}
