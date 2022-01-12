import os
import time
import logging
import cv2

from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from api.static_text import ABOUT, START, STICKER1
# from api.model_yolo import start_model
from api.model import BashmakModel

# Включаем логирование
logging.basicConfig(
    filename='log.log', 
    level=logging.INFO
)

# Загрузка токена через env
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f'{user_id} запустил бота в {time.asctime()}')
    await message.reply(START % user_name)


@dp.message_handler(commands=['about'])
async def process_help_command(message: types.Message):
    await message.reply(ABOUT)


# Главная функция
@dp.message_handler(content_types=['photo'])
async def handle_photo_for_prediction(message):
    chat_id = message.chat.id

    # media_group_id is None means single photo at message
    if message.media_group_id is None:
        user_id = message.from_user.id
        message_id = message.message_id

        # Отправка стикера во время предсказания
        await bot.send_video(chat_id, video=open('/home/jabulani/Final_Project/data/video.mp4', 'rb'))

        # Define input photo local path
        input_photo_name = '/home/jabulani/Final_Project/data/images/input/sneaker_%s_%s.jpg' % (user_id, message_id)

        await message.photo[-1].download(input_photo_name) # extract photo for further procceses

        ouput_photo_name = '/home/jabulani/Final_Project/data/images/output/photo_%s_%s.jpg' % (user_id, message_id)

        model = BashmakModel(input_photo_name)
        model.get_yolo_prediction()
        
        
        await bot.send_photo(chat_id, photo=open('/home/jabulani/Final_Project/predictions.jpg', 'rb'), caption='Ура, кроссовки найдены! Предсказываю модель кроссовок...')
        
        
        
        model.yolo_image_processing(ouput_photo_name)

        await bot.send_video(chat_id, video=open('/home/jabulani/Final_Project/data/video.mp4', 'rb'))

        output_text = model.get_resnet_prediction(ouput_photo_name)

        img1, img2, img3, img4 = output_text
        first = KeyboardButton(text=img1)
        second = KeyboardButton(text=img2)
        thrird = KeyboardButton(text=img3)
        fourth = KeyboardButton(text=img4)

        inline_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(first, second, thrird, fourth)

        await bot.send_photo(chat_id, photo=open(input_photo_name, 'rb'), caption='Вуаля!', reply_markup=inline_kb)
    else:
        await message.reply("Пожалуйста, пришли одну фотографию, а не вот столько!")


if __name__ == '__main__':
    executor.start_polling(dp)
