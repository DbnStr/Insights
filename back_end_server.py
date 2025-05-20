from flask import Flask, jsonify, request
import report_generator
import summarize_utils
import datetime
import os
import uuid
import base64
import transcribe_utils
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

@app.route('/getReport', methods=['POST'])
def get_report():
    text = request.json.get('text', '')
    template_type = request.json.get('template_type', '')

    report_data = report_generator.generate_report(template_type, text)
    
    # Создаем уникальный идентификатор для файла
    unique_id = str(uuid.uuid4())
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Проверяем существование директории
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Формируем путь к файлу
    file_path = f'reports/отчет_{unique_id}_{current_time}.xlsx'
    
    # Создаем Excel файл
    report_generator.create_excel_with_wrapped_text(file_path, report_data)
    
    # Читаем файл и кодируем в base64
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
    
    return jsonify({
        'res': report_data,
        'excelFile': encoded_file
    })
    

@app.route('/getSummary', methods=['POST'])
def get_summary():    
    text = request.json.get('text', '')
    interviewer_id = request.json.get('interviewer_id', '1')
    
    # Получаем пары вопрос-ответ из текста
    questions_answers = summarize_utils.get_questions_answers_pairs(text, interviewer_id)
    
    # Создаем уникальный идентификатор для файла
    unique_id = str(uuid.uuid4())
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Проверяем существование директории
    if not os.path.exists('summary-results'):
        os.makedirs('summary-results')
    
    # Формируем путь к файлу
    file_path = f'summary-results/суммаризация_{unique_id}_{current_time}.xlsx'
    
    # Создаем Excel файл
    summarize_utils.create_excel_with_wrapped_text(file_path, questions_answers)
    
    # Читаем файл и кодируем в base64
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
    
    return jsonify({
        'excelFile': encoded_file
    })

@app.route('/transcribe', methods=['POST'])
def transcribe():    
    # Проверяем существование директории
    if not os.path.exists('transcribe-files'):
        os.makedirs('transcribe-files')
        
    # Декодируем base64 файл и сохраняем его
    file = request.files['file']
    file_path = f'transcribe-files/transcribe_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp3'
    file.save(file_path)

    remote_file_name = transcribe_utils.send_media_to_recognition(file_path)
    print("Имя файла с транскрибацией на удаленном сервере : {}".format(remote_file_name))

    while True:
        status, text_with_diarization, text_without_diarization = transcribe_utils.get_recognition_result(remote_file_name)
        if status == 'not ready':
            sleep(10)
        else:
            text = transcribe_utils.improve_transcription(text_with_diarization, text_without_diarization)
            break
    
    # Создаем временный текстовый файл
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f'transcribe-results/transcribe_{current_time}.txt'
    
    # Записываем текст в файл
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # Читаем файл и кодируем в base64
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
    
    return jsonify({
        'resFile': encoded_file
    })

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
