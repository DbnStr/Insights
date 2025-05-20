import Constants
import requests
import json
import proxy_gpt

def send_media_to_recognition(file_path):
    print(f'Sending file to recognition. File path : {file_path}')
    headers = {
        "accept": "application/json"
    }
    params = {
        "separate_vocal": "yes",
        "format": "audio",
        "model_name": "gigaam",
        "count_speakers": None
    }
    files = {'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')}
    url = f'http://{Constants.TRANSCRIPTION_SERVER_IP_ADDRESS}:{Constants.TRANSCRIPTION_SERVER_PORT}/file/upload-file'

    res = requests.post(url=url, params=params, files=files, headers=headers)

    print(f"Результат загрузки {res.json()}")
    remote_file_path = json.loads(res.text)['request']['path']

    return remote_file_path


def get_recognition_result(file_name):
    headers = {
        "accept": "application/json"
    }
    params = {
        "path": file_name,
        "format": "txt"
    }
    url = f'http://{Constants.TRANSCRIPTION_SERVER_IP_ADDRESS}:{Constants.TRANSCRIPTION_SERVER_PORT}/file/download'

    res = requests.get(url=url, params=params, headers=headers)
    print("recognition result for {}:\n{}".format(file_name, res.text))
    res_json = json.loads(res.text)

    return res_json.get('status'), res_json.get('text_with_diarization'), res_json.get('text_without_diarization')


def improve_transcription(text_with_diarization, text_without_diarization):
    messages = [
        f"Текст с разбиением по спикерам:\n{text_with_diarization}",
        f"Текст без разбиения по спикерам:\n{text_without_diarization}",
        "Я прислал тебе 2 файла. Один с хорошим разбиением по спикерам, второй с правильным текстом. Скорректируй текст, разбитый по спикерам, используя правильный текст. Не придумывай от себя, в ответе пришли только скорректированный текст с разбиением по спикерам"
    ]
    text = proxy_gpt.send_request(messages=messages)

    return text