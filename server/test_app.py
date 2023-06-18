from fastapi.testclient import TestClient
from app import app
import responses
import requests

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@responses.activate
def test_retrieve_bot_answer():
    responses.add(responses.POST, 'https://api.openai.com/v1/images/generations',
                  json={"image_url": "http://openai.com/image_url"}, status=200)

    resp = requests.post('https://api.openai.com/v1/images/generations')

    assert resp.json() == {"image_url": "http://openai.com/image_url"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'https://api.openai.com/v1/images/generations'
    assert responses.calls[0].response.text == '{"image_url": "http://openai.com/image_url"}'
