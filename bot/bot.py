# -*- coding: utf-8 -*-

import os
import textwrap

from dotenv import load_dotenv
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from database_handler import DatabaseHandler
from image_handler import ImageHandler
import logging
from keyboards.Keyboards import kb_menu
import help

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.ERROR)


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    await message.answer(f"Hi👋 {message.from_user.full_name}! \n"
                         f"Learn about all the bot features: /help", reply_markup=kb_menu)


@dp.message_handler(commands='help')
async def command_help(message: types.Message):
    await message.answer(f'{help.help_text}')


@dp.message_handler(commands=['c'])
async def process_command(message: types.Message):
    try:
        logging.info("Received command: %s", message.text)

        if not message.reply_to_message or not message.reply_to_message.from_user:
            logging.warning("Invalid command: No reply_to_message or from_user is None.")
            return

        # Add this line for debugging
        logging.info("Processing /c command")

        if message.reply_to_message.text:
            user_text = message.reply_to_message.text
            textwrap.fill(user_text, width=25)
        else:
            logging.warning("No text in the replied message.")
            return

        original_user_id = message.reply_to_message.from_user.id
        original_user = message.reply_to_message.from_user  # User who wrote the original message
        db_handler = DatabaseHandler()
        image_handler = ImageHandler(bot)

        logging.info("Calling update_command_usage")
        await db_handler.update_command_usage(original_user_id, original_user.username)

        logging.info("Calling create_image")
        await image_handler.create_image(original_user, message, original_user_id)

        logging.info("Command processed successfully.")
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


if __name__ == '__main__':
    from loader import on_startup, on_shutdown

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
