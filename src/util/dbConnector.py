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