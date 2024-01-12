import uvicorn
from typing import Annotated
from fastapi import FastAPI, Header, Form
from fastapi.responses import JSONResponse
from accessToken import AccessToken
from accessAuthorization import AccessAuthorization
from util.bsException import BSException
from models.accessAuthorizationModel import AccessAuthorizationModel

app = FastAPI()

@app.post('/oauth/token')
def generateAccessToken(client_id: Annotated[str, Form()], client_secret: Annotated[str, Form()], grant_type: Annotated[str, Form()], scope: Annotated[str, Form()]):
    data = AccessToken.generate(client_id, client_secret, grant_type, scope)
    return data


@app.get('/oauth/userinfo')
def getUserInfo(authorization: str = Header(None, convert_underscores=False)):
    data = AccessToken.decode(authorization)
    return data


@app.post('/oauth/authorization')
def generateAccessAuthorization(request: AccessAuthorizationModel.Request):
    data = AccessAuthorization.create(request.name, request.email, request.application_name, request.application_description)
    return JSONResponse(
        status_code=201,
        content=data.model_dump()
    )


@app.exception_handler(BSException)
async def bsExceptionHandler(request, exc):
    return JSONResponse(
        status_code=exc.statusCode,
        content={"error": exc.error, "status-code": exc.statusCode}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)