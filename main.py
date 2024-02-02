import logging
import os
import redis.asyncio as redis
from typing import NoReturn
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler

from aiotdlib import Client as TdLibClient
from dotenv import load_dotenv

from bl.BasicUserInfo import BasicUserInfo
from services.user_conn_info_service import UserConnInfoService

load_dotenv()

# initialize user connection info service
USER_CONN_DATA_DB_HOST = os.getenv('USER_CONN_DATA_DB_HOST')
USER_CONN_DATA_DB_PORT = int(os.getenv('USER_CONN_DATA_DB_PORT'))
redis_client = redis.Redis(host=USER_CONN_DATA_DB_HOST, port=USER_CONN_DATA_DB_PORT, decode_responses=True)
user_conn_info_service = UserConnInfoService(redis_client)

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await user_conn_info_service.save_user_conn_info()
    # start mini app to ask user for its connection info
    user_conn_info = None # TODO
    client = TdLibClient(
        api_id=user_conn_info.api_id,
        api_hash=user_conn_info.api_hash,
        phone_number=user_conn_info.phone_number
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

    #TODO: await client.aclose() on error handler
    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_bot()