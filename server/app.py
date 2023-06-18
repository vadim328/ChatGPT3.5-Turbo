from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from openai_api import send_request, get_image, translate
from settings import FASTAPI_ACCESS_TOKEN

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat")
async def bot(data: Dict[str, Any]):
    if not authorization(data['token']):
        raise HTTPException(
            status_code=403, detail="Authentication failed"
        )
    response = send_request(data['prompt'])
    return {"message": response}


@app.post("/image")
async def image(data: Dict[str, Any]):
    if not authorization(data['token']):
        raise HTTPException(
            status_code=403, detail="Authentication failed"
        )
    translated_result = translate(data["prompt"])
    response = get_image(translated_result['choices'][0]['text'])
    return {"image_urls": response}


def authorization(token):
    if FASTAPI_ACCESS_TOKEN == token:
        return True
    else:
        return False


@app.get("/hello")
async def hello():
    return {"message": 'Hello!!!!'}
