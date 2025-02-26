# Стартовое меню бота
START_MESSAGE = "Привет!\nЯ бот для составления транскрибации файлов и составления отчетов по тексту!"
BACK_TO_MAIN_MENU = 'Вы вернулись на главный экран!'
YOU_ARE_IN_START_MENU = 'Вы на главном экране'

# Запросы
TRANSCRIPTION_REQUEST = 'Переведи аудио/видео в текст'
SUMMARY_REQUEST = 'Сделай краткое резюме'
REPORT_REQUEST = 'Создать отчет'
BACK_TO_START_MENU = 'Вернуться на главный экран'
SUMMARY_FILE_REQUEST = 'Отправьте текст для резюме. Поддерживаемые форматы:\n- txt\n- обычное сообщение'
TRANSCRIPTION_FILE_REQUEST = 'Отправьте видео/аудио для перевода в текст. Поддерживаемые форматы:\n- mp3\n- голосовое сообщение'
REPORT_FILE_REQUEST = 'Отправьте текст для генерации отчета. Поддерживаемые форматы:\n- txt\n- обычное сообщение'
REPORT_TEMPLATE_NAME_REQUEST = 'Выберите нужный шаблон'

# Типы шаблонов
WORK_MEETING_TEMPLATE_TEXT = 'Рабочее совещание'
WORK_MEETING_TEMPLATE_NAME = 'meeting'
PRODUCT_PRESENTATION_TEMPLATE_TEXT = 'Презентация продукта/проекта'
PRODUCT_PRESENTATION_TEMPLATE_NAME = 'presentation'
TECHNICAL_ASSIGNMENT_TEMPLATE_TEXT = 'Обсуждение ТЗ с заказчиком'
TECHNICAL_ASSIGNMENT_TEMPLATE_NAME = 'technical_assignment'
INTERVIEW_TEMPLATE_TEXT = 'Интервью'
INTERVIEW_TEMPLATE_NAME = 'interview'

TEMPLATES = [WORK_MEETING_TEMPLATE_TEXT, PRODUCT_PRESENTATION_TEMPLATE_TEXT, TECHNICAL_ASSIGNMENT_TEMPLATE_TEXT, INTERVIEW_TEMPLATE_TEXT]

# Ошибки при формировании отчетов
NO_SUCH_TEMPLATE_ERROR = 'Такого шаблона у нас пока нет( Выберите из предложенных'

# Общие ошибки
UNKNOWN_COMMAND_ERROR = 'Неизвестная команда'

# Сообщения при суммаризации
SUCCESS_LOAD_FILE = "Файл успешно загружен и принят в обработку. Ожидайте результат"

# Ошибки при загрузке файла
FILE_DATA_ERROR = 'Файл содержит некорректную информацию'
FILE_FORMAT_ERROR = "Формат файла не поддерживается! Повторите ввод"
FILE_SIZE_ERROR = 'Размер файла не должен превышать 20 мб'
FILE_PROCESS_ERROR = 'Ошибка во время обработки файла, повторите попытку'
FILE_NO_SOUND = 'В файле нету звука. Попробуйте другой файл'

# Типы файла в телеге
TXT_FORMAT = 'text/plain'
DOC_FORMAT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
MP4_FORMAT = 'video/mp4'
M4A_FORMAT = 'audio/x-m4a'
MP3_FORMAT = 'audio/mpeg'

# Конфигурационные данные
API_ID = 28020262
API_HASH = 'cb5c33b77f266ad18ef29d7fc4f10a2a'

# Конфигурационные данные о сервере транскрибации
TRANSCRIPTION_SERVER_IP_ADDRESS = '176.99.131.129'
TRANSCRIPTION_SERVER_PORT = '3389'

# Названия директория
REPORTS_DIR_NAME = 'reports'
SUMMARY_RESULTS_DIR_NAME = 'summary-results'
TEXTS_FOR_SUMMARY_DIR_NAME = ''