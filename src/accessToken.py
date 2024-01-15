import jwt
import uuid
from config import ConfigFiles, ConfigToken
from datetime import datetime, timedelta
from utils.dbConnector import DBConnector
from utils.dtConvert import DTConvert 
from utils.bsException import BSException
from models.accessTokenModel import AccessTokenModel
from models.userInfoModel import UserInfoModel
from accessAuthorization import AccessAuthorization

def removeTokenType(tokenJWT):
    return tokenJWT.replace(ConfigToken.TOKEN_TYPE_SPACE, "")


class AccessToken:
    def generate(clientId, clientSecret, grantType, scope):

        if AccessAuthorization.valid(clientId, clientSecret, grantType, scope):
            createdDateUTC = datetime.utcnow()
            createdDateBrazil = DTConvert.dateUtcToDateTimeZone(createdDateUTC, ConfigFiles.BRAZIL_TIME_ZONE)

            expireToken = createdDateUTC + timedelta(minutes=ConfigToken.TIME_EXPIRATION_TOKEN_IN_MINUTES)      
            expireTokenBrazil = DTConvert.dateUtcToDateTimeZone(expireToken, ConfigFiles.BRAZIL_TIME_ZONE)

            authorizationInfos = AccessAuthorization.getAuthorizationInfos(clientId, clientSecret)
            
            userInfos = UserInfoModel.Request(uuid=uuid.uuid4().hex, nome=authorizationInfos.name, email=authorizationInfos.email, 
                                              application_name=authorizationInfos.application_name, 
                                              application_description=authorizationInfos.application_description, 
                                              iat=createdDateUTC, exp=expireToken)
            
            tokenJWT = jwt.encode(userInfos.model_dump(), ConfigToken.PRIVATE_KEY, algorithm='HS256')
            if isinstance(tokenJWT, bytes):
                tokenJWT = tokenJWT.decode('utf-8')

            sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
            sqlite.openConnection()
            sqlite.executeCommand("INSERT INTO token (token, iat, exp) VALUES ('" + tokenJWT + "', '" 
                                + createdDateBrazil.strftime('%d/%m/%Y %H:%M:%S') + "', '" 
                                + expireTokenBrazil.strftime('%d/%m/%Y %H:%M:%S') + "')")
            sqlite.closeConnection()
            return AccessTokenModel.Response(token_type=ConfigToken.TOKEN_TYPE, token=tokenJWT, 
                                             created_date=createdDateBrazil.strftime('%d/%m/%Y %H:%M:%S'), 
                                             expire_date=expireTokenBrazil.strftime('%d/%m/%Y %H:%M:%S'))
        else:
            raise BSException(error="Error granting authorization", statusCode=401) 


    def valid(tokenJWT):
        if (tokenJWT is None) or (tokenJWT == ''):
            raise BSException(error="The request header must contain the following parameter: 'Authorization'", statusCode=401)
        elif not tokenJWT.startswith(ConfigToken.TOKEN_TYPE_SPACE):
            raise BSException(error="Token must start with '" + ConfigToken.TOKEN_TYPE_SPACE + "'", statusCode=401)
        else:
            tokenJWT = removeTokenType(tokenJWT)
    
        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        results = sqlite.executeQuery("SELECT token, exp FROM token where token = '"  + tokenJWT + "'")
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
        if AccessToken.valid(tokenJWT):
            tokenJWT = removeTokenType(tokenJWT)
            codedInformation = jwt.decode(tokenJWT, ConfigToken.PRIVATE_KEY, algorithms=['HS256'])

            iat = datetime.utcfromtimestamp(codedInformation['iat'])
            iat = DTConvert.dateUtcToDateTimeZone(iat, ConfigFiles.BRAZIL_TIME_ZONE)

            exp = datetime.utcfromtimestamp(codedInformation['exp'])
            exp = DTConvert.dateUtcToDateTimeZone(exp, ConfigFiles.BRAZIL_TIME_ZONE)

            return UserInfoModel.Response(uuid=codedInformation['uuid'], 
                                             nome=codedInformation['nome'], 
                                             email=codedInformation['email'], 
                                             application_name=codedInformation['application_name'], 
                                             application_description=codedInformation['application_description'], 
                                             iat=iat.strftime('%d/%m/%Y %H:%M:%S'), 
                                             exp=exp.strftime('%d/%m/%Y %H:%M:%S')) 
        else:
            raise BSException(error="Token is not valid", statusCode=401)
