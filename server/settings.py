import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

env = dotenv_values(".env")
DEBUG = os.getenv("DEBUG") == "1"

OPENAI_ACCESS_TOKEN = env['OPENAI_ACCESS_TOKEN']
OPENAI_COMPLETIONS_URL = env['OPENAI_COMPLETIONS_URL']
OPENAI_GPT_MODEL = env['OPENAI_GPT_MODEL']
OPENAI_IMAGE_URL = env['OPENAI_IMAGE_URL']
OPENAI_TRANSLATE_URL = env['OPENAI_TRANSLATE_URL']
FASTAPI_ACCESS_TOKEN = env['FASTAPI_ACCESS_TOKEN']
