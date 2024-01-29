import logging
import os
import redis as redislib
from dataclasses import dataclass
from typing import NoReturn, Optional
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler

from aiotdlib import Client
from dotenv import load_dotenv

load_dotenv()

USER_CONN_DATA_DB_HOST = os.getenv('USER_CONN_DATA_DB_HOST')
USER_CONN_DATA_DB_PORT = int(os.getenv('USER_CONN_DATA_DB_PORT'))
redis = redislib.Redis(host=USER_CONN_DATA_DB_HOST, port=USER_CONN_DATA_DB_PORT, decode_responses=True)

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
BOT_TOKEN = os.getenv('BOT_TOKEN')


@dataclass
class BasicUserInfo:
    first_name: str
    last_name: str
    username: Optional[str]
    id: int

    def __str__(self) -> str:
        s = f"{self.first_name} {self.last_name}"
        if self.username is not None:
            s += f" (@{self.username})"

        return s


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=PHONE_NUMBER
    )
    async with client:
        me = await client.api.get_me()
        user_info = BasicUserInfo(me.first_name, me.last_name,
                                  me.usernames.active_usernames[0] if len(me.usernames.active_usernames) >= 1 else None,
                                  me.id)
        logging.info(f"Successfully logged in as {user_info}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome {user_info}")


def start_bot() -> NoReturn:
    application = Application.builder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_bot()