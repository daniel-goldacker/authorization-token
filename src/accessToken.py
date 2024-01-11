import jwt
import pytz
from datetime import datetime, timedelta
from util.dbConnector import DBConnector
from models.accessTokenModel import AccessTokenModel
from config import ConfigFiles

class AccessToken:
    def generate():
        privateKey = ConfigFiles.PRIVATE_KEY # Chave secreta para assinar o token
        expireToken = datetime.utcnow() + timedelta(minutes=ConfigFiles.TIME_EXPIRATION_TOKEN_IN_MINUTES) # Tempo de expiração do token em minutos

        # Informações do usuário (pode ser qualquer informação que deseje incluir)
        userInfos = AccessTokenModel.userInfo(123, 'Exemplo', 'exemplo@email.com', expireToken)
        
        # Gerando o token JWT com as informações do usuário
        tokenJWT = jwt.encode(userInfos, privateKey, algorithm='HS256')
        if isinstance(tokenJWT, bytes):
            tokenJWT = tokenJWT.decode('utf-8')

        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        sqlite.createTable(''' CREATE TABLE IF NOT EXISTS tokens (
                                    token TEXT PRIMARY KEY,
                                    exp DATETIME
                                )
                            ''')
        

        brazilTimeZone = pytz.timezone(ConfigFiles.BRAZIL_TIME_ZONE)
        expireTokenBrazil = expireToken.replace(tzinfo=pytz.utc).astimezone(brazilTimeZone)

        sqlite.executeCommand("INSERT INTO tokens (token, exp) VALUES ('" + tokenJWT + "', '" + expireTokenBrazil.strftime('%d/%m/%Y %H:%M:%S') + "')")

     
        return AccessTokenModel.response(tokenJWT, expireTokenBrazil.strftime('%d/%m/%Y %H:%M:%S'))


    def valid(tokenJWT):
        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        results = sqlite.executeQuery("SELECT token, exp FROM tokens where token = '"  + tokenJWT + "'")
        if results:
            dateExpireToken = datetime.strptime(results[1], '%d/%m/%Y %H:%M:%S')
            if (datetime.now() <= dateExpireToken):
                return True
            else:
                return False
        else:
          return False      

    
    def decode(tokenJWT):
        privateKey = ConfigFiles.PRIVATE_KEY # Chave secreta para assinar o token

        if AccessToken.valid(tokenJWT):
            informacoes_decodificadas = jwt.decode(tokenJWT, privateKey, algorithms=['HS256'])
            return informacoes_decodificadas 
        else:
            return False