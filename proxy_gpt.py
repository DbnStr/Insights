import time

from openai import OpenAI

def send_request(messages):
    time.sleep(2)
    client = OpenAI(
        api_key="sk-KIBQoCywhraAVHcCbjor91Cif9mJRojT",
        base_url="https://api.proxyapi.ru/openai/v1",
    )

    conversation_history = []
    for m in messages:
        conversation_history.append({"role" : "user", "content" : m})

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=conversation_history
    )
    res_mes = chat_completion.choices[0].message.content
    # print('Запрос: {}'.format(message))
    print('Ответ от бота: {}'.format(res_mes))
    print('Запрос выполнен успешно!\nОбщее число потра'
          'ченных токенов: {}'.format(chat_completion.usage.total_tokens))
    return res_mes