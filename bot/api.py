import requests
from settings import SERVER_URL, FASTAPI_ACCESS_TOKEN


def retrieve_bot_answer(message):
    url = SERVER_URL + '/chat'
    headers = {"Content-Type": "application/json"}
    data = {"token": FASTAPI_ACCESS_TOKEN, "prompt": message}
    response = requests.post(url, headers=headers, json=data)
    return response


def generate_image(message, img_prompt):
    # count_image = input_validation(message.text)
    url = SERVER_URL + '/image'
    headers = {"Content-Type": "application/json"}
    data = {"token": FASTAPI_ACCESS_TOKEN, "prompt": img_prompt, "count_img": message.text}
    response = requests.post(url, headers=headers, json=data)
    return response


# def input_validation(count_img):
#     try:
#         count_img = int(count_img)
#         if count_img > 5:
#             return 5
#         return count_img
#     except ValueError:
#         return 1
