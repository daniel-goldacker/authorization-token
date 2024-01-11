import uvicorn
from fastapi import FastAPI, Response
from accessToken import AccessToken

app = FastAPI()

# Rota para retornar uma mensagem simples
@app.post('/token')
def integration(response: Response):
    data = AccessToken.generate()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)