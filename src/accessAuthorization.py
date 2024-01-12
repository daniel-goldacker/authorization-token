import uuid
from util.dbConnector import DBConnector
from util.bsException import BSException
from models.accessAuthorizationModel import AccessAuthorizationModel
from config import ConfigFiles

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
                                                            "'" + ConfigFiles.AUTHORIZATION_STATUS + "', "
                                                            "'" + appName+ "', '" + appDescription + "', " 
                                                            "'" + clientId+ "', '" + clientSecret + "', "
                                                            "'" + ConfigFiles.AUTHORIZATION_GRANT_TYPE + "', "
                                                            "'" + ConfigFiles.AUTHORIZATION_SCOPE + "')")
        sqlite.closeConnection()

        return AccessAuthorizationModel.Response(name=name, email=email, application_name=appName, application_description=appDescription, 
                                                status=ConfigFiles.AUTHORIZATION_STATUS, client_id=clientId, client_secret=clientSecret, 
                                                grant_type=ConfigFiles.AUTHORIZATION_GRANT_TYPE, scope=ConfigFiles.AUTHORIZATION_SCOPE)
    

    def valid(clientId, clientSecret, grant_type, scope):

        if (clientId is None) or (clientId == ''):
            raise BSException(error="The request body must contain the following parameter: 'client_id'", statusCode=400)
        elif (clientSecret is None) or (clientSecret == ''):
            raise BSException(error="The request body must contain the following parameter: 'client_secret'", statusCode=400)
        elif (grant_type is None) or (grant_type == ''):
            raise BSException(error="The request body must contain the following parameter: 'grant_type'", statusCode=400)
        elif (grant_type != ConfigFiles.AUTHORIZATION_GRANT_TYPE):
            raise BSException(error="The app requested an unsupported grant type '" + grant_type + "'", statusCode=400)
        elif (scope is None) or (scope == ''):
            raise BSException(error="The request body must contain the following parameter: 'scope'", statusCode=400)
        elif (scope != ConfigFiles.AUTHORIZATION_SCOPE):
            raise BSException(error="The provided value for scope '" + scope + "' is not valid'" + grant_type + "'", statusCode=400)
        
        sqlite = DBConnector.SQLite(ConfigFiles.DATABASE_SQLITE)
        sqlite.openConnection()
        results = sqlite.executeQuery("SELECT application_name FROM authorization where client_id = '"  + clientId + "' and client_secret = '" + clientSecret + "'")
        sqlite.closeConnection()
        if results:
            if (results[0] is not None):
                return True
            else:
                return False
        else:
          return False      
    