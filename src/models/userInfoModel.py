from pydantic import BaseModel
from datetime import datetime

class UserInfoModel:
        class Request(BaseModel):
            uuid: str
            nome: str
            email: str
            application_name: str
            application_description: str
            iat: datetime
            exp: datetime

        class Response(BaseModel):
            uuid: str
            nome: str
            email: str
            application_name: str
            application_description: str
            iat: str
            exp: str