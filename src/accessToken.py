import jwt
import uuid
from datetime import datetime, timedelta
from util.dbConnector import DBConnector
from util.dtConvert import DTConvert 
from util.bsException import BSException
from models.accessTokenModel import AccessTokenModel
from config import ConfigFiles

def removeTokenType(tokenJWT):
    return tokenJWT.replace(ConfigFiles.TOKEN_TYPE_SPACE, "")


class AccessToken:
    def generate():
        privateKey = ConfigFiles.PRIVATE_KEY # Chave secreta para assinar o token
        
        createdDateUTC = datetime.utcnow()
        createdDateBrazil = DTConvert.dateUtcToDateTimeZone(createdDateUTC, ConfigFiles.BRAZIL_TIME_ZONE)

        expireToken = createdDateUTC + timedelta(minutes=ConfigFiles.TIME_EXPIRATION_TOKEN_IN_MINUTES) # Tempo de expiração do token em minutos         
        expireTokenBrazil = DTConvert.dateUtcToDateTimeZone(expireToken, ConfigFiles.BRAZIL_TIME_ZONE) # Tempo de expiração do token em minutos 

        # Informações do usuário (pode ser qualquer informação que deseje incluir)
        userInfos = AccessTokenModel.userInfo(123, 'Exemplo', 'exemplo@email.com', createdDateUTC, expireToken, uuid.uuid4().hex)
        
        # Gerando o token JWT com as informações do usuário
        tokenJWT = jwt.encode(userInfos, privateKey, algorithm='HS256')
        if isinstance(tokenJWT, bytes):
            tokenJWT = tokenJWT.decode('utf-8')

        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        sqlite.executeCommand("INSERT INTO tokens (token, iat, exp) VALUES ('" + tokenJWT + "', '" 
                              + createdDateBrazil.strftime('%d/%m/%Y %H:%M:%S') + "', '" 
                              + expireTokenBrazil.strftime('%d/%m/%Y %H:%M:%S') + "')")
        sqlite.closeConnection()
 
        return AccessTokenModel.response(ConfigFiles.TOKEN_TYPE, tokenJWT,createdDateBrazil.strftime('%d/%m/%Y %H:%M:%S'), expireTokenBrazil.strftime('%d/%m/%Y %H:%M:%S'))


    def valid(tokenJWT):
        if (tokenJWT is None):
            raise BSException(error="Authorization is required", statusCode=401)
        elif (tokenJWT == ''):
            raise BSException(error="Token is required", statusCode=401)
        elif not tokenJWT.startswith(ConfigFiles.TOKEN_TYPE_SPACE):
            raise BSException(error="Token must start with '" + ConfigFiles.TOKEN_TYPE_SPACE + "'", statusCode=401)
        else:
            tokenJWT = removeTokenType(tokenJWT)
    
        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        results = sqlite.executeQuery("SELECT token, exp FROM tokens where token = '"  + tokenJWT + "'")
        sqlite.closeConnection()
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
            tokenJWT = removeTokenType(tokenJWT)
            informacoes_decodificadas = jwt.decode(tokenJWT, privateKey, algorithms=['HS256'])
            return informacoes_decodificadas 
        else:
            raise BSException(error="Token is not valid", statusCode=401)
