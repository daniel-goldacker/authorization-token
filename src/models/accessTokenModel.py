class AccessTokenModel : 
    def response(token, expireDate):
        return {
            'token': token, 
            'expire-date': expireDate
        }