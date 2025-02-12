from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from Constants import *

def construct_keyboard(buttons_texts, buttons_in_line=3):
    builder = ReplyKeyboardBuilder()
    for c in buttons_texts:
        builder.add(types.KeyboardButton(text=c))
    builder.adjust(buttons_in_line)
    keyboard = builder.as_markup(resize_keyboard=True)

    return keyboard

start_menu_keyboard = construct_keyboard(
    [
        SUMMARY_REQUEST,
        TRANSCRIPTION_REQUEST,
        REPORT_REQUEST,
    ],
    1
)

template_choose_keyboard = construct_keyboard(
    TEMPLATES,
    2
)