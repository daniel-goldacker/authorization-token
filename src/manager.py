import uvicorn
from fastapi import FastAPI, Response
from authenticator import Token

app = FastAPI()

# Rota para retornar uma mensagem simples
@app.post('/token')
def integration(response: Response):
    data = Token.generate()
    response.headers["Content-Type"] = "application/json"
    return data


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=log_config)