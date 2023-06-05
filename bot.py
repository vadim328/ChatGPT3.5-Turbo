import logging
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

from dotenv import dotenv_values

env = dotenv_values(".env")

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


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = send_request(update.message.text)
        await update.message.reply_text(response)
    except:
        await update.message.reply_text(update.message.text)


def send_request(message):
    url = env['GPT_URL']
    headers = {"Authorization": "Bearer " + env["GPT_TOKEN"]}
    data = {"message": message}
    response = requests.post(url, headers=headers, data=data)
    return response.json()["generated_text"]


def main() -> None:
    application = Application.builder().token(env["BOT_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()

