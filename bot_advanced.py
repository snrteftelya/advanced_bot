import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from bs4 import BeautifulSoup
import requests
import datetime
import time
from aiogram import Bot, Dispatcher, executor, types
from sqlite_db import Database
from config import token, open_weather_token, kolya, olya
#dasha
#,mum, nikita
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
import json
from main import check_news_update
from main import sport_class, world_class, society_class, economy_class, politics_class, regions_class, accident_class
from main import president_class, kaleidoscope_class
from main import technological_class, cultural_class, playbill_class, comments_class, interview_class, mix_class
import random


storage = MemoryStorage()
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


db = Database('user_base.db')

class registration(StatesGroup):
    user_name = State()




@dp.message_handler(commands="start", state=None)
async def start(message: types.Message, state: FSMContext):
    start_buttons = ["Курсы валют💵", "Погода\U00002601"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("Новости📰")
    await state.finish()
    await message.answer('Выбери что-нибудь из меню', reply_markup=keyboard)




@dp.message_handler(lambda message: 'меню' in message.text, state="*")
async def start(message: types.Message, state: FSMContext):
    start_buttons = ["Курсы валют💵", "Погода\U00002601"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("Новости📰")
    await state.finish()
    await message.answer('Выбери что-нибудь из меню', reply_markup=keyboard)



class weather_get(StatesGroup):
    weather_country = State()
    weather_region = State()

@dp.message_handler(lambda message: 'Погода' in message.text, state=None)
async def weather(message: types.Message, state: FSMContext):
    start_buttons = ["Беларусь🇧🇾", "Россия🇷🇺"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("В меню➡")
    await message.answer("Выберите страну", reply_markup=keyboard)
    await weather_get.weather_country.set()


@dp.message_handler(lambda message: 'Беларусь' in message.text, state=weather_get.weather_country)
async def get_keyboard_belarus(message: types.Message, state: FSMContext):
    start_buttons = ["Брест", "Витебск", "Гомель", "Гродно", "Могилёв", "Минск"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("В меню➡")
    await message.answer("Выберите город", reply_markup=keyboard)
    await weather_get.weather_region.set()


@dp.message_handler(Text(equals=["Брест", "Витебск", "Гомель", "Гродно", "Могилёв", "Минск"]),\
                    state=weather_get.weather_region)
async def get_weather_belarus(message: types.Message, state: FSMContext):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
    )
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]

    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотри в окно, не пойму что там за погода!"

    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])
    start_buttons = ["Курсы валют💵", "Погода\U00002601"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("Новости📰")
    await message.answer(f"{datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}\n"
          f"Город: {hbold(city)}\n"
          f"{wd}\nТемпература: {hunderline(cur_weather)}{hunderline('C°')}\n"
          f"Ветер: {wind} м/с\nВлажность: {humidity}%\n"
          f"Восход солнца: {sunrise_timestamp.strftime('%H:%M')}\nЗакат солнца: {sunset_timestamp.strftime('%H:%M')}\n"
        f"Продолжительность дня: {length_of_the_day}\n", reply_markup=keyboard
        )
    await state.finish()



@dp.message_handler(lambda message: 'Россия' in message.text, state=weather_get.weather_country)
async def get_keyboard_russia(message: types.Message, state: FSMContext):
    start_buttons1 = ["Москва","Санкт-Петербург"]
    start_buttons2 = ["Новосибирск", "Екатеринбург"]
    start_buttons3 =  ["Казань", "Иркутск", "Тюмень"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*start_buttons1).row(*start_buttons2).row(*start_buttons3).insert("В меню➡")
    await message.answer("Выберите город", reply_markup=keyboard)
    await weather_get.weather_region.set()



@dp.message_handler(Text(equals=["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Иркутск",\
                                 "Тюмень"]), state=weather_get.weather_region)
async def get_weather_russia(message: types.Message, state: FSMContext):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
    )
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]

    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотри в окно, не пойму что там за погода!"

    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])
    start_buttons = ["Курсы валют💵", "Погода\U00002601"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("Новости📰")
    await message.answer(f"{datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}\n"
          f"Город: {hbold(city)}\n"
          f"{wd}\nТемпература: {hunderline(cur_weather)}{hunderline('C°')}\n"
          f"Ветер: {wind} м/с\nВлажность: {humidity}%\n"
          f"Восход солнца: {sunrise_timestamp.strftime('%H:%M')}\nЗакат солнца: {sunset_timestamp.strftime('%H:%M')}\n"
        f"Продолжительность дня: {length_of_the_day}\n", reply_markup=keyboard
        )
    await state.finish()

@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(v['date_time'])}" \
               f"{hbold(v['article_time'])}\n\n" \
               f"#{v['article_topic']}\n\n" \
               f"{v['article_title']}\n\n" \
               f"{v['article_url']}"

        await message.answer(news)


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(v['date_time'])}" \
                       f"{hbold(v['article_time'])}\n\n" \
                       f"#{v['article_topic']}\n\n" \
                       f"{v['article_title']}\n\n" \
                       f"{v['article_url']}"
                await bot.send_message(kolya, news, disable_notification=True)
                await bot.send_message(olya, news, disable_notification=True)
                #await bot.send_message(dasha, news, disable_notification=True)
                #await bot.send_message(mum, news, disable_notification=True)
                #await bot.send_message(nikita, news, disable_notification=True)

        await asyncio.sleep(40)

