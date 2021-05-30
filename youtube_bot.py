from __future__ import unicode_literals
import os
import sh
from glob import glob
import telebot
import youtube_dl
import urllib
import shutil
from telebot import types
bot = telebot.TeleBot('1890084498:AAFO2D4mSZJ9zHWBTz50h8emZMQ98HliQ4c') 
path = '/home/guru/Рабочий стол/python_bot/videos'
url1 = ' '
os.chdir('/home/guru/Рабочий стол/python_bot/videos/')
def downloadYouTube(videourl):

    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videourl])

def remove_video():
    sh.rm(sh.glob('/home/guru/Рабочий стол/python_bot/videos/*'))
@bot.message_handler(commands = ['start','help'])
def send_welcome(message):
    bot.reply_to(message,f'Здарова, я бот, который с радостью поможет тебе скачать видео с YouTube!Для того чтобы скачать видео, просто напиши мне "/download"')
    print("Приветствие отправлено!")
@bot.message_handler(commands = ['download'])
def get_text_messages(message):
    bot.send_message(message.chat.id,'Введите ссылку на видео и введите команду "/continue":')
    print("Запрос на ссылку отправлен!")
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        url2 = message.text
        print("URL получен")
        print(url2)
        downloadYouTube(url2)
        print("Видео скачано!")
@bot.message_handler(commands = ['continue'])
def continue_one(message):
    keyboard = types.InlineKeyboardMarkup()
    key_download = types.InlineKeyboardButton(text = 'Отправить видео💿', callback_data = 'skachat')
    keyboard.add(key_download)
    key_donate = types.InlineKeyboardButton(text = 'Помочь автору💰', callback_data = 'zadonatit') 
    keyboard.add(key_donate)
    bot.send_message(message.from_user.id, text='Выбери действие, которое ты хочешь выполнить:', reply_markup=keyboard)
    print("Запрос на выбор дейтсвия отправлен!")
@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    if call.data == "skachat":
        bot.send_message(call.message.chat.id, 'Начинаю отправлять видео, ожидайте...')
        try:
            filename = glob('*.mp4')[0]
            video = open(filename,'rb')
        except IndexError:
            bot.send_message(call.message.chat.id, 'Ой, ошибочка вышла!Введите команду "/download" и отправьте ссылку снова.')
            print("Ой, ошибочка вышла!(1)")
        try:
            bot.send_video(call.message.chat.id,video)
            print("Видео отправлено!")
            remove_video()
        except UnboundLocalError:
            #bot.send_message(call.message.chat.id, 'Ой, ошибочка вышла!Введите команду "/download" и отправьте ссылку снова.')
            print("Ой, ошибочка вышла!(2)")
    if call.data == "zadonatit":
        bot.send_message(call.message.chat.id, 'Хотите помочь автору купить чашечку кофе? Если да, то держите реквизиты:\nТинькофф -> 4377 7237 4664 6011')
        print("Риквизиты отправлены!")
#@bot.message_handler(content_types=['text'])
#def get_message_text(message):
 #   url = message.text 
 #   if url == 'привет':
#        print("fuf")
    #downloadYouTube(url,path)
    #video = open(* + '.mp4','rb')
    #bot.send_video(message.chat.id,video)
bot.polling()