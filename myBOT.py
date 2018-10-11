import telebot
import random
from telebot.types import Message
from telebot import apihelper
import requests
import os
from PIL import Image
from zipfile import ZipFile


def get_all_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


RECORD = False

TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

apihelper.proxy = {'xxxxxxxxxxxxxxxxxxxxxxxxxxx'}

PATH_TO_FILE = 'F:\Загрузки\\'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(regexp='начинаем')
def start_recording(message):
    global RECORD
    RECORD = True
    bot.send_message(message.chat.id, 'Начинаю запись. Присылай мне по очереди стикеры, которые хочешь получить в архиве')


@bot.message_handler(regexp='закончили')
def stop_recording(message):
    global RECORD
    RECORD = False
    bot.send_message(message.chat.id, 'Заканчиваю запись. Сейчас получишь свой архив...')
    directory = 'F:\Загрузки\stickers'
    file_paths = get_all_file_paths(directory)
    with ZipFile(directory + '\my_stickers.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file)
        for file in file_paths:
            os.remove(file)
    bot.send_document(message.chat.id, open(directory + '\my_stickers.zip', 'rb') )
    os.remove(directory + '\my_stickers.zip')

@bot.message_handler(content_types=['sticker'])
def recording_stickers(message):
    global RECORD
    file_info = bot.get_file(message.sticker.file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
    with open(PATH_TO_FILE + file_info.file_path, 'wb') as f:
        f.write(file.content)
    if RECORD:
        bot.send_message(message.chat.id, 'Получил')
        im = Image.open(PATH_TO_FILE + file_info.file_path).convert("RGB")
        im.save(PATH_TO_FILE + (file_info.file_path)[:-5]+'.png', "png")
        os.remove(PATH_TO_FILE + file_info.file_path)
    else:
        bot.send_photo(message.chat.id, photo=open(PATH_TO_FILE + file_info.file_path, 'rb') , caption=message.sticker.emoji)
        os.remove(PATH_TO_FILE + file_info.file_path)

@bot.message_handler(regexp='подтвер')
def agree_with_me(message):
    bot.send_message(message.chat.id, 'Подтверждаю')

@bot.message_handler(content_types=['text'])
def upper(message: Message):
    k = random.randint(0,1)
    if k:
        bot.send_message(message.chat.id, 'Угу')


bot.polling()
