import uvicorn
from fastapi import FastAPI, Response, Header
from accessToken import AccessToken

app = FastAPI()

# Rota para retornar uma mensagem simples
@app.post('/token')
def generateAccessToken(response: Response):
    data = AccessToken.generate()
    return data

@app.get('/userinfo')
def getUserInfo(authorization: str = Header(None, convert_underscores=False)):
    data = AccessToken.decode(authorization)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)