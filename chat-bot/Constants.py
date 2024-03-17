#Стартовое меню бота
START_MESSAGE = "Привет!\nЯ бот для проведения CustDev или по-простому опросу потребителей! Я умею:\n" \
                "- расшифровывать текстовые, аудио и видео интервью.\n" \
                "- делать краткую выжимку результатов интервью."
BACK_TO_MAIN_MENU = 'Вы вернулись на главный экран!'
TRANSCRIPTION_REQUEST = 'Переведи аудио/видео в текст'
SUMMARY_REQUEST = 'Сделай краткое резюме'
BACK_TO_START_MENU = 'Вернуться на главный экран'
YOU_ARE_IN_START_MENU = 'Вы на главном экране'
SUMMARY_FILE_REQUEST = 'Отправьте текст для резюме. Поддерживаемые форматы:\n' \
                       '- txt'
TRANSCRIPTION_FILE_REQUEST = 'Отправьте видео/аудио для перевода в текст. Поддерживаемые форматы:\n' \
                             '- mp3' \
                             '- голосовое сообщение'

#Общие ошибки
UNKNOWN_COMMAND_ERROR = 'Неизвестная команда'

#Сообщения при суммаризации
SUCCESS_LOAD_FILE = "Файл успешно загружен и принят в обработку. Ожидайте результат"

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

#Конфигурационные данные
API_ID = 28020262
API_HASH = 'cb5c33b77f266ad18ef29d7fc4f10a2a'

#Конфигурационные данные о сервере транскрибации
TRANSCRIPTION_SERVER_IP_ADDRESS = '34.41.250.251'
TRANSCRIPTION_SERVER_PORT = '3389'
TRANSCRIPTION_SERVER_URL = "0.0.0.0:3389"