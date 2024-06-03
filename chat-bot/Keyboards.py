from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from Constants import *

#Клавиатура с изначальным меню выбора
start_menu = ReplyKeyboardBuilder()
start_menu.add(
    types.KeyboardButton(text=SUMMARY_REQUEST),
    types.KeyboardButton(text=TRANSCRIPTION_REQUEST),
    types.KeyboardButton(text=REPORT_REQUEST))
start_menu.adjust(1)
start_menu_keyboard = start_menu.as_markup(resize_keyboard=True)