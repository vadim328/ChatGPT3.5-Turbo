import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()

env = dotenv_values(".env")
DEBUG = os.getenv("DEBUG") == "1"
AMQP_URI = os.getenv("AMQP_URI")
UNIQUE_PREFIX = os.getenv("UNIQUE_PREFIX")
GPT_TOKEN = env['GPT_TOKEN']
GPT_URL = env['GPT_URL']
GPT_ORG = env['GPT_ORG']
