from aiogram import Dispatcher
from database_handler import DatabaseHandler
from image_handler import ImageHandler
from utils.notify_admins import on_startup_notify


# Sends a message to the bot about the start
async def on_startup(dp: Dispatcher):
    db_handler = DatabaseHandler()
    await db_handler.create_table()

    image_handler = ImageHandler(dp.bot)
    dp.bot.image_handler = image_handler
    await on_startup_notify(dp)


# Sends a message to the bot about the off
async def on_shutdown(dp: Dispatcher):
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
