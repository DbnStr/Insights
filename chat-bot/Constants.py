#Стартовое меню бота
START_MESSAGE = "Привет!\nЯ бот для проведения CustDev или по-простому опросу потребителей! Я умею:\n" \
                "- расшифровывать текстовые, аудио и видео интервью.\n" \
                "- делать краткую выжимку результатов интервью."
BACK_TO_MAIN_MENU = 'Вы вернулись на главный экран!'
TRANSCRIPTION_REQUEST = 'Переведи аудио/видео в текст'
SUMMARY_REQUEST = 'Сделай краткое резюме'
BACK_TO_START_MENU = 'Вернуться на главный экран'
YOU_ARE_IN_START_MENU = 'Вы на главном экране'
SUMMARY_FILE_REQUEST = 'Отправьте текст для резюме в сообщении или в форматах txt'

#Общие ошибки
UNKNOWN_COMMAND_ERROR = 'Неизвестная команда'

#Ошибки при загрузки файла
FILE_DATA_ERROR = 'Файл содержит некорректную информацию'
FILE_FORMAT_ERROR = "Формат файла не поддерживается! Повторите ввод"
FILE_SIZE_ERROR = 'Размер файла не должен превышать 20 мб'
FILE_PROCESS_ERROR = 'Ошибка во время обработки файла, повторите попытку'
FILE_NO_SOUND = 'В файле нету звука. Попробуйте другой файл'

#Типы файла в телеге
TXT_FORMAT = 'text/plain'
DOC_FORMAT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
MP4_FORMAT = 'video/mp4'
M4A_FORMAT = 'audio/x-m4a'
MP3_FORMAT = 'audio/mpeg'