from constants import *

CHARSET = 'utf8mb4'

SOCIAL_DATABASE = 'social'
USERS_TABLE = 'users'
AUTH_TABLE = 'auth'

SOCIAL_SCHEMA = {
    'name': SOCIAL_DATABASE,
    'tables': {
        USERS_TABLE: {
            'schema': {
                'user_id': 'INT NOT NULL',
                'first_name': f'VARCHAR({USER_NAME.FIRST_NAME_MAX_SIZE}) DEFAULT ""',
                'last_name': f'VARCHAR({USER_NAME.LAST_NAME_MAX_SIZE}) DEFAULT ""',
                'city': f'VARCHAR({CITY.MAX_SIZE}) DEFAULT ""',
                'birth_date': 'DATE DEFAULT "1970-01-01"',
                'udata': 'JSON NOT NULL'
            },
            'indexes': {
                'lfcb_idx': ('last_name', 'first_name', 'city', 'birth_date'),
                'fcb_idx': ('first_name', 'city', 'birth_date'),
                'cb_idx': ('city', 'birth_date'),
                'b_idx': ('birth_date',)
            },
            'primary_key': ('user_id',)
        },
        AUTH_TABLE: {
            'schema': {
                'login': f'VARCHAR({AUTH.LOGIN_MAX_SIZE}) NOT NULL',
                'user_id': 'INT NOT NULL AUTO_INCREMENT UNIQUE',
                'password': f'VARCHAR({AUTH.LOGIN_MAX_SIZE}) NOT NULL'
            },
            'indexes': {},
            'primary_key': ('login',)
        }
    }
}

ALL_USER_FIELDS = SOCIAL_SCHEMA['tables'][USERS_TABLE]['schema'].keys()
PUBLIC_USER_FIELDS = ('user_id', 'first_name', 'last_name', 'city', 'birth_date', 'udata')
PREVIEW_USER_FIELDS = ('user_id', 'first_name', 'last_name', 'city', 'birth_date')
EDITABLE_USER_FIELDS = ('first_name', 'last_name', 'city', 'birth_date', 'udata')


SOCIAL_CHAT_DATABASE = 'social_chat'
CHAT_TABLE = 'chat'
CHAT_MESSAGES_TABLE = 'chat_messages'

SOCIAL_CHAT_SCHEMA = {
    'name': SOCIAL_CHAT_DATABASE,
    'tables': {
        CHAT_MESSAGES_TABLE: {
            'schema': {
                'message_id': 'BIGINT AUTO_INCREMENT',
                'user_id_lower': 'INT NOT NULL',
                'user_id_higher': 'INT NOT NULL',
                'message': 'TEXT',
                'datetime': 'DATETIME'
            },
            'indexes': {
                'lhd_idx': ('user_id_lower', 'user_id_higher', 'datetime'),
                'hd_idx': ('user_id_higher', 'datetime')
            },
            'primary_key': ('message_id',)
        },
        CHAT_TABLE: {
            'schema': {
                'user_id': 'INT NOT NULL',
                'other_user_id': 'INT NOT NULL'
            },
            'indexes': {},
            'primary_key': ('user_id', 'other_user_id')
        }
    }
}