@dp.message_handler(lambda message: 'Новости' in message.text)
async def get_keyboard_news(message: types.Message):
    news_buttons1 = ["Спорт🏀", "В мире🗺️", "Общество👫"]
    news_buttons2 = ["Экономика💸", "Политика🤴", "Регионы🇧🇾"]
    news_buttons3 = ["Происшествия💥", "Калейдоскоп🤪"]
    news_buttons4 = ["Президент👨‍💼", "Технологии‍💻", "Культура🕯️"]
    news_buttons5 = ["Афиша📰", "Комменты💬", "Интервью🎤"]
    news_buttons6 = ["Mix новостей🔀", "В меню➡"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*news_buttons1).row(*news_buttons2).row(*news_buttons3).row(*news_buttons4).row(*news_buttons5)\
        .row(*news_buttons6)
    await message.answer("Новости по рубрикам:", reply_markup=keyboard)


@dp.message_handler(lambda message: 'Mix новостей' in message.text)
async def mix_news(message: types.Message):
    mix_news_list = []
    mix_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    mix_news = mix_class()
    for i in mix_news:
        if i not in mix_news_sorted:
            mix_news_sorted.append(i)
    for n in mix_news_sorted:
        x = news_dict.get(n)
        mix_news_list.append(x)
    for v in mix_news_list:
        news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
        await message.answer(news)
        time.sleep(5)


@dp.message_handler(lambda message: 'Спорт' in message.text)
async def sport_news(message: types.Message):
    sport_news_list = []
    sport_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    sport_news = sport_class()
    if len(sport_news) > 0:
        for i in sport_news:
            if i not in sport_news_sorted:
                sport_news_sorted.append(i)
        for n in sport_news_sorted:
            x = news_dict.get(n)
            sport_news_list.append(x)
        for v in (sport_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',\
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)

@dp.message_handler(lambda message: 'В мире' in message.text)
async def world_news(message: types.Message):
    world_news_list = []
    world_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    world_news = world_class()
    if len(world_news) > 0:
        for i in world_news:
            if i not in world_news_sorted:
                world_news_sorted.append(i)
        for n in world_news_sorted:
            x = news_dict.get(n)
            world_news_list.append(x)
        for v in (world_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Общество' in message.text)
async def society_news(message: types.Message):
    society_news_list = []
    society_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    society_news = society_class()
    if len(society_news) > 0:
        for i in society_news:
            if i not in society_news_sorted:
                society_news_sorted.append(i)
        for n in society_news_sorted:
            x = news_dict.get(n)
            society_news_list.append(x)
        for v in (society_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Экономика' in message.text)
async def economy_news(message: types.Message):
    economy_news_list = []
    economy_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    economy_news = economy_class()
    if len(economy_news) > 0:
        for i in economy_news:
            if i not in economy_news_sorted:
                economy_news_sorted.append(i)
        for n in economy_news_sorted:
            x = news_dict.get(n)
            economy_news_list.append(x)
        for v in (economy_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Политика' in message.text)
async def politics_news(message: types.Message):
    politics_news_list = []
    politics_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    politics_news = politics_class()
    if len(politics_news) > 0:
        for i in politics_news:
            if i not in politics_news_sorted:
                politics_news_sorted.append(i)
        for n in politics_news_sorted:
            x = news_dict.get(n)
            politics_news_list.append(x)
        for v in (politics_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Регионы' in message.text)
async def regions_news(message: types.Message):
    regions_news_list = []
    regions_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    regions_news = regions_class()
    if len(regions_news) > 0:
        for i in regions_news:
            if i not in regions_news_sorted:
                regions_news_sorted.append(i)
        for n in regions_news_sorted:
            x = news_dict.get(n)
            regions_news_list.append(x)
        for v in (regions_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Происшествия' in message.text)
async def accident_news(message: types.Message):
    accident_news_list = []
    accident_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    accident_news = accident_class()
    if len(accident_news) > 0:
        for i in accident_news:
            if i not in accident_news_sorted:
                accident_news_sorted.append(i)
        for n in accident_news_sorted:
            x = news_dict.get(n)
            accident_news_list.append(x)
        for v in (accident_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Президент' in message.text)
async def president_news(message: types.Message):
    president_news_list = []
    president_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    president_news = president_class()
    if len(president_news) > 0:
        for i in president_news:
            if i not in president_news_sorted:
                president_news_sorted.append(i)
        for n in president_news_sorted:
            x = news_dict.get(n)
            president_news_list.append(x)
        for v in (president_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Калейдоскоп' in message.text)
async def kaleidoscope_news(message: types.Message):
    kaleidoscope_news_list = []
    kaleidoscope_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    kaleidoscope_news = kaleidoscope_class()
    if len(kaleidoscope_news) > 0:
        for i in kaleidoscope_news:
            if i not in kaleidoscope_news_sorted:
                kaleidoscope_news_sorted.append(i)
        for n in kaleidoscope_news_sorted:
            x = news_dict.get(n)
            kaleidoscope_news_list.append(x)
        for v in (kaleidoscope_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Технологии' in message.text)
async def technological_news(message: types.Message):
    technological_news_list = []
    technological_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    technological_news = technological_class()
    if len(technological_news) > 0:
        for i in technological_news:
            if i not in technological_news_sorted:
                technological_news_sorted.append(i)
        for n in technological_news_sorted:
            x = news_dict.get(n)
            technological_news_list.append(x)
        for v in (technological_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Культура' in message.text)
async def cultural_news(message: types.Message):
    cultural_news_list = []
    cultural_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    cultural_news = cultural_class()
    if len(cultural_news) > 0:
        for i in cultural_news:
            if i not in cultural_news_sorted:
                cultural_news_sorted.append(i)
        for n in cultural_news_sorted:
            x = news_dict.get(n)
            cultural_news_list.append(x)
        for v in (cultural_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Афиша' in message.text)
async def playbill_news(message: types.Message):
    playbill_news_list = []
    playbill_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    playbill_news = playbill_class()
    if len(playbill_news) > 0:
        for i in playbill_news:
            if i not in playbill_news_sorted:
                playbill_news_sorted.append(i)
        for n in playbill_news_sorted:
            x = news_dict.get(n)
            playbill_news_list.append(x)
        for v in (playbill_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Комменты' in message.text)
async def comments_news(message: types.Message):
    comments_news_list = []
    comments_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    comments_news = comments_class()
    if len(comments_news) > 0:
        for i in comments_news:
            if i not in comments_news_sorted:
                comments_news_sorted.append(i)
        for n in comments_news_sorted:
            x = news_dict.get(n)
            comments_news_list.append(x)
        for v in (comments_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


@dp.message_handler(lambda message: 'Интервью' in message.text)
async def interview_news(message: types.Message):
    interview_news_list = []
    interview_news_sorted = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    interview_news = interview_class()
    if len(interview_news) > 0:
        for i in interview_news:
            if i not in interview_news_sorted:
                interview_news_sorted.append(i)
        for n in interview_news_sorted:
            x = news_dict.get(n)
            interview_news_list.append(x)
        for v in (interview_news_list)[-5:]:
            news = f"{hbold(v['date_time'])}" \
                f"{hbold(v['article_time'])}\n\n" \
                f"#{v['article_topic']}\n\n" \
                f"{v['article_title']}\n\n" \
                f"{v['article_url']}"
            await message.answer(news)
    else:
        emoji_sad = ['😬', '🤥', '😔', '😴', '😪', '😕', '😟', '🙁', '☹', '😮', '😯', '😲', '😳',
                     '😦', '😧', '😖', '😣', '😭', '😢', '😥', '😰', '😞', '😓', '😿']
        emoji_select_sad = random.choice(emoji_sad)
        await message.answer("Пока нету новостей данной категории" + emoji_select_sad)


class curses(StatesGroup):
    curses_region = State()



@dp.message_handler(lambda message: 'Курсы валют' in message.text, state=None)
async def get_curses_keyboard(message: types.Message, state: FSMContext):
    #start_buttons = ["brest", "vitebsk", "gomel", "mogilev", "minsk"]
    start_buttons = ["Брест", "Витебск", "Гомель", "Гродно", "Могилёв", "Минск"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("В меню➡")
    await message.answer("Выберите город", reply_markup=keyboard)
    await curses.curses_region.set()




@dp.message_handler(Text(equals='Гродно'), state=curses.curses_region)
async def get_curses_grodno(message: types.Message, state: FSMContext):
    listik = []
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }
    url = f"https://myfin.by/currency/usd/grodno"
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    articles_cards = soup.find_all('td')
    currency = soup.find('tbody').find_all('td')
    date = soup.find('h1').text.strip()
    date1 = date[:5]
    date2 = date[13:22]
    date3 = date[29::]
    for element in articles_cards:
        element = element.text.strip()
        listik.append(element)
    usd_in = listik[1]
    usd_out = listik[2]
    value_list = (
     f'{hbold("*" + date1 + date2 + date3 + "*")}\n\n'
     f'Покупка USD: {hcode(usd_in[:4] + " BYN")}\n'
     f'Продажа USD: {hcode(usd_out[:4] + " BYN")}\n\n'
     f'Покупка EUR: {hcode(listik[4] + " BYN")}\n'
     f'Продажа EUR: {hcode(listik[5] + " BYN")}\n\n'
     f'Покупка 10 PLN: {hcode(listik[7] + " BYN")}\n'
     f'Продажа 10 PLN: {hcode(listik[8] + " BYN")}\n\n'
    )
    start_buttons = ["Курсы валют💵", "Погода\U00002601"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("Новости📰")
    await message.answer(value_list, reply_markup=keyboard)
    await state.finish()








@dp.message_handler(Text(equals=["Брест", "Витебск", "Гомель", "Могилёв", "Минск"]), state=curses.curses_region)
async def get_curses(message: types.Message, state: FSMContext):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }
    if message.text == 'Брест':
        city = 'brest'
    if message.text == 'Витебск':
        city = 'vitebsk'
    if message.text == 'Гомель':
        city = 'gomel'
    if message.text == 'Могилёв':
        city = 'mogilev'
    if message.text == 'Минск':
        city = 'minsk'
    url = f"https://myfin.by/currency/usd/{city}"
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    articles_cards = soup.find("tbody")
    currency = soup.find('tbody').find_all('td')
    date = soup.find('h1').text.strip()
    date1 = date[:5]
    date2 = date[13:22]
    date3 = date[31::]
    value_list = (
     f'{hbold("*" + date1 + date2 + date3 + "*")}\n\n'
     f'Покупка USD: {hcode(currency[1].text.strip() + " BYN")}\n'
     f'Продажа USD: {hcode(currency[2].text.strip() + " BYN")}\n\n'
     f'Покупка EUR: {hcode(currency[6].text.strip() + " BYN")}\n'
     f'Продажа EUR: {hcode(currency[7].text.strip() + " BYN")}\n\n'
     f'Покупка 100 RUB: {hcode(currency[11].text.strip() + " BYN")}\n'
     f'Продажа 100 RUB: {hcode(currency[12].text.strip() + " BYN")}\n\n'
     f'Покупка 10 PLN: {hcode(currency[16].text.strip() + " BYN")}\n'
     f'Продажа 10 PLN: {hcode(currency[17].text.strip() + " BYN")}\n\n'
     f'Покупка 100 UAH: {hcode(currency[21].text.strip() + " BYN")}\n'
     f'Продажа 100 UAH: {hcode(currency[22].text.strip() + " BYN")}\n'
    )
    start_buttons = ["Курсы валют💵", "Погода\U00002601"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons).insert("Новости📰")
    await message.answer(value_list, reply_markup=keyboard)
    await state.finish()

@dp.message_handler()
async def none_func(message: types.Message):
    await message.answer('Я тебя не понимаю...\nВоспользуйся командой /start')





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)