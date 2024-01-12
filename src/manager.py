import uvicorn
from typing import Annotated
from fastapi import FastAPI, Header, Form
from fastapi.responses import JSONResponse
from accessToken import AccessToken
from accessAuthorization import AccessAuthorization
from util.bsException import BSException
from models.accessAuthorizationModel import AccessAuthorizationModel
from models.accessTokenModel import AccessTokenModel

app = FastAPI(
    title="AuthorizationToken",
    description="This application 'AuthorizationToken', provides endpoints for token generation and authorization. It supports functionalities related to OAuth 2.0, allowing clients to obtain access tokens and authorization to access protected resources. The application is versioned as 0.0.1 and is authored by Daniel Goldacker.",
    version="0.0.1",
    contact={
        "name": "Daniel Goldacker",
        "url": "https://github.com/daniel-goldacker",
        "email": "daniel-goldacker@hotmail.com",
    },
)

@app.post('/oauth/token', tags=["token"], name='token generation', response_model=AccessTokenModel.Response)
def generateAccessToken(client_id: Annotated[str, Form()], client_secret: Annotated[str, Form()], grant_type: Annotated[str, Form()], scope: Annotated[str, Form()]):
    data = AccessToken.generate(client_id, client_secret, grant_type, scope)
    return data


@app.get('/oauth/userinfo', tags=["token"], name='fetch token information', response_model=AccessTokenModel.UserInfo)
def getUserInfo(authorization: str = Header(None, convert_underscores=False)):
    data = AccessToken.decode(authorization)
    return data


@app.post('/oauth/authorize', tags=["authorization"], name='obtain authorization to generate the token', response_model=AccessAuthorizationModel.Response)
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