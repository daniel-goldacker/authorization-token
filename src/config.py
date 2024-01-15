class ConfigFiles():
    DATABASE_SQLITE = 'src/database/authenticator.db'
    BRAZIL_TIME_ZONE = 'America/Sao_Paulo'


class ConfigToken():
    TOKEN_TYPE = 'Bearer'
    TOKEN_TYPE_SPACE = TOKEN_TYPE + ' '
    TOKEN_JWT_ALGORITHMS = 'HS256'
    TOKEN_PRIVATE_KEY = 'P17B8JZH1PRACVEC5W4IJXH2FZKD6ZFB8T5OAEFWG7VHJE40MQ'
    TOKEN_TIME_EXPIRATION_IN_MINUTES = 60


class ConfigAuthorization():    
    AUTHORIZATION_SCOPE = 'default_scope'
    AUTHORIZATION_STATUS = 'ACTIVE'
    AUTHORIZATION_GRANT_TYPE = 'client_credentials'
    