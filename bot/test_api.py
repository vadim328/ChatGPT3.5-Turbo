import responses
import requests


@responses.activate
def test_retrieve_bot_answer():
    responses.add(responses.POST, 'http://server:8080/chat',
                  json={'message': 'some answer'}, status=200)

    resp = requests.post('http://server:8080/chat')

    assert resp.json() == {"message": "some answer"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://server:8080/chat'
    assert responses.calls[0].response.text == '{"message": "some answer"}'
