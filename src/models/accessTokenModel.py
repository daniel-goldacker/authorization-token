from pydantic import BaseModel
from datetime import datetime

class AccessTokenModel : 
    class Response(BaseModel):
        token_type: str
        token: str
        created_date: str
        expire_date: str

    class UserInfo(BaseModel):
        id: int
        nome: str
        email: str
        iat: datetime
        exp: datetime
        uuid: str