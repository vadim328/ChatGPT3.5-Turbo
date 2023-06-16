from fastapi import FastAPI, Body
from typing import Dict, Any
from openai_api import send_request, get_image, translate


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/bot")
async def bot(data: Dict[str, Any]):
    print(data)
    resp = send_request(data['messages'])
    return {"message": resp}


@app.get("/hello")
async def hello():
    return {"message": 'Hello!!!!'}


@app.post("/image")
async def image(data: Dict[str, Any]):
    translated_result = translate(data["message"])
    response = get_image(translated_result['choices'][0]['text'])
    return {"image_url": response}
