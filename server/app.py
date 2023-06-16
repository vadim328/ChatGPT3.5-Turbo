from fastapi import FastAPI, Body
from openai_api import send_request, get_image, translate
from typing import Dict, Any

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/bot")
async def bot(data: Dict[str, Any]):
    print(data)
    resp = send_request(data['message'])
    return {"message": resp}


@app.get("/hello")
async def hello():
    return {"message": 'Hello!!!!'}


@app.post("/image")
async def image(data: Dict[str, Any]):
    res = translate(data["text"])
    resp = get_image(res['choices'][0]['text'])
    return {"image_url": resp}


@app.post("/translate")
async def translate_text(data: Dict[str, Any]):
    res = translate(data["text"])
    return res
