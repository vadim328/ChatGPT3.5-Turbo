from telebot import apihelper, util, TeleBot
tb = TeleBot("test")


def test_start_message():
    apihelper.CUSTOM_REQUEST_SENDER = start_custom_sender
    res = tb.send_message(123, "Test")
    assert res.json == {'message_id': 1,
                        'date': 1,
                        'chat': {'id': 1, 'type': 'private'},
                        'text': 'Привет'}


def start_custom_sender(method, url, **kwargs):
    print("custom_sender. method: {}, url: {}, params: {}".format(method, url, kwargs.get("params")))
    result = util.CustomRequestResponse(
        '{"ok":true,"result":{"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}, "text": "Привет"}}')
    return result
