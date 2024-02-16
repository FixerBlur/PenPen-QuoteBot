# utils/notify_admins.py
import logging
import datetime

admins = []  # your telegram id


async def on_startup_notify(dp):
    for admin in admins:
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            text = f'📅Date: {current_time} \nBot started✅'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(dp):
    for admin in admins:
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            text = f'📅Date: {current_time} \nBot off😮‍💨'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
