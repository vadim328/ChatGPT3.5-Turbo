import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

env = dotenv_values(".env")

DEBUG = os.getenv("DEBUG") == "1"

BOT_TOKEN = env['BOT_TOKEN']
FASTAPI_ACCESS_TOKEN = env['FASTAPI_ACCESS_TOKEN']
SERVER_URL = env['SERVER_URL']
