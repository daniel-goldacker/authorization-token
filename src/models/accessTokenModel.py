class AccessTokenModel : 
    def response(token, expireDate):
        return {
            'token': token, 
            'expire-date': expireDate
        }
    
    def userInfo(id, nome, email, exp):
        return {
            'id': id,
            'nome': nome,
            'email': email,
            'exp': exp 
        }