
IS_DEVELOPMENT = True

class STATUS:
    SUCCESS = 200
    BAD_REQUEST = 400
    SERVER_ERROR = 500

class AUTH:
    JWT_SECRET = 'Oops'
    JWT_SALT = 'Oooops'
    LOGIN_MAX_SIZE = 63
    PASSWORD_MAX_SIZE = 63

GET_USERS_LIMIT = 1000
