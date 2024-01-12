from pydantic import BaseModel
from datetime import datetime

class AccessTokenModel : 
    class Response(BaseModel):
        token_type: str
        token: str
        created_date: str
        expire_date: str

    class UserInfo(BaseModel):
        uuid: str
        nome: str
        email: str
        application_name: str
        application_description: str
        iat: datetime
        exp: datetime
        