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