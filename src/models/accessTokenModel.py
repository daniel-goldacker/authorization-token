from pydantic import BaseModel

class AccessTokenModel : 
    class Response(BaseModel):
        token_type: str
        token: str
        created_date: str
        expire_date: str