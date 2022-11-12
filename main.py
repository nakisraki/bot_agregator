# -*- encoding: utf-8 -*-
##DURING TASK add last block, news_block remake , user statistic send , link-videos agregator,check all parsers
import logging
import requests
import os
import codecs
import re
import urllib.request as ur
from config import API
from aiogram import Bot, Dispatcher, types, executor
import asyncio
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from datetime import datetime
from  shutil import copyfile as copy
import time
import random
import json
import io
from sql import SQLighter
import parsers.base as p_base
import urllib.parse
import bet_and_fin as baf

   

API_TOKEN = API


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

##global admin
admin_file = ''
##global users activity
id_active_status = {}
id_active_movie = {}
id_busket = {}
id_links_status = {}
id_active_web = {}

vote_cb = CallbackData('vote', 'action','user','data')


# инициализируем соединение с БД
db = SQLighter('Bot_Agr.db')

commodities , ipos = baf.Finance.base_price(),baf.Finance.upcoming_ipo()


anecdots = p_base.humor.anecdot()
fun_story = p_base.humor.fun_stories()
mems = p_base.humor.mems()
sms = p_base.humor.sms_message()
afforisms = p_base.humor.afforisms()

geo_tests = p_base.tests.geo_test()
art_test = p_base.tests.art_test()

short_stories = p_base.adult.short_stories()
long_stories = p_base.adult.long_stories()
ad_comixes = p_base.adult.comixes()
x_test = p_base.adult.test()
web_cams = p_base.video_agr.web_cam()

accidents,world,public,army = p_base.video_agr.accidents(),p_base.video_agr.world(),p_base.video_agr.public(),p_base.video_agr.army()
science,autos,j_video_short = p_base.video_agr.science(),p_base.video_agr.autos(),p_base.video_agr.fun()
movies = p_base.video_agr.movies()



#async def for_anecdots(wait_for):
 #       global anecdots
  #      while True:
   #             await asyncio.sleep(wait_for)
    #            anecdots = p_base.humor.anecdot()
    #            fun_story = p_base.humor.fun_stories()
    #            sms = p_base.humor.sms_message()
    #            j_video_short = p_base.humor.short_videos()
    #            tests = {"geo_test":p_base.tests.geo_test()}
    #            id_busket = {}


# Команда активации подписки
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		time = datetime.now().strftime('%Y-%m-%d-%H')
		db.add_subscriber(message.from_user.id,True,"","",time,"","","","","","","","","","","")
		await message.answer("Bot: Вы успешно подписаны для доступа к основным разделам")
		
	else:
                pass
		
	



                    ######BUTTONS AND KEYBOARD########

def main_menu():
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
        keyboard_markup.add(types.KeyboardButton("\U0001F306 Новости"),types.KeyboardButton("\U0001F92A Юмор"),types.KeyboardButton("\U0001F3AC Видео Дня"),types.KeyboardButton("\U0001F393 Тесты"),types.KeyboardButton("\U0001F4B5 Деньги"),types.KeyboardButton("\U0001F49E Взрослым"))
        return keyboard_markup


def inline_buttons(head,content,user):
        if head == "q_geo_start":
             keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
             for i in content[3]:
                if i==content[1]:  
                        keyboard_markup.add(types.InlineKeyboardButton(i,callback_data=vote_cb.new(action='g_True',data='0',user=user)))
                else:
                        keyboard_markup.add(types.InlineKeyboardButton(i,callback_data=vote_cb.new(action='g_False',data='0',user=user)))                           
             return keyboard_markup
        elif head == "q_art_start":
             keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
             for i in content[2]:
                if i==content[0]:  
                        keyboard_markup.add(types.InlineKeyboardButton(i,callback_data=vote_cb.new(action='art_True',data='0',user=user)))
                else:
                        keyboard_markup.add(types.InlineKeyboardButton(i,callback_data=vote_cb.new(action='art_False',data='0',user=user)))                           
             return keyboard_markup
        elif head == "adult_test_start":
             keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
             for i in content[1]:
                     if i == content[0]:
                             keyboard_markup.add(types.InlineKeyboardButton(i,callback_data=vote_cb.new(action='x_adault_True',data='0',user=user)))
                     else:
                             keyboard_markup.add(types.InlineKeyboardButton(i,callback_data=vote_cb.new(action='x_adault_False',data='0',user=user)))
             return keyboard_markup

        elif head == "admin":
             keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.InlineKeyboardButton("В архив",callback_data=vote_cb.new(action='add_archive',data=content,user=user)),types.InlineKeyboardButton("Удалить",callback_data=vote_cb.new(action='remove_file',data=content,user=user)))
             return keyboard_markup 

        elif head == "adult_test_start+":
                keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
                return  keyboard_markup.add(types.InlineKeyboardButton("Смотреть галлерею",callback_data=vote_cb.new(action='x_adault_True+',data='0',user=user)))
                

        else:
             pass

def key_buttons(x):
        if x == "News":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=1)
             keyboard_markup.add(types.KeyboardButton("\U0001F64B Еще новoстей"),types.KeyboardButton("\U0001F645 Хватит Новостей"))
             return keyboard_markup
        if x == "Jokes":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F929 Short Видео"),types.KeyboardButton("\U0001F602 Фото и Мемы"),types.KeyboardButton("\U0001F642 Анекдоты"),types.KeyboardButton("\U0001F92D Истории"),
                                 types.KeyboardButton("\U0001F3AD СМС Переписка"),types.KeyboardButton("\U0001F913 Aфоризмы"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Quiz":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F5FA GEO"),types.KeyboardButton("\U0001F3A8 ART"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Art_Next":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F3A8 ART - Cледующий вопрос"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Geo_Next":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F5FA GEO - Cледующий вопрос"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Money":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=1)
             keyboard_markup.add(types.KeyboardButton("\U0001F3C0 Ставки на спорт"),types.KeyboardButton("\U0001F4B9 Финансовые рынки"),types.KeyboardButton("\U0001F64B Подписаться"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup                    
        if x == "Adult":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F9D6 ВебКам"),types.KeyboardButton("\U0001F494 Истории"),types.KeyboardButton("\U0001F48B Рассказы с фото"),types.KeyboardButton("\U0001F46F Угадай актрису"),types.KeyboardButton("\U0001F9DA Комиксы"),types.KeyboardButton("\U0001F4D6 Закладка"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "adult_comix":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F9DC Следующяя страница"),types.KeyboardButton("\U0001F9DA Другой Комикс"),types.KeyboardButton("\U0001F4D5 Добавить Комикс в закладку и выйти"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup   
        if x == "X_Test_Next":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)                                    
             keyboard_markup.add(types.KeyboardButton("\U0001F46F Следующий вопрос"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "adult_long":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F9CF Следующяя страница"),types.KeyboardButton("\U0001F926 Другой Рассказ"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Afforisms":
             tag = afforisms[2]
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             for i in range(0,len(tag),2):
                     keyboard_markup.add(types.KeyboardButton(tag[i]),types.KeyboardButton(tag[i+1]))
             keyboard_markup.add(types.KeyboardButton("\U0001F519 Главное Меню"))        
             return keyboard_markup
        if x == "Videos":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
             keyboard_markup.add(types.KeyboardButton("\U0001F691 Проишествия"),types.KeyboardButton("\U0001F30F В Мире"),types.KeyboardButton("\U0001F482 Общество"),types.KeyboardButton("\U0001F698 Авто"),types.KeyboardButton("\U0001F469 Наука"),types.KeyboardButton("\U0001F6F0 Армия"),types.KeyboardButton("\U0001F3A5 Фильмы"),types.KeyboardButton("\U0001F64B Подписаться"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Fin":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
             keyboard_markup.add(types.KeyboardButton("\U0001F984 IPO"),types.KeyboardButton("\U0001F301 Акции"),types.KeyboardButton("\U0001F4B8 Валюты и Крипто"),types.KeyboardButton("\U0001F6E2 Сырье и Металлы"),types.KeyboardButton("\U0001F5FF События"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        if x == "Bet":
             keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
             keyboard_markup.add(types.KeyboardButton("\U0001F3CB Фавориты"),types.KeyboardButton("\U0001F938 Аутсайдеры"),types.KeyboardButton("\U0001F914 Изменения"),types.KeyboardButton("\U0001F4AC Cправка"),types.KeyboardButton("\U0001F519 Главное Меню"))
             return keyboard_markup
        else:
             pass        

def button_url(channel,link,head):
        keyboard_markup = types.InlineKeyboardMarkup()
        keyboard_markup.add(types.InlineKeyboardButton(channel + head,url=link))
        return keyboard_markup


                 #######TEXT COMMANDS###########
@dp.message_handler()
async def text_in_handler(message: types.Message):
        global id_busket,id_active_status,admin_file,id_links_status,id_active_movie
        user_id = str(message.from_user.id)
        if user_id not in id_busket:
                id_busket[user_id] = {}          
                 #### NEWS ####
        if message.text == "\U0001F306 Новости":
                 news_head = p_base.news.Ru_news()[:10]
                 await message.answer("Главные новости")
                 await message.answer(commodities)
                 for i in news_head:
                         await message.answer(i[0],reply_markup=button_url(i[1],i[2]," \U0001F446"))
                         await asyncio.sleep(3)
                 await message.answer("******",reply_markup=key_buttons("News"))       
        elif message.text == "\U0001F64B Еще новoстей":
                 news_add = p_base.news.Ru_news()[10:]
                 await message.answer("Новости дня")
                 for i in news_add:
                         await message.answer(i[0],reply_markup=button_url(i[1],i[2]," \U0001F446"))
                         await asyncio.sleep(3)
                 await message.answer("******",reply_markup=main_menu())
                 #### HUMOR
        elif message.text == "\U0001F92A Юмор":
                 await message.answer("\U0001F447",reply_markup=key_buttons("Jokes"))


                              ###anekdots###
        elif message.text == "\U0001F642 Анекдоты":
                 if "anecdots" not in id_busket[user_id]:
                        id_busket[user_id]["anecdots"] = [[-1],[-1]]
                 for i in range(2):
                         a = -1
                         if len(id_busket[user_id]["anecdots"][0])-1 != len(anecdots[0]) and len(anecdots[0])>0: 
                              while a in id_busket[user_id]["anecdots"][0]:
                                 a = random.randrange(len(anecdots[0]))
                              text = str(anecdots[0][a])
                              await message.answer(text)
                              id_busket[user_id]["anecdots"][0].append(a)
                         else:
                              if i==0:
                                await message.answer("Bot: Новых пока нет достаю случайные из архива")
                              while a in id_busket[user_id]["anecdots"][1]:
                                 a = random.randrange(len(anecdots[1]))
                              text = anecdots[1][a]
                              await message.answer(text)
                              id_busket[user_id]["anecdots"][1].append(a)

                            ###fun_story###
        elif message.text == "\U0001F92D Истории":
                if "fun_story" not in id_busket[user_id]:
                        id_busket[user_id]["fun_story"] = [[],[]]
                a = None
                if len(id_busket[user_id]["fun_story"][0]) != len(fun_story[0]):
                     while a in id_busket[user_id]["fun_story"][0] or a==None:     
                        a = random.randrange(len(fun_story[0]))
                     await message.answer(fun_story[0][a])
                     id_busket[user_id]["fun_story"][0].append(a)
                elif len(id_busket[user_id]["fun_story"][1]) != len(fun_story[1]): 
                     await message.answer("Bot: Новых пока нет достаю случайную из архива")   
                     while a in id_busket[user_id]["fun_story"][1] or a==None :
                        a = random.randrange(len(fun_story[1]))
                     await message.answer(fun_story[1][a])
                     id_busket[user_id]["fun_story"][1].append(a)
                else:
                     id_busket[user_id]["fun_story"] = [[],[]]


                                  ###mems###
        elif message.text == "\U0001F602 Фото и Мемы":
                watched_mems = db.mems_watched(user_id)
                path = "media/udaf/"
                a = None        
                new = [i for i in mems[0] if i not in watched_mems.split(",")]
                if len(new)>0:
                     a = random.choice(new)   
                     photo = open(path+a, 'rb')
                     await bot.send_photo(message.from_user.id,photo)
                     photo.close()
                     
                else:
                     await message.answer("Bot: Новых пока нет достаю случайную из архива")
                     while a in watched_mems.split(",") or a==None:
                        a = random.choice(mems[1])
                     photo = open(path+a, 'rb')
                     await bot.send_photo(message.from_user.id,photo)
                     photo.close()
                     
                mems_new = watched_mems + a + ","     
                if len(mems_new.split(","))-1 == len(mems[1]):
                        mems_new = ""
                db.update_mems(user_id,mems_new)        
                    

                               ###sms_chats###
        elif message.text == "\U0001F3AD СМС Переписка":
                path = "media/sms_fun/"
                watched_sms = db.sms_watched(user_id)
                a = None
                while a in watched_sms.split(",") or a==None:
                        a = random.choice(sms[1])
                photo = open(path+a, 'rb')
                await bot.send_photo(message.from_user.id,photo)
                photo.close()
                sms_new = watched_sms + a + ","
                if len(sms_new.split(","))-1 == len(sms[1]):
                        sms_new = ""
                db.update_sms(user_id,sms_new)        
                

                                ###short_video block###
        elif message.text == "\U0001F929 Short Видео":
                watched_video = db.video_watched(user_id)
                path = "media/temporary/Развлечения/"
                archive_path = "media/fun_short_videos/"
                a = None
                new = [i for i in j_video_short[0] if i not in watched_video.split(",")]
                print(new)
                if len(new)>0:
                     a = random.choice(new)
                     print(a)
                     video = open(path+a, 'rb')
                     await bot.send_video(message.from_user.id,video)
                     video.close()
                     if user_id == "920120916":
                             admin_file = path+a
                             await message.answer("admin panel",reply_markup=inline_buttons("admin","Развлечения",user_id))
                             
                else: 
                     await message.answer("Bot: Новых пока нет достаю случайную из архива")   
                     while a in watched_video.split(",") or a==None:
                        a = random.choice(j_video_short[1])
                     video = open(archive_path+a, 'rb')
                     await bot.send_video(message.from_user.id,video)
                     video.close()
                     if user_id == "920120916":
                             admin_file = archive_path+a
                             await message.answer("admin panel",reply_markup=inline_buttons("admin","Развлечения",user_id))
                watched_new = watched_video + a + ","
                if len(watched_new.split(","))-19 > len(j_video_short[1]):
                        watched_new = ",".join(j_video_short[0])
                db.update_watched(user_id,watched_new)               
                                
                                ###afforism block###
        elif message.text == "\U0001F913 Aфоризмы":
                await message.answer("Выбери тему на которую мне подобрать цитату или аффоризм",reply_markup=key_buttons("Afforisms"))
                
        elif message.text in afforisms[2]:
                topic = " ".join(message.text.split(" ")[1:])
                theme = ''
                if topic not in id_busket[user_id]:
                       id_busket[user_id][topic] = []
                if topic == "Цитаты дня":
                        theme = afforisms[0]
                else:
                        theme = afforisms[1][topic]
                       
                if len(id_busket[user_id][topic])==len(theme):
                        id_busket[user_id][topic] = []
                        if topic == "Цитаты дня":
                                await message.answer("Bot: На сегодня новых нет")
                                
                msg = None
                while msg == None or msg in id_busket[user_id][topic]:
                        msg = random.choice(theme)
                                
                id_busket[user_id][topic].append(msg)        
                await message.answer(msg)
                
                       ###QUIZZ and GAMES###
        elif message.text == "\U0001F393 Тесты":
                await message.answer("Выбери тему",reply_markup=key_buttons("Quiz"))
                
                           ###geo###
        elif message.text == "\U0001F5FA GEO":
                watched_geo = db.geo_watched(user_id)
                path = "media/geo_images/"       
                a =  None
                while str(a) in watched_geo.split(",") or a==None: 
                       a = random.randrange(len(geo_tests[1]))
                geo_new = watched_geo + str(a) + ","      
                if len(geo_new.split(","))-1 == len(geo_tests[1]):
                        geo_new = ''        
                db.update_geo(user_id,geo_new)   
                test = geo_tests[1][a]
                title ,test = test[0],test[1]
                await message.answer(title)     
                photo = open(path+test['0'][2], 'rb')
                await bot.send_photo(message.from_user.id,photo)
                await message.answer(test['0'][0])
                photo.close()
                id_active_status[user_id] = [test,0,0,False]
                await message.answer("Выбери один из вариантов",reply_markup=inline_buttons("q_geo_start",test['0'],user_id))
                await message.answer("*****",reply_markup=key_buttons("Geo_Next"))      
        elif message.text == "\U0001F5FA GEO - Cледующий вопрос":
                path = "media/geo_images/"
                if id_active_status[user_id][3] == True:
                        index = id_active_status[user_id][1]
                        question = id_active_status[user_id][0][str(index)]
                        photo = open(path+question[2], 'rb')
                        await bot.send_photo(message.from_user.id,photo)
                        await message.answer(question[0])
                        photo.close()
                        await message.answer("Выбери один из вариантов",reply_markup=inline_buttons("q_geo_start",question,user_id))
                        await message.answer("*****",reply_markup=key_buttons("Geo_Next"))
                        id_active_status[user_id][3] = False
                else:
                        if id_active_status[user_id][3] == 'Stop':
                                await message.answer("Вопросы закончились - твой результат: " + str(id_active_status[user_id][2]) + " из " + str(id_active_status[user_id][1]))
                                await message.answer("Bot: Хочешь знать больше про страны и континеты ",reply_markup=button_url("Geo.koltyrin","https://geo.koltyrin.ru/"," \U0001F446"))
                                await message.answer("Тебе сюда",reply_markup=main_menu())
                        else:
                                await message.answer("Bot: Пожалуйста ответь  сначала на вопрос")

                                ###art###
        elif message.text == "\U0001F3A8 ART":
                names = [i for i in art_test]
                test = [random.choice(names) for j in range(11)]
                test = [[i,[i,random.choice(art_test[i])]] for i in test]
                for i in range(len(test)):
                        question = []
                        while len(set(question))!=4:
                                add = random.choices(names, k=3)
                                add.append(test[i][0])
                                question = add
                        random.shuffle(question)
                        test[i].append(question)       
                await message.answer("BOT: Угадай кто автор картины?")
                path = "media/art_pictures/" + test[0][1][1]
                photo = open(path, 'rb')
                await bot.send_photo(message.from_user.id,photo)
                photo.close()
                id_active_status[user_id] = [test,0,0,False]
                await message.answer("Выбери один из вариантов",reply_markup=inline_buttons("q_art_start",test[0],user_id))
                await message.answer("*****",reply_markup=key_buttons("Art_Next"))

        elif message.text == "\U0001F3A8 ART - Cледующий вопрос":
                path = "media/art_pictures/"
                if id_active_status[user_id][3] == True:
                        await message.answer("BOT: Угадай кто автор картины?")
                        index = id_active_status[user_id][1]
                        question = id_active_status[user_id][0][index]
                        try:
                            photo = open(path+question[1][1], 'rb')
                            await bot.send_photo(message.from_user.id,photo)
                            photo.close()
                            await message.answer("Выбери один из вариантов",reply_markup=inline_buttons("q_art_start",question,user_id))
                            await message.answer("*****",reply_markup=key_buttons("Art_Next"))
                            id_active_status[user_id][3] = False
                        except:
                            print("error")
                            print(path+question[1][1])
                else:
                        if id_active_status[user_id][3] == 'Stop':
                                await message.answer("Вопросы закончились - твой результат: " + str(id_active_status[user_id][2]) + " из " + str(id_active_status[user_id][1]))
                                await message.answer("Bot: Хочешь узнать Больше про картины и выставки",reply_markup=button_url("Gallerix.ru","https://gallerix.ru/"," \U0001F446"))
                                await message.answer("Тебе сюда",reply_markup=main_menu())
                        else:
                                await message.answer("Bot: Пожалуйста ответь  сначала на вопрос")

                                ###ADULTS###
        elif message.text == "\U0001F49E Взрослым":
                await message.answer("\U0001F447",reply_markup=key_buttons("Adult"))


                                ###web_cam###
        elif message.text == "\U0001F9D6 ВебКам":
                path = "media/temporary/web/"
                if user_id not in id_active_web:
                        id_active_web[user_id] = 0
                name = [i for i in web_cams][id_active_web[user_id]]
                print(name)
                vid = web_cams[name]
                print(vid[1])
                await message.answer(name)
                photo = open(vid[0], 'rb')
                await bot.send_photo(message.from_user.id,photo,reply_markup=button_url(" ",vid[1],"Смотреть "))
                photo.close()
                if id_active_web[user_id]+1 == len(web_cams):
                        id_active_web[user_id] = 0
                else:
                        id_active_web[user_id]+=1
                
                

                                ###short_story###
        elif message.text == "\U0001F494 Истории":
                watched_x_short = db.x_short_watched(user_id)   
                a = None   
                while a in watched_x_short.split(",") or a==None:
                        a = str(random.randrange(len(short_stories[1])))
                x_short_new =  watched_x_short + a + ","
                if len(x_short_new.split(","))-1 == len(short_stories[1]):
                        x_short_new = ""
                db.update_x_short(user_id,x_short_new)        
                text = short_stories[1][a]
                while len(text)>0:
                        await message.answer(text[:2000])
                        text = text[2000:]      
                 

                                ###comixes###
        elif message.text == "\U0001F9DA Комиксы" or message.text == "\U0001F9DA Другой Комикс":
                path = "media/a_comixes/"
                await message.answer("\U0001F9DA",reply_markup=key_buttons("adult_comix"))
                watched_comixes = db.x_comixes_watched(user_id)   
                a = None
                while a in watched_comixes.split(",") or a==None:
                        a = str(random.randrange(len(short_stories[1])))
                comixes_new = watched_comixes + a + ","        
                if len(comixes_new.split(","))-1 == len(short_stories[1]):
                        comixes_new = ''      
                db.update_x_comixes(user_id,comixes_new)
                comix = ad_comixes[1][a]
                await message.answer(comix[0])
                photo = open(path+comix[1], 'rb')
                await bot.send_photo(message.from_user.id,photo)
                photo.close()
                id_active_status[user_id]=[comix[2],1]
        elif message.text == "\U0001F9DC Следующяя страница":
                path = "media/a_comixes/"
                content = id_active_status[user_id]
                try:    
                    photo = open(path+content[0][content[1]], 'rb')
                    await bot.send_photo(message.from_user.id,photo)
                    photo.close()
                    id_active_status[user_id][1] += 1
                except:
                    await message.answer("******",reply_markup=key_buttons("Adult"))

                               ###long_story###
        elif message.text == "\U0001F48B Рассказы с фото" or message.text == "\U0001F926 Другой Рассказ":
                path = "media/a_long_story/"
                await message.answer("\U0001F48B",reply_markup=key_buttons("adult_long"))
                watched_x_long = db.x_long_watched(user_id)     
                title = None
                while title in watched_x_long.split(",") or title==None:
                        title = random.choice([i for i in long_stories[1]])
                x_long_new = watched_x_long + title + ","  
                if len(x_long_new.split(","))-1 == len(long_stories[1]):
                        x_long_new = ""
                db.update_x_long(user_id,x_long_new)        
                await message.answer(title)
                story = long_stories[1][title]
                photo = open(path+story[0], 'rb')
                await bot.send_photo(message.from_user.id,photo)
                photo.close()
                content = [i for i in story[1] if len(i)>5]
                id_active_status[user_id]=[content,0]
        elif message.text == "\U0001F9CF Следующяя страница":
                path = "media/a_long_story/"
                content = id_active_status[user_id]
                try:
                    if content[0][content[1]].endswith("jpg") or content[0][content[1]].endswith("png"):
                            photo = open(path+content[0][content[1]], 'rb')
                            await bot.send_photo(message.from_user.id,photo)
                            photo.close()
                            id_active_status[user_id][1] += 1
                    else:
                            await message.answer(content[0][content[1]])
                            id_active_status[user_id][1] += 1
                            
                except:
                    await message.answer("******",reply_markup=key_buttons("Adult"))
                                ###x_test###
        elif message.text == "\U0001F46F Угадай актрису":
                names = []
                while len(set(names))!=10:
                        names = random.choices(x_test[0],k=10)
                test = []
                for i in names:
                        question = []
                        while len(set(question))!=4:
                                  question = random.choices(names,k=3)
                                  question.append(i)
                        random.shuffle(question)
                        test.append([i,question])
                await message.answer("BOT: Угадай кто это?")
                path = "media/xxx/" + test[0][0]
                try:
                    photo = open(path+".jpg", 'rb')
                except:
                    photo = open(path+".png", 'rb')    
                await bot.send_photo(message.from_user.id,photo)
                photo.close()
                id_active_status[user_id] = [test,0,0,False,None,0]
                await message.answer("******",reply_markup=key_buttons("X_Test_Next"))
                await message.answer("Выбери один из вариантов",reply_markup=inline_buttons("adult_test_start",test[0],user_id))

        elif message.text == "\U0001F46F Следующий вопрос":
                id_active_status[user_id][4]=None
                id_active_status[user_id][5]=0
                path = "media/xxx/"
                if id_active_status[user_id][3] == True:
                        
                        await message.answer("BOT: Угадай кто это?")
                        index = id_active_status[user_id][1]
                        question = id_active_status[user_id][0][index]
                        try:
                           photo = open(path+question[0]+".jpg", 'rb')
                        except:
                           photo = open(path+question[0]+".png", 'rb') 
                        await bot.send_photo(message.from_user.id,photo)
                        photo.close()
                        await message.answer("******",reply_markup=key_buttons("X_Test_Next"))
                        await message.answer("Выбери один из вариантов",reply_markup=inline_buttons("adult_test_start",question,user_id))
                        id_active_status[user_id][3] = False
                else:
                        if id_active_status[user_id][3] == 'Stop':
                                await message.answer("Вопросы закончились - твой результат: " + str(id_active_status[user_id][2]) + " из " + str(id_active_status[user_id][1]),reply_markup=main_menu())
                        else:
                                await message.answer("Bot: Пожалуйста ответь  сначала на вопрос")        
                
                                ###ДЕНЬГИ###
        elif message.text == "\U0001F4B5 Деньги":
                await message.answer("Bot: Здесь я рассчитаю для тебя точные шансы на текущиие спортивные события ,стоимость ценных бумаг валют и другие финансовые иснструменты выбери на чем бы ты хотел заработать  ",reply_markup=key_buttons("Money"))

                                ###ВИДЕО AGREGATOR###
        elif message.text == "\U0001F3AC Видео Дня":
                await message.answer("\U0001F3AC",reply_markup=key_buttons("Videos"))
        elif message.text == "\U0001F3A5 Фильмы":
                path = "media/temporary/movies/"
                if user_id not in id_active_movie:
                        id_active_movie[user_id] = 0
                movie = movies[id_active_movie[user_id]]        
                title = movie.replace(".mp4"," ").replace("+"," ").replace("#"," ")
                await message.answer(title)
                video = open(path+movie, 'rb')
                link = "https://zloekino.su/movie#search/movie/" +  title.split("Русский")[0] 
                await bot.send_video(message.from_user.id,video,reply_markup=button_url("Cмотреть",link,"-бесплатно"))
                video.close()
                print(id_active_movie[user_id])
                print(len(movies))
                if id_active_movie[user_id]+1 == len(movies):
                        id_active_movie[user_id] = 0
                else:
                        id_active_movie[user_id]+=1
                    
        elif message.text == "\U0001F691 Проишествия":
                path = "media/temporary/Происшествия/"
                watched_accidents = db.get_accidents(user_id)
                accidents_day = [i for i in accidents if i not in watched_accidents.split(",")]
                if len(accidents_day)>0:
                        a = random.choice(accidents_day)
                        if a.startswith("unname"):
                             title = "Без комментариев...."
                        else:        
                             title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                        await message.answer(title)
                        try:
                            video = open(path+a, 'rb')
                            await bot.send_video(message.from_user.id,video)
                            video.close()
                        except:
                            pass
        
                        new_watched = watched_accidents + a + ","
                        db.update_accidents(user_id,new_watched)
                else:
                        await message.answer("Bot:Видео проишествий дня пока нет если хочешь чтоб я искал видео специально для тебя - Нажми Подписаться")

        elif message.text == "\U0001F30F В Мире":
                path = "media/temporary/Мир/"
                watched_wp = db.get_world_public(user_id)
                world_day = [i for i in world if i not in watched_wp.split(",")]
                if len(world_day)>0:
                        a = random.choice(world_day)
                        if a.startswith("unname"):
                             title = "Без комментариев...."
                        else:        
                             title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                        await message.answer(title)
                        try:
                            video = open(path+a, 'rb')
                            await bot.send_video(message.from_user.id,video)
                            video.close()
                        except:
                            pass
                        if len(watched_wp.split(","))>250:
                                watched_wp = ",".join(watched_wp.split(",")[50:])
                        new_watched = watched_wp + a + ","
                        db.update_world_public(user_id,new_watched)
                else:
                        await message.answer("Bot:Видео день в мире пока нет если хочешь чтоб я искал видео специально для тебя - Нажми Подписаться")
        elif message.text == "\U0001F482 Общество":
                path = "media/temporary/Общество/"
                watched_wp = db.get_world_public(user_id)
                public_day = [i for i in public if i not in watched_wp.split(",")]
                if len(public_day)>0:
                        a = random.choice(public_day)
                        if a.startswith("unname"):
                             title = "Без комментариев...."
                        else:        
                             title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                        await message.answer(title)
                        try:
                            video = open(path+a, 'rb')
                            await bot.send_video(message.from_user.id,video)
                            video.close()
                        except:
                            pass
                        if len(watched_wp.split(","))>250:
                                watched_wp = ",".join(watched_wp.split(",")[50:])
                        new_watched = watched_wp + a + ","
                        db.update_world_public(user_id,new_watched)
                else:
                     await message.answer("Bot:Видео Общество за день пока нет если хочешь чтоб я искал видео специально для тебя - Нажми Подписаться")

        elif message.text == "\U0001F6F0 Армия":
                path = "media/temporary/Армия/"
                archive = "media/weapon/"
                watched_army = db.get_army(user_id)
                army_day = [i for i in army[0] if i not in watched_army.split(",")]
                if len(army_day)>0:
                        a = random.choice(army_day)
                        title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                        await message.answer(title)
                        try:
                            video = open(path+a, 'rb')
                            await bot.send_video(message.from_user.id,video)
                            video.close()
                        except:
                            pass
                        new_army = watched_army + a + ","
                        db.update_army(user_id,new_army)
                else:
                        watched_army = db.get_army(user_id)
                        army_archive = [i for i in army[1] if i not in watched_army.split(",")]
                        if len(army_archive)>0:
                                a = random.choice(army_archive)
                                title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                                await message.answer(title)
                                try:
                                    video = open(archive+a, 'rb')
                                    await bot.send_video(message.from_user.id,video)
                                    video.close()
                                except:
                                    pass
                                new_army = watched_army + a + ","
                                db.update_army(user_id,new_army)
                        else:
                                await message.answer("Bot:Извини новых видео Армия пока нет если хочешь чтоб я искал видео специально для тебя - Нажми Подписаться")
                                
        elif message.text == "\U0001F469 Наука":
                path = "media/temporary/Наука/"
                watched_science = db.get_science(user_id)
                sci_avl = [i for i in science[0] if i not in watched_science.split(",")]
                if len(sci_avl)>0:
                        a = random.choice(sci_avl)
                        title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                        await message.answer(title)
                        try:
                            video = open(path+a, 'rb')
                            await bot.send_video(message.from_user.id,video)
                            video.close()
                        except:
                            pass
                        new_sci = watched_science + a + ","
                        db.update_science(user_id,new_sci)
                else:
                        if user_id not in id_links_status:
                                id_links_status[user_id] = 0
                        start,end = id_links_status[user_id] , id_links_status[user_id] + 3
                        if end > len(science[1]):
                                end = len(science[1])
                        if end == len(science[1]):
                                id_links_status[user_id] = 0
                        else:
                                id_links_status[user_id] = end        
                        for i in science[1][start:end]:
                                try:
                                    new_path = "media/temporary/" + user_id + ".jpg"
                                    title = i.replace(".mp4","")
                                    path_img = "https://storage.yandexcloud.net/videos2808/" + title + ".jpg"
                                    path_video = "https://storage.yandexcloud.net/videos2808/" + title + ".mp4"
                                    photo = ur.urlopen(path_img)
                                    head = urllib.parse.unquote(title).replace("+"," ")
                                    await message.answer(head)
                                    await bot.send_photo(message.from_user.id,photo,reply_markup=button_url(" ",path_video,"Смотреть "))
                                    photo.close()
                                    await asyncio.sleep(3)
                                except:
                                    print(urllib.parse.unquote(title).replace("+"," "))
                                               
        elif message.text == "\U0001F698 Авто":
                path = "media/temporary/Авто/"
                watched_auto = db.get_auto(user_id)
                new_auto = [i for i in autos if i not in watched_auto.split(",")]
                if len(new_auto)>0:
                        a = random.choice(new_auto)
                        if a.startswith("unname"):
                             title = "Без комментариев...."
                        else:        
                             title = a.split(".mp4")[0].replace("mp4"," ").replace("mkv"," ").replace("avi"," ").replace("#"," ")
                        await message.answer(title)
                        try:
                            video = open(path+a, 'rb')
                            await bot.send_video(message.from_user.id,video)
                            video.close()
                        except:
                            pass
                        new_auto = watched_auto + a + ","
                        db.update_auto(user_id,new_auto)
                else:
                        await message.answer("Bot:Видео Авто за день пока нет я нашел для тебя ссылки:")                        
                        

                                  ##FINANCE#               
        elif message.text == "\U0001F4B9 Финансовые рынки":
                await message.answer("\U0001F3DB",reply_markup=key_buttons("Fin"))
        elif message.text == "\U0001F984 IPO":
                for i in ipos:
                        if i[1] != "":
                                await message.answer(i[0],reply_markup=button_url("Веб-Сайт",i[1]," \U0001F446"))
                
                        else:
                                await message.answer(i[0])
                        await message.answer("График на следующий месяц : " + i[2])
                await message.answer("*******",reply_markup=key_buttons("Fin"))

        elif message.text == "\U0001F4B8 Валюты и Крипто":
                crypto = baf.Finance.crypto()
                icon = open('media/btc.png','rb')
                await bot.send_photo(message.from_user.id,icon)
                await message.answer("BTC: " + crypto[0] + "\n" + "График на следующий месяц : ---" )
                icon.close()
                icon = open('media/eth.png','rb')
                await bot.send_photo(message.from_user.id,icon)
                await message.answer("ETH: "+crypto[1] + "\n" + "График на следующий месяц : ---" )
                icon.close()
                
                                ##BETTING##
        elif message.text == "\U0001F3C0 Ставки на спорт":
                await message.answer("\U0001F945",reply_markup=key_buttons("Bet"))
                
        elif message.text == "\U0001F4AC Cправка":
                text = "Bot:Фавориты и Аутсайдеры  - перерасчитанные моими алгоритмами коэффиценты на главные спортивные события"
                text2 = "Bot:Изменения - зафиксированные мной, большие изменения в линиях букмекерских контор"
                await message.answer(text)
                await message.answer(text2)

        elif message.text == "\U0001F914 Изменения":
                games = baf.Sport.sport_line_change()
                for i in games:
                        await message.answer(i)
                        await asyncio.sleep(3)
                await message.answer("*******",reply_markup=key_buttons("Bet"))
                
                                ###Закладки###
        elif message.text.startswith("\U0001F4D5 Добавить Комикс в закладку"):
                content = id_active_status[user_id]
                signets = (",".join(content[0])) + ":^" + str(content[1])
                db.update_signents(user_id,signets)
                await message.answer("Bot:Комикс добавлен в закладку",reply_markup=main_menu())

        elif message.text == "\U0001F4D6 Закладка":
                signets = db.get_signets(user_id)
                if len(signets)>2:
                        signets = signets.split(":^")
                        id_active_status[user_id] = [[i for i in signets[0].split(",")],int(signets[1])]
                        await message.answer("\U0001F9DA Закладка открыта.Нажми следующяя страница",reply_markup=key_buttons("adult_comix"))
                        signets = ""
                        db.update_signents(user_id,signets)

                else:
                        await message.answer("Bot: У тебя нет активной закладки")
        
        else:
                await message.answer("Bot: Выбирай",reply_markup=main_menu())
                

   
@dp.callback_query_handler(vote_cb.filter(action=['g_True', 'g_False']))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
        global id_active_status
        callback_data_action = callback_data['action']
        user_id = callback_data["user"]
        index = id_active_status[user_id][1]
        answer = id_active_status[user_id][0][str(index)][1]
        if callback_data_action == 'g_True':
                if str(index+1) in id_active_status[user_id][0]:
                        id_active_status[user_id][3] = True
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][2] += 1
                else:
                        id_active_status[user_id][1] += 1 
                        id_active_status[user_id][2] += 1
                        id_active_status[user_id][3] = "Stop"
                await bot.edit_message_text("Верно!!!",query.from_user.id,
                                query.message.message_id)

        if callback_data_action == 'g_False':
                if str(index+1) in id_active_status[user_id][0]:
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][3] = True
                else:
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][3] = "Stop"
                await bot.edit_message_text("Неверно - Правильный ответ " + answer,query.from_user.id,
                                query.message.message_id)
                
@dp.callback_query_handler(vote_cb.filter(action=['art_True', 'art_False']))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
        global id_active_status
        callback_data_action = callback_data['action']
        user_id = callback_data["user"]
        index = id_active_status[user_id][1]
        answer =  id_active_status[user_id][0][index][1][1].split("_")[1].replace(".jpg","")
        answer = re.sub(r"\d+", "", answer)
        if callback_data_action == 'art_True':
                if index+1 < len(id_active_status[user_id][0]):
                        id_active_status[user_id][3] = True
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][2] += 1
                else:
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][2] += 1
                        id_active_status[user_id][3] = "Stop"
                await bot.edit_message_text("Верно!!!",query.from_user.id,
                                query.message.message_id)

        if callback_data_action == 'art_False':
                if index+1 < len(id_active_status[user_id][0]):
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][3] = True
                else:
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][3] = "Stop"
                await bot.edit_message_text("Нет! Это " + answer,query.from_user.id,
                                query.message.message_id)

        

@dp.callback_query_handler(vote_cb.filter(action=['x_adault_True','x_adault_False','x_adault_True+']))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
        global id_active_status
        callback_data_action = callback_data['action']
        user_id = callback_data["user"]
        index = id_active_status[user_id][1]
        answer = id_active_status[user_id][0][index][0]
        if callback_data_action == 'x_adault_True':
                if index+1 < len(id_active_status[user_id][0]):
                        id_active_status[user_id][3] = True
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][2] += 1
                        if id_active_status[user_id][4] == None:
                                id_active_status[user_id][4] = db.person_gallery(answer)
                                
                                
                else:
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][2] += 1
                        id_active_status[user_id][3] = "Stop"
                await bot.edit_message_text("Верно!!!",query.from_user.id,
                                query.message.message_id,reply_markup=inline_buttons("adult_test_start+",answer,user_id))        

        if callback_data_action == 'x_adault_False':
                if index+1 < len(id_active_status[user_id][0]):
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][3] = True
                        id_active_status[user_id][4] = None
                        id_active_status[user_id][5] = 0
                else:
                        id_active_status[user_id][1] += 1
                        id_active_status[user_id][3] = "Stop"
                await bot.edit_message_text("Нет! Это " + answer,query.from_user.id,
                                query.message.message_id)        
        if  callback_data_action == 'x_adault_True+':
                ind_photo = id_active_status[user_id][5]
                
                try:
                        
                        new_path = "media/temporary/" + user_id + ".jpg"
                        with open(new_path, "wb") as f:
                                f.write(id_active_status[user_id][4][ind_photo])
                        photo = open(new_path, 'rb')        
                        id_active_status[user_id][5] += 1
                        await bot.send_photo(query.from_user.id,photo,reply_markup=inline_buttons("adult_test_start+",answer,user_id))
                except:
                        id_active_status[user_id][4] = None
                        id_active_status[user_id][5] = 0
                        await bot.send_message(query.from_user.id,"Bot:Вся галлерея просмотренна")
                        
                #await bot.edit_message_text("Bot:для просмотра галлереи нужна подписка и возраст +18",query.from_user.id,
                                #query.message.message_id)
                
                        
               
##administration
@dp.callback_query_handler(vote_cb.filter(action=['add_archive','remove_file']))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
        global j_video_short
        callback_data_action = callback_data['action']
        file = admin_file
        #path = file.split("/")[2]
        path = callback_data['data']
        print(path)
        if callback_data_action == 'remove_file':
                print(file)
                os.remove(file)
                if path=="Развлечения":
                        j_video_short = p_base.video_agr.fun()
                await bot.send_message(query.from_user.id,"Файл удален")        
                
        else:
                if path=="Развлечения":
                        path = "media/fun_short_videos/" + file.split("/")[-1]
                        print(path)
                        copy(file,path,follow_symlinks=True)
                        await bot.send_message(query.from_user.id,"Файл сохранен в архив")
            

                
                
      
                  

if __name__ == '__main__':
    #dp.loop.create_task(for_anecdots(84000))    
    executor.start_polling(dp, skip_updates=True)


