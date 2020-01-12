CHARSET = 'utf8mb4'

DATABASE = 'social'
USERS_TABLE = 'users'

TABLES = {
    USERS_TABLE: {
        'first_name': 'varchar(255)',
        'last_name': 'varchar(255)',
        'city': 'varchar(255)',
        'udata': 'json'
    }
}
