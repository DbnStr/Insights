import asyncio
import datetime
import io
import json
import logging
import os
import sys
from time import sleep

import pandas as pd
import pyrogram
import requests
import uvloop
from aiogram.types import BufferedInputFile

sys.path.append(os.path.abspath('../'))

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

sys.path.append(os.path.abspath('../'))

from summarize_utils import get_questions_answers_pairs
from report_generator import generate_report, create_excel_with_wrapped_text
import Constants
from Keyboards import *

import summarize_utils
import transcribe_utils
import proxy_gpt

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6884733501:AAEeffzK8uGFrdBiluIgC3ZFlAmUqAgMFuo"

class States(StatesGroup):
    START = State()
    # Вопросы по резюме продукта
    WAITING_FILE_FOR_SUMMARY = State()
    # Ждём файл для транскрибации
    WAITING_TRANSCRIPTION_FILE = State()
    # Состояния во время генерации отчетов
    WAITING_TEMPLATE_NAME = State()
    WAITING_FILE_FOR_REPORT = State()


router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state(States.START)
    await message.reply(START_MESSAGE, reply_markup=start_menu_keyboard)



@dp.message(F.text == Constants.SUMMARY_REQUEST)
async def process_summary_req(message: types.Message, state: FSMContext):
    await state.set_state(States.WAITING_FILE_FOR_SUMMARY)
    await message.reply(SUMMARY_FILE_REQUEST,
                        reply_markup=start_menu_keyboard)


@dp.message(F.text == Constants.TRANSCRIPTION_REQUEST)
async def process_summary_req(message: types.Message, state: FSMContext):
    await state.set_state(States.WAITING_TRANSCRIPTION_FILE)
    await message.reply(TRANSCRIPTION_FILE_REQUEST,
                        reply_markup=start_menu_keyboard)


@dp.message(F.text == Constants.REPORT_REQUEST)
async def process_report_req(message: types.Message, state: FSMContext):
    await state.set_state(States.WAITING_TEMPLATE_NAME)
    await message.reply(REPORT_TEMPLATE_NAME_REQUEST,
                        reply_markup=template_choose_keyboard)


@dp.message(States.WAITING_TEMPLATE_NAME)
async def process_summary_req(message: types.Message, state: FSMContext):
    if not message.text in TEMPLATES:
        await message.reply(NO_SUCH_TEMPLATE_ERROR,
                            reply_markup=start_menu_keyboard)
        return
    
    data = {'template_type' : template_mapping(message.text)}
    print(data)

    await state.update_data(data=data)
    await state.set_state(States.WAITING_FILE_FOR_REPORT)
    await message.reply(REPORT_FILE_REQUEST,
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
            file_name = message.document.file_name
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

    await message.reply(SUCCESS_LOAD_FILE)
    text = text.replace('\r', '')

    # Получаем пары вопрос-ответ из текста
    questions_answers = get_questions_answers_pairs(text)

    # Формируем путь к файлу результата
    user_id = message.from_user.id
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f'{SUMMARY_RESULTS_DIR_NAME}/суммаризация_{user_id}_{current_time}.xlsx'
    
    # Создаем Excel-файл с результатами
    summarize_utils.create_excel_with_wrapped_text(file_path, questions_answers)

    # Отправляем файл пользователю
    with open(file_path, "rb") as f:
        content = f.read()
    
    file = BufferedInputFile(
        content,
        filename=f"суммаризация_{current_time}.xlsx"
    )
    
    await state.clear()
    await bot.send_document(message.from_user.id, file, reply_markup=start_menu_keyboard)


@router.message(States.WAITING_TRANSCRIPTION_FILE)
async def process_transcription_file(message: types.Message, state: FSMContext):
    if message.voice == None and not (message.audio != None and message.audio.mime_type == MP3_FORMAT):
        await state.clear()
        await message.reply(FILE_FORMAT_ERROR,
                            reply_markup=start_menu_keyboard)
        return

    #Голосовое сообшение
    if message.voice != None:
        file_id = message.voice.file_id
        file_name = f'{message.from_user.username}_{datetime.datetime.now()}.mp3'
        await download_file(file_id, file_name)
    #MP3
    if message.audio != None and message.audio.mime_type == MP3_FORMAT:
        file_id = message.audio.file_id
        file_name = message.audio.file_name

    try:
        start_time = datetime.datetime.now()
        uvloop.install()
        await download_file(file_id, file_name)
        print(f"Время загрузки файла: {datetime.datetime.now() - start_time}")
    except Exception as e:
        print(f'Ошибка во время загрузки: {e}')
        await message.reply(FILE_PROCESS_ERROR,
                            reply_markup=start_menu_keyboard)
        return

    remote_file_name = transcribe_utils.send_media_to_recognition('downloads/{}'.format(file_name))
    print("Имя файла с транскрибацией на удаленном сервере : {}".format(remote_file_name))

    while True:
        status, text_with_diarization, text_without_diarization = transcribe_utils.get_recognition_result(remote_file_name)
        if status == 'not ready':
            sleep(10)
        else:
            text = transcribe_utils.improve_transcription(text_with_diarization, text_without_diarization)
            break

    file = BufferedInputFile(bytes(text.encode('utf-8')),
                             filename="Расшифровка.txt")
    await state.clear()
    await bot.send_document(message.from_user.id, file, reply_markup=start_menu_keyboard)


@router.message(States.WAITING_FILE_FOR_REPORT)
async def process_file_for_report(message: types.Message, state: FSMContext):
    if message.document != None and message.document.mime_type != TXT_FORMAT:
        await message.reply(FILE_FORMAT_ERROR,
                            reply_markup=start_menu_keyboard)
        return
    if message.document == None:
        text = message.text
    else:
        text = ''
        if message.document.mime_type == TXT_FORMAT:
            file_path = message.document.file_name
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

    await message.reply(SUCCESS_LOAD_FILE)

    text = text.replace('\r', '')

    data = await state.get_data()
    template_type = data['template_type']

    report_data = generate_report(template_type, text)
    user_id = message.from_user.id
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f'{Constants.REPORTS_DIR_NAME}/отчет_{user_id}_{current_time}.xlsx'
    create_excel_with_wrapped_text(file_path, report_data)

    content = open(file_path, "rb").read()
    file = BufferedInputFile(content,
                             filename="Отчет.xlsx")
    await state.clear()
    await bot.send_document(message.from_user.id, file, reply_markup=start_menu_keyboard)


async def download_file(file_id, local_file_name):
    async with pyrogram.Client("custDevAIClient", api_id=API_ID, api_hash=API_HASH) as app:
        await app.download_media(file_id, file_name=local_file_name)


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


def template_mapping(template_text):
    if template_text == WORK_MEETING_TEMPLATE_TEXT:
        return WORK_MEETING_TEMPLATE_NAME
    elif template_text == PRODUCT_PRESENTATION_TEMPLATE_TEXT:
        return PRODUCT_PRESENTATION_TEMPLATE_NAME
    elif template_text == TECHNICAL_ASSIGNMENT_TEMPLATE_TEXT:
        return TECHNICAL_ASSIGNMENT_TEMPLATE_NAME
    elif template_text == INTERVIEW_TEMPLATE_TEXT:
        return INTERVIEW_TEMPLATE_NAME
    
    print('Неверное имя шаблона')
    return ''


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
