import requests
from settings import OPENAI_ACCESS_TOKEN, OPENAI_COMPLETIONS_URL, OPENAI_GPT_MODEL, OPENAI_IMAGE_URL, OPENAI_TRANSLATE_URL


def send_request(prompt, model=OPENAI_GPT_MODEL, max_tokens=60):
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(OPENAI_COMPLETIONS_URL, headers=query_headers(), json=data)
    print(response.json())
    return response.json()['choices'][0]['message']['content']


def get_image(prompt, count_img):
    data = {"prompt": prompt, "n": count_img, "size": "512x512"}
    response = requests.post(OPENAI_IMAGE_URL, headers=query_headers(), json=data)
    print(response.json())
    img_urls = response.json()['data']
    return img_urls


def translate(prompt):
    edited_prompt = f"Translate this into 1. English:\n\n{prompt}\n\n1."
    data = {"prompt": edited_prompt,
            "model": "text-davinci-003",
            "temperature": 0.3,
            "max_tokens": 100,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
            }
    response = requests.post(OPENAI_TRANSLATE_URL, headers=query_headers(), json=data)
    return response.json()


def query_headers():
    return {
        "Authorization": "Bearer " + OPENAI_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
