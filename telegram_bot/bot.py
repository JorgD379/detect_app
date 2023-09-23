import logging
import requests
from aiogram import Bot, types,Dispatcher, executor


logging.basicConfig(level=logging.INFO)

bot = Bot(token='6620645581:AAGhk251_IBznW5qzHiASZ515ISecteWmxU')
dp = Dispatcher(bot)
label_dict = {
    "1": "СПО250.14.190",
    "2": "СК50.02.01.411",  # Добавьте другие расшифровки
    "3": "СК50.01.01.404",
    "4": "СК30.01.01.03.403",
    "5": "СК30.01.01.02.402",
    "6": "СК20.01.01.02.402",
    # Добавьте расшифровки для других цифр, если необходимо
}
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет! Отправь мне фотографию, и я отправлю ее на сервер и пришлю тебе ответ.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def on_photo(message: types.Message):
    photo = message.photo[-1]

    photo_file = await bot.download_file_by_id(photo.file_id)
    photo_data = photo_file.read()

    server_response = send_photo_to_server(photo_data)

    await message.answer(f"Ответ от сервера: {server_response}")

def send_photo_to_server(photo_data):
    server_url = 'http://127.0.0.1:5000/api/ml'
    files = {'file': ('photo.jpg', photo_data)}
    response = requests.post(server_url, files=files)
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
        labels = response_data.get("labels", [])
        decoded_labels = [label_dict.get(label, label) for label in labels]
        confidence = response_data.get("score", [])[0]
        response_string = f"Ответ: {', '.join(decoded_labels)}, Уверенность: {confidence}"
        return response_string
    else:
        return "Произошла ошибка на сервере"

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
