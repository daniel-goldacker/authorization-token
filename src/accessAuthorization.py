import uuid
from config import ConfigFiles, ConfigAuthorization
from util.dbConnector import DBConnector
from util.bsException import BSException
from models.accessAuthorizationModel import AccessAuthorizationModel

class AccessAuthorization:
    def create(name, email, appName, appDescription):  
        clientId = str(uuid.uuid4())
        clientSecret = uuid.uuid4().hex

        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        sqlite.executeCommand("INSERT INTO authorization (name, email, status, application_name, " +
                                                          "application_description, client_id, " +
                                                          "client_secret, grant_type, scope) " +
                                                    "VALUES ('" + name + "', '" + email + "', " 
                                                            "'" + ConfigAuthorization.AUTHORIZATION_STATUS + "', "
                                                            "'" + appName+ "', '" + appDescription + "', " 
                                                            "'" + clientId+ "', '" + clientSecret + "', "
                                                            "'" + ConfigAuthorization.AUTHORIZATION_GRANT_TYPE + "', "
                                                            "'" + ConfigAuthorization.AUTHORIZATION_SCOPE + "')")
        sqlite.closeConnection()

        return AccessAuthorizationModel.Response(name=name, email=email, application_name=appName, application_description=appDescription, 
                                                status=ConfigAuthorization.AUTHORIZATION_STATUS, client_id=clientId, client_secret=clientSecret, 
                                                grant_type=ConfigAuthorization.AUTHORIZATION_GRANT_TYPE, scope=ConfigAuthorization.AUTHORIZATION_SCOPE)
    

    def valid(clientId, clientSecret, grantType, scope):
        if (grantType != ConfigAuthorization.AUTHORIZATION_GRANT_TYPE):
            raise BSException(error="The app requested an unsupported grant type '" + grantType + "'", statusCode=400)
        elif (scope is None) or (scope == ''):
            raise BSException(error="The request body must contain the following parameter: 'scope'", statusCode=400)
        elif (scope != ConfigAuthorization.AUTHORIZATION_SCOPE):
            raise BSException(error="The provided value for scope '" + scope + "' is not valid'", statusCode=400)
        
        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        results = sqlite.executeQuery("SELECT client_secret, status FROM authorization where client_id = '"  + clientId + "'")
        sqlite.closeConnection()
        if results:
            if (results[0] == clientSecret):
                if (results[1] == ConfigAuthorization.AUTHORIZATION_STATUS):
                    return True
                else:
                    raise BSException(error="Application with identifier '" + clientId + "' is not '" + ConfigAuthorization.AUTHORIZATION_STATUS + "'", statusCode=400)    
            else:
                raise BSException(error="Invalid client secret provided. Ensure the secret being sent in the request is the client secret value, not the client secret ID, for a secret added to app '" + clientId + "'", statusCode=400)
        else:
          raise BSException(error="Application with identifier '" + clientId + "' was not found in the directory", statusCode=400)      
    
    
    def getAuthorizationInfos(clientId, clientSecret):
        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        results = sqlite.executeQuery("SELECT name, email, status, application_name, " +
                                              "application_description, client_id, " +
                                              "client_secret, grant_type, scope " +
                                            "FROM authorization where client_id = '"  + clientId + "' and client_secret = '" + clientSecret + "'")
        sqlite.closeConnection()
        if results:
            return AccessAuthorizationModel.Response(name=results[0], email=results[1], status=results[2], application_name=results[3], 
                                                     application_description=results[4], client_id=results[5], client_secret=results[6], 
                                                     grant_type=results[7], scope=results[8])
      