from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(

    keyboard=[
        [
            KeyboardButton(text='/help'),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)
