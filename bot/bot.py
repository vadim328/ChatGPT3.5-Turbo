import logging
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
# from telegram.helpers import escape_markdown
# from telegram.utils.helpers import escape_markdown
import requests
# import openai
import re
import pdb

from dotenv import dotenv_values

env = dotenv_values(".env")
# openai.api_key = env['GPT_URL']
# openai.organization = env['GPT_ORG']
# openai.api_key.set(env['GPT_URL'])
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Задай свой вопрос:",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Помощь")


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     try:
#         response = send_request(update.message.text)
#         escaped_text = escape_chars(response)
#         await update.message.reply_text(escaped_text, parse_mode=ParseMode.MARKDOWN_V2)
#     except:
#         await update.message.reply_text('Что то пошло не так, повторите вопрос.')
#

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = send_api(update.message.text)
        escaped_text = escape_chars(response['message'])
        await update.message.reply_text(escaped_text, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as error:
        print(error.args)
        await update.message.reply_text('Что то пошло не так, повторите вопрос.')


def send_api(message):
    url = env['SERVER_URL'] + '/bot'
    headers = {"Content-Type": "application/json"}
    # data = {"messages": message}
    response = requests.post(url, headers=headers, json=message)
    print(response.json())
    return response.json()


def escape_chars(text):
    # escape_chars = r"\_*[]()~`>#+-=|{}.!"
    pattern = r"\_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(pattern)}])", r"\\\1", text)


# def send_request(prompt, model="gpt-3.5-turbo", max_tokens=60):
#     url = env['GPT_URL']
#     headers = {"Authorization": "Bearer " + env["GPT_TOKEN"], "Content-Type": "application/json"}
#     data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
#     response = requests.post(url, headers=headers, json=data)
#     print(response.json())
#     return response.json()['choices'][0]['message']['content']


def main() -> None:
    # application = Application.builder().token(env["BOT_TOKEN"]).read_timeout(30).write_timeout(30).build()
    application = Application.builder().token(env["BOT_TOKEN"]).read_timeout(60).get_updates_read_timeout(60).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("api", api_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()
