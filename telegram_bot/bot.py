import base64
import logging
from io import BytesIO

import requests
from PIL import Image
from aiogram import Bot, types, Dispatcher, executor

logging.basicConfig(level=logging.INFO)

bot = Bot(token='6460150280:AAFbRqfnRRY5Oy2CUrsmTH6wnhZRmGxr9wc')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет! Отправь мне фотографию, я отправлю ее на сервер и пришлю тебе ответ.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def on_photo(message: types.Message):
    user_id = message.from_user.id
    photo = message.photo[-1]

    photo_file = await bot.download_file_by_id(photo.file_id)
    photo_data = photo_file.read()

    server_response = send_photo_to_server(photo_data)

    res = "\n\n".join(server_response[0])
    await message.answer(f"Ответ от сервера: {res}")

    img_base64 = server_response[1]
    image_data = base64.b64decode(img_base64)
    if image_data:
        image = Image.open(BytesIO(image_data))

        await bot.send_photo(user_id, types.InputFile(BytesIO(image_data), filename='image.png'))


async def process_server_response(message: types.Message, photo_bytes, response_data):
    image, description = send_photo_to_server(photo_bytes)

    if image and description:
        # Ваш код для обработки изображения и отправки его пользователю
        await message.answer_photo(image)
        await message.answer(description)
    else:
        await message.answer("Произошла ошибка при получении изображения и/или описания с сервера.")


def send_photo_to_server(photo_data):
    server_url = 'http://127.0.0.1:5000/api/ml'
    files = {'file': ('photo.jpg', photo_data)}
    response = requests.post(server_url, files=files)

    if response.status_code == 200:
        response_data = response.json()
        description = response_data.get("description")
        image = response_data.get("image")

        if image:
            return description, image
        else:
            return "Изображение отсутствует в ответе сервера", ""
    else:
        return "Произошла ошибка на сервере", ""


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
