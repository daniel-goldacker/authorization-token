from pydantic import BaseModel

class AccessAuthorizationModel:
    class Request(BaseModel):
        name: str
        email: str
        application_name: str
        application_description: str

    class Response(BaseModel):
        name: str
        email: str
        application_name: str
        application_description: str
        status: str
        client_id: str
        client_secret: str
        grant_type: str
        scope: str

