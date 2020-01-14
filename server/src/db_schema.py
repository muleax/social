CHARSET = 'utf8mb4'

DATABASE = 'social'
USERS_TABLE = 'users'

TABLES = {
    USERS_TABLE: {
        'id': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
        'first_name': 'VARCHAR(255)',
        'last_name': 'VARCHAR(255)',
        'city': 'VARCHAR(255)',
        'udata': 'JSON'
    }
}
