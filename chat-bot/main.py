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
import Constants
from Keyboards import *

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6884733501:AAEeffzK8uGFrdBiluIgC3ZFlAmUqAgMFuo"

class States(StatesGroup):
    START = State()
    # Вопросы по резюме продукта
    WAITING_FILE_FOR_SUMMARY = State()
    # Ждём файл для транскрибации
    WAITING_TRANSCRIPTION_FILE = State()


router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state(States.START)
    await message.reply(START_MESSAGE)


@dp.message(States.START)
async def send_mes(message: types.Message, state: FSMContext):
    await message.reply("На данный момент бот приостановлен по причине отсутствия средств на серверные мощности :(")

# @dp.message(F.text == Constants.SUMMARY_REQUEST)
# async def process_summary_req(message: types.Message, state: FSMContext):
#     await state.set_state(States.WAITING_FILE_FOR_SUMMARY)
#     await message.reply(SUMMARY_FILE_REQUEST,
#                         reply_markup=start_menu_keyboard)
#
#
# @dp.message(F.text == Constants.TRANSCRIPTION_REQUEST)
# async def process_summary_req(message: types.Message, state: FSMContext):
#     await state.set_state(States.WAITING_TRANSCRIPTION_FILE)
#     await message.reply(TRANSCRIPTION_FILE_REQUEST,
#                         reply_markup=start_menu_keyboard)
#
#
# @router.message(States.WAITING_FILE_FOR_SUMMARY)
# async def process_file_for_summary(message: types.Message, state: FSMContext):
#     if message.document != None and message.document.mime_type != TXT_FORMAT:
#         await message.reply(FILE_FORMAT_ERROR,
#                             reply_markup=start_menu_keyboard)
#         return
#     if message.document == None:
#         text = message.text
#     else:
#         text = ''
#         if message.document.mime_type == TXT_FORMAT:
#             file_name = message.document.file_name
#             try:
#                 text = await get_text_from_txt_file(message.document.file_id)
#             except Exception as e:
#                 print(e)
#                 await message.reply(FILE_DATA_ERROR,
#                                     reply_markup=start_menu_keyboard)
#                 return
#
#     if text == '':
#         await message.reply(FILE_DATA_ERROR,
#                             reply_markup=start_menu_keyboard)
#         return
#
#     await message.reply(SUCCESS_LOAD_FILE)
#
#     text = text.replace('\r', '')
#
#     questions_answers = get_questions_answers_pairs(text)
#
#     df = pd.DataFrame({
#         'Вопрос': [i[0] for i in questions_answers],
#         'Ответ': [i[1] for i in questions_answers],
#         'Оценка ответа': [''] * len(questions_answers)})
#     df.to_excel('texts-for-summary/Суммаризация_{}.xlsx'.format(file_name), index=False)
#
#     content = open('texts-for-summary/Суммаризация_{}.xlsx'.format(file_name), "rb").read()
#     file = BufferedInputFile(content,
#                              filename="Суммаризация_{}.xlsx".format(file_name))
#     await state.clear()
#     await bot.send_document(message.from_user.id, file, reply_markup=start_menu_keyboard)
#
#
# @router.message(States.WAITING_TRANSCRIPTION_FILE)
# async def process_transcription_file(message: types.Message, state: FSMContext):
#     if message.voice == None and not (message.audio != None and message.audio.mime_type == MP3_FORMAT):
#         await state.clear()
#         await message.reply(FILE_FORMAT_ERROR,
#                             reply_markup=start_menu_keyboard)
#         return
#
#     #Голосовое сообшение
#     if message.voice != None:
#         file_id = message.voice.file_id
#         file_name = f'{message.from_user.username}_{datetime.datetime.now()}.mp3'
#         await download_file(file_id, file_name)
#     #MP3
#     if message.audio != None and message.audio.mime_type == MP3_FORMAT:
#         file_id = message.audio.file_id
#         file_name = message.audio.file_name
#
#     try:
#         start_time = datetime.datetime.now()
#         uvloop.install()
#         await download_file(file_id, file_name)
#         print(f"Время загрузки файла: {datetime.datetime.now() - start_time}")
#     except Exception as e:
#         print(f'Ошибка во время загрузки: {e}')
#         await message.reply(FILE_PROCESS_ERROR,
#                             reply_markup=start_menu_keyboard)
#         return
#
#     remote_file_name = send_media_to_recognition('downloads/{}'.format(file_name))
#     print("Имя файла с транскрибацией на удаленном сервере : {}".format(remote_file_name))
#
#     while True:
#         res = get_recognition_result(remote_file_name)
#         if res['status'] == 'not ready':
#             sleep(5)
#         else:
#             text = res['text']
#             break
#
#     file = BufferedInputFile(bytes(text.encode('utf-8')),
#                              filename="Расшифровка.txt")
#     await state.clear()
#     await bot.send_document(message.from_user.id, file, reply_markup=start_menu_keyboard)
#
#
# async def download_file(file_id, local_file_name):
#     async with pyrogram.Client("custDevAIClient", api_id=API_ID, api_hash=API_HASH) as app:
#         await app.download_media(file_id, file_name=local_file_name)
#
#
# def save_file(path, text):
#     file = open(path, "w+")
#     file.write(text)
#     file.close()
#
#
# def send_media_to_recognition(file_path):
#     print(f'Sending file to recognition. File path : {file_path}')
#     headers = {
#         "accept": "application/json"
#     }
#     params = {
#         "separate_vocal": "no",
#         "format": "audio",
#         "model_name": "whisper",
#         "count_speakers": "2"
#     }
#     files = {'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')}
#     url = f'http://{TRANSCRIPTION_SERVER_IP_ADDRESS}:{TRANSCRIPTION_SERVER_PORT}/file/upload-file'
#     print(url)
#
#     res = requests.post(url=url, params=params, files=files, headers=headers)
#
#     return json.loads(res.text)['request']['path']
#
#
# def get_recognition_result(file_name):
#     headers = {
#         "accept": "application/json"
#     }
#     params = {
#         "path": file_name,
#         "format": "txt"
#     }
#     url = f'http://{TRANSCRIPTION_SERVER_IP_ADDRESS}:{TRANSCRIPTION_SERVER_PORT}/file/download'
#
#     res = requests.get(url=url, params=params, headers=headers)
#
#     print("recognition result for {}:\n{}".format(file_name, res.text))
#
#     return json.loads(res.text)
#
#
# async def get_text_from_txt_file(file_id):
#     file_in_io = io.BytesIO()
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     await bot.download_file(file_path, file_in_io)
#     return file_in_io.read().decode('utf-8')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
