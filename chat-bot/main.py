import asyncio
import io
import logging
import os
import sys

sys.path.append(os.path.abspath('../'))

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

sys.path.append(os.path.abspath('../'))

from summarize_utils import get_questions_answers_pairs
import Constants
from Keyboards import *

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6884733501:AAEeffzK8uGFrdBiluIgC3ZFlAmUqAgMFuo"


class States(StatesGroup):
    START = State()
    # Вопросы по резюме продукта
    WAITING_FILE_FOR_SUMMARY = State()
    # Вопросы по продукту
    WAITING_PRODUCT_DESCRIPTION = State()
    WAITING_ADDITIONAL_QUESTIONS_REQ = State()
    WAITING_QUESTION_COUNT = State()
    # Вопросы по транскриптции
    WAITING_TRANSCRIPTION_FILE = State()


router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state(States.START)
    await message.reply(START_MESSAGE,
                        reply_markup=start_menu_keyboard)


@dp.message(F.text == Constants.SUMMARY_REQUEST)
async def process_summary_req(message: types.Message, state: FSMContext):
    await state.set_state(States.WAITING_FILE_FOR_SUMMARY)
    await message.reply(SUMMARY_FILE_REQUEST,
                        reply_markup=start_menu_keyboard)


@router.message(States.WAITING_FILE_FOR_SUMMARY)
async def process_file_for_summary(message: types.Message, state: FSMContext):
    if message.document != None and message.document.mime_type != TXT_FORMAT:
        await message.reply(FILE_FORMAT_ERROR,
                            reply_markup=start_menu_keyboard)
        return
    if message.document == None:
        text = message.text
    else:
        text = ''
        if message.document.mime_type == TXT_FORMAT:
            try:
                text = await get_text_from_txt_file(message.document.file_id)
            except Exception as e:
                print(e)
                await message.reply(FILE_DATA_ERROR,
                                    reply_markup=start_menu_keyboard)
                return

    if text == '':
        await message.reply(FILE_DATA_ERROR,
                            reply_markup=start_menu_keyboard)
        return

    text = text.replace('\r', '')
    summary = get_questions_answers_pairs(text)

    res = ''
    for i, qa in enumerate(summary):
        if i == len(summary) - 1:
            res = res + "<b>Вопрос {}</b>: {}\n<b>Ответ</b>: {}".format(i, qa[0], qa[1])
        else: res = res + "<b>Вопрос {}</b>: {}\n<b>Ответ</b>: {}\n\n".format(i, qa[0], qa[1])

    await state.clear()
    await message.reply(res, reply_markup=start_menu_keyboard, parse_mode=ParseMode.HTML)


def save_file(path, text):
    file = open(path, "w+")
    file.write(text)
    file.close()


async def get_text_from_txt_file(file_id):
    file_in_io = io.BytesIO()
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, file_in_io)
    return file_in_io.read().decode('utf-8')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
