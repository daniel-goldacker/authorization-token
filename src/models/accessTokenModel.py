class AccessTokenModel : 
    def response(tokenType, token, expireDate):
        return {
            'token-type': tokenType,
            'token': token, 
            'expire-date': expireDate
        }
    
    def userInfo(id, nome, email, iat, exp, uuid):
        return {
            'id': id,
            'nome': nome,
            'email': email,
            'iat': iat, 
            'exp': exp,
            'uuid': uuid
        }