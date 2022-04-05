from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.const import SPIN_TEXT, SPIN_TEXT_5, SPIN_TEXT_10


def get_spin_keyboard():
    keyboard = [
        [KeyboardButton(text=SPIN_TEXT), KeyboardButton(text=SPIN_TEXT_5), KeyboardButton(text=SPIN_TEXT_10)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
