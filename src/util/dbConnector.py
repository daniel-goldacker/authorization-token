import sqlite3

class DBConnector:
    class SQLite:
        def __init__(self, database):
            self.database = database
            self.__connection = None
            self.__cursor = None


        def openConnection(self):
            self.__connection = sqlite3.connect(self.database)
            self.__cursor =  self.__connection.cursor()

            initialProcess(self)


        def closeConnection(self):
            self.__connection.close()


        def createTable(self, create):
            self.__cursor.execute(create)


        def executeCommand(self, command):
            self.__cursor.execute(command)
            self.__connection.commit()


        def executeQuery(self, sql):
            self.__cursor.execute(sql)
            return self.__cursor.fetchone()
        
        
def initialProcess(self):
    self.createTable(''' CREATE TABLE IF NOT EXISTS token (
                                                token TEXT PRIMARY KEY,
                                                iat DATETIME,
                                                exp DATETIME
                                            )
                                    ''')
    
    self.createTable(''' CREATE TABLE IF NOT EXISTS authorization (
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                name TEXT,
                                                email TEXT,
                                                status TEXT,
                                                application_name TEXT,
                                                application_description TEXT,
                                                client_id TEXT UNIQUE,
                                                client_secret TEXT UNIQUE,
                                                grant_type TEXT,
                                                scope TEXT
                                            )
                                    ''')