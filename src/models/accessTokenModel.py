class AccessTokenModel : 
    def response(tokenType, token, createdDate, expireDate):
        return {
            'token-type': tokenType,
            'token': token, 
            'created-date': createdDate,
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