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
        model="gpt-4o-mini", messages=conversation_history
    )
    res_mes = chat_completion.choices[0].message.content
    # print('Запрос: {}'.format(message))
    # print('Ответ от бота: {}'.format(res_mes))
    print('Запрос выполнен успешно!\nОбщее число потра'
          'ченных токенов: {}'.format(chat_completion.usage.total_tokens))
    return res_mes

# def gen_image():

#     # Открываем изображение и конвертируем его в формат RGBA
#     image = Image.open("example.png").convert("RGBA")
#     image_bytes = io.BytesIO()
#     image.save(image_bytes, format='PNG')
#     image_bytes.seek(0)
    
#     client = OpenAI(
#         api_key="sk-KIBQoCywhraAVHcCbjor91Cif9mJRojT",
#         base_url="https://api.proxyapi.ru/openai/v1",
#     )
#     response = client.images.edit(
#         image=image_bytes,
#         prompt="На картинке должна быть надпись \"Покупай скорее\". Также должны быть надписи \"Скидка\", \"Успей\"",
#         n=2,
#         size="1024x1024"
#     )
    
#     # Сохраняем изображение, которое пришло в ответе
#     for idx, image in enumerate(response.data):
#         image_url = image.url
#         image_response = requests.get(image_url)
#         print(response.data)
#         if image_response.status_code == 200:
#             file_name = f"downloaded_image_{idx + 1}.png"
#             with open(file_name, "wb") as f:
#                 f.write(image_response.content)
#                 print(f"Изображение успешно сохранено как {file_name}.")
#         else:
#             print("Ошибка при загрузке изображения.")