class AccessTokenModel : 
    def response(token, expireDate):
        return {
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