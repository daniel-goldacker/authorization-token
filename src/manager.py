import uvicorn
from fastapi import FastAPI, Response, Header
from fastapi.responses import JSONResponse
from accessToken import AccessToken
from accessAuthorization import AccessAuthorization
from util.bsException import BSException
from models.accessAuthorizationModel import AccessAuthorizationModel

app = FastAPI()

@app.post('/oauth/token')
def generateAccessToken(response: Response):
    data = AccessToken.generate()
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