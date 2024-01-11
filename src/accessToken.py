import jwt
from datetime import datetime, timedelta
from util.dbConnector import DBConnector
from models.accessTokenModel import AccessTokenModel
from config import ConfigFiles

class AccessToken:
    def generate():
        privateKey = ConfigFiles.PRIVATE_KEY # Chave secreta para assinar o token
        expireToken = datetime.now() + timedelta(hours=1) # Tempo de expiração do token (1 hora a partir de agora)

        # Informações do usuário (pode ser qualquer informação que deseje incluir)
        informacoes_usuario = {
            'id': 123,
            'nome': 'Exemplo',
            'email': 'exemplo@email.com',
            'exp': expireToken.isoformat()  
        }

        # Gerando o token JWT com as informações do usuário
        tokenJWT = jwt.encode(informacoes_usuario, privateKey, algorithm='HS256')
        


        sqlite = DBConnector.SQLite('src/database/authenticator.db')
        sqlite.openConnection()
        sqlite.createTable(''' CREATE TABLE IF NOT EXISTS tokens (
                                    token TEXT PRIMARY KEY,
                                    exp DATETIME
                                )
                            ''')
        sqlite.executeCommand("INSERT INTO tokens (token, exp) VALUES ('" + tokenJWT + "', '" + expireToken.strftime('%d/%m/%Y %H:%M:%S') + "')")
        sqlite.closeConnection()
     
        return AccessTokenModel.response(tokenJWT,expireToken.strftime('%d/%m/%Y %H:%M:%S'))
    
    def decode(tokenJWT):
        privateKey = ConfigFiles.PRIVATE_KEY # Chave secreta para assinar o token

        try:
            # Decodificando o token usando a mesma chave secreta
            informacoes_decodificadas = jwt.decode(tokenJWT, privateKey, algorithms=['HS256'])
            
            # Exibindo as informações decodificadas
            print("Informações do usuário:")
            print(informacoes_decodificadas)
        except jwt.ExpiredSignatureError:
            print("Token expirado. Por favor, gere um novo token.")
        except jwt.InvalidTokenError:
            print("Token inválido. Verifique a chave secreta ou o formato do token.")
