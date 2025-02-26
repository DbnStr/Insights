from flask import Flask, jsonify, request
import report_generator
import summarize_utils
import datetime
import os
import uuid
import base64

app = Flask(__name__)

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
    print(text)
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

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
