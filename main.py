# from inspect import Traceback
# from operator import add
# import re
# from traceback import TracebackException
# from webbrowser import get
# import aiogram
# import re
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from markupsafe import Markup
import config
import random
import asyncio
from datetime import date
from aiogram.dispatcher.filters import BoundFilter
import os
import requests
from requests_html import HTMLSession
import csv
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from googletrans import Translator
import json
import arrow

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
# bot = Bot(token="5314423100:AAG7LWeBRFOguuJAHrDJHUAfx119FmNpG0E")
# bot = Bot(token="5313866230:AAGM7JR9nH44dkpiLXA1S1G4BW323FXuOy8")
dp = Dispatcher(bot, storage=storage)

muted = []

class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message : types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()

dp.filters_factory.bind(AdminFilter)


# get string with number and letter and multiply number on letter's meaning (time)
async def get_time(string):
    if string[-1] == "s":
        return int(string[:-1])
    elif string[-1] == "m":
        return int(string[:-1]) * 60
    elif string[-1] == "h":
        return int(string[:-1]) * 3600
    elif string[-1] == "d":
        return int(string[:-1]) * 86400
    elif string[-1] == "w":
        return int(string[:-1]) * 604800
    elif string[-1] == "o":
        return int(string[:-1]) * 2592000
    elif string[-1] == "y":
        return int(string[:-1]) * 31536000
    # if string doesn't contain any of the symbols but only numbers
    elif string.isdigit():
        return int(string)
    else:
        return 0

# @dp.message_handler()
# async def on_message(message):
#     if message.chat.id in muted:
#         return
#     await message.answer_dice(emoji=message.dice)
    

@dp.message_handler(content_types="dice", chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def dice(message):
    # smiles = ["🎲", "🎯", "🏀", "⚽️", "🎰", "🎳"]
    # smileInMsg = ""
    # for smile in smiles:
    #     if smile in message.text:
    #         smileInMsg = smile 
    # if smileInMsg == "": return
    if message.chat.id in muted:
        return
    await message.answer_dice(emoji=message.dice)
    # await message.sendDice(message.chat.id, smileInMsg)
    # await message.reply(smile)

# @dp.message_handler(commands=['help'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
# async def process_help_command(message: types.Message):
#     await message.reply("*Commands this bot can do:* \n" +
###     "/mute # - mutes for the # of minutes (admin-only)\n" +
###     "/unmute - stops the mute (admin-only)\n" +
###     "/addanti - adds a random anti (admin-only)\n" +
###     "*Quotes:* \n" +
###     "/addquote <quote> - adds a quote to the quote list \n" +
###     "/add - adds message you replied to as a quote \n" +
###     # "/add :user: - adds message you replied to as a quote with user who sent the command as author \n" +
###     "/quote - sends a random quote \n" +
###     "/searchquote <content of the quote> - sends a random quote containing the following words \n" +
###     "/quoteid # - the quote that matches the # \n" +
###     "*Images:* \n" +
###     "/addimage <optional text> - adds an image to the image list (upload image with command) \n" +
###     "/image - sends a random image \n" +
###     "/imagesearch <image text or author> - sends a random image containing the following text \n" +
###     "/imageid # - the image that matches the # \n" +
#     "_Send any of these stickers 🎲🎯🏀⚽️🎰🎳 and Brobot will respond_ \n" +
###     "/yomamma - displays a random your momma joke \n" +
###     "/prayer - says a random verse from the king James bible \n" +
###     "/8ball - says a random 8 ball msg \n" +
###     '/mx - responds a vodka quote \n' +
###     "/remindme <delay> <text> - reminds you set text after set days \n"
###     "_While setting delay, use 1s for 1 second, 1m for 1 minute, 1h for 1 hour, 1w for 1 week, 1o for 1 month and 1y for 1 year_ \n"
###     "/version - displays the latest version \n" +
###     "/anti - sends a random anti \n" +
###     "/motivation - sends a random motivational quote \n" +
###     "/ud <word> - send an urban dictionary definition of the word \n" +
###     "/weather <city> - send \n" +
###     "/rps - challenge a person you are replying to to play rock paper scissors \n" +
###     "/rpsleaders - see a leaderboard of rock paper scissors players \n" +
###     "/translate - reply to message or enter text after the command to translate it to English \n" +
###     "/buddhism - sends a Biddhist quote\n" +
###     "/hindu - sends a Hindu quote \n" +
###     "/atheist - sends an atheist quote \n" +
###     "/satan - sends a satanic quote \n" +
###     "/marx - sends a marxist quote \n" +
###     "/johnnycash - sends a quote from Johnny Cash \n" +
###     "/joelosteen - sends a quote from Joel Osteen \n" +
###     "/onlyfans or /of - sends a random photo from OnlyFans \n" +
###     "/nword <person> - shows how many times the user has said the n-word", parse_mode = 'Markdown')

religion_help_btn = InlineKeyboardButton('Religion', callback_data='religion_help')
fun_help_btn = InlineKeyboardButton('Fun', callback_data='fun_help')
productivity_help_btn = InlineKeyboardButton('Productivity', callback_data='productivity_help')
surfing_help_btn = InlineKeyboardButton('Surfing', callback_data='surfing_help')
help_kb1 = InlineKeyboardMarkup().add(religion_help_btn, fun_help_btn, productivity_help_btn).add(surfing_help_btn)

back_help_btn = InlineKeyboardButton('Back', callback_data='help_back')
help_back_kb = InlineKeyboardMarkup().add(back_help_btn)

help_dict = {
    "religion":
        "*RELIGION commands:* \n\n" +
        "/prayer - says a random verse from the king James bible \n" +
        "/buddhism - sends a Biddhist quote\n" +
        "/hindu - sends a Hindu quote \n" +
        "/atheist - sends an atheist quote \n" +
        # "/satan - sends a satanic quote \n" +
        "/marx - sends a marxist quote \n" +
        "/joelosteen - sends a quote from Joel Osteen",
    "fun":
        "*FUN commands:* \n\n" +
        "/johnnycash - sends a quote from Johnny Cash" +
        "/8ball - says a random 8 ball msg \n",
    "productivity":
        "*PRODUCTIVITY commands:* \n\n" +
        "/motivation - sends a random motivational quote \n" +
        "/ud <word> - send an urban dictionary definition of the word \n" +
        # "/weather <place> - sends current weather in the place \n" +
        # "/surf <place> - sends current surfing stats in the place \n" +
        "/translate - reply to message or enter text after the command to translate it to English \n" +
        "/version - displays the latest version \n\n" +
        "/remindme <delay> <text> - reminds you set text after set days \n" +
        "_Notice: While setting delay, use 1s for 1 second, 1m for 1 minute, 1h for 1 hour, 1w for 1 week, 1o for 1 month and 1y for 1 year_",
    "surfing":
        "*SURFING commands :* \n\n" +
        "/weather <place> - sends current weather in the place \n" +
        "/surf <place> - sends current surfing stats in the place \n" +
        "/ai <place> - sends a detailed analyse of current surfing conditions in the place *(PREMIUM-ONLY)* ",
}

@dp.message_handler(commands=['help'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def process_help_command(message: types.Message):
    await message.reply("*H E L P* \n\n" +
                        "_Send any of these stickers 🎲🎯🏀⚽️🎰🎳 and BDB will respond_ \n\n" +
                        "Choose a category to display a list of its commands:", parse_mode = 'Markdown', reply_markup=help_kb1)


@dp.callback_query_handler(lambda c: c.data.endswith('_help'))
async def process_callback_help(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text=help_dict[callback_query.data.replace("_help", "")], parse_mode = 'Markdown', reply_markup=help_back_kb)

@dp.callback_query_handler(lambda c: c.data == 'help_back')
async def process_help_command(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("*H E L P* \n\n" +
                        "_Send any of these stickers 🎲🎯🏀⚽️🎰🎳 and BDB will respond_ \n\n" +
                        "Choose a category to display a list of its commands:", parse_mode = 'Markdown', reply_markup=help_kb1)

async def remindme(message):
    try:
        delay = message.get_args().split(" ")[0]
        seconds_delay = await get_time(delay)
        text = " ".join(message.get_args().split(" ")[1:])
        
        if not delay.isdigit():
            if float(delay[:-1]) < 1:
                await message.reply(f"You cannot have a reminder in less than 1{delay[-1]}!")
                return
        elif delay.isdigit():
            if float(delay) < 1:
                await message.reply("You cannot have a reminder in less than 1 second!")
                return
        elif seconds_delay == 0:
            await message.reply("Wrong command usage!")
            return
        await message.reply("Reminder set")
        #await asyncio.sleep(delay)
        await asyncio.sleep(seconds_delay)
        await bot.send_message(message.chat.id, text=f"@{message.from_user.username} {text}")
    except Exception as e:
        print(e)
        await message.reply("Wrong command usage")

@dp.message_handler(commands=['version'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def version(message: types.Message):
    await message.reply(config.VERSION)

@dp.message_handler(commands=['8ball'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def ball(message: types.Message):
    if message.get_args() != "":
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
                "Yes.", "Yes - definitely.", "You may rely on it."]
    else:
        responses = ["What are you asking sir?", "I can only predict the future not what you are asking", "You're a dumbass, ask a question first"]
    await message.reply(random.choice(responses))

@dp.message_handler(commands=['prayer'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def version(message: types.Message):
    url = "https://dailyverses.net/random-bible-verse/kjv"
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        await message.reply("An error occurred")
        return
    verse = response.html.find('.v1', first=True).text
    await message.reply(verse)

# /Buddhism
# /Hindu
# /Atheist
# /Satan
# /Marx
# /Johnnycash

@dp.message_handler(commands=['buddhism'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def buddhism(message: types.Message):
    url = await getAPI("http://palicanon.codebuckets.com.au/api/quote")
    text = url.get("text")
    author = url.get("author")
    await message.reply(f"{text} © {author}")

file = open("atheistQuotes.json", "r", encoding="utf-8")
atheistQuotes = json.loads(file.read())
file.close()

file = open("hinduQuotes.json", "r")
hinduQuotes = json.loads(file.read())
file.close()

file = open("johnnyCashQuotes.json", "r", encoding="utf-8")
johnnyCashQuotes = json.loads(file.read())
file.close()

file = open("joelosteenquotes.json", "r", encoding="utf-8")
joelOsteenQuotes = json.loads(file.read())
file.close()

file = open("marxQuotes.txt", "r", encoding="utf-8")
marxQuotes = []
for line in file:
    marxQuotes.append(line)
file.close()

@dp.message_handler(commands=['johnnycash'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def atheist(message: types.Message):
    quote = random.choice(johnnyCashQuotes)
    await message.reply(f'{quote} \n© Johnny Cash')

@dp.message_handler(commands=['joelosteen'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def atheist(message: types.Message):
    quote = random.choice(joelOsteenQuotes)
    await message.reply(f'{quote} © Joel Osteen')

@dp.message_handler(commands=['marx'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def atheist(message: types.Message):
    quote = random.choice(marxQuotes)
    await message.reply(quote)

@dp.message_handler(commands=['hindu'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def atheist(message: types.Message):
    quote = random.choice(hinduQuotes)
    await message.reply(quote)

@dp.message_handler(commands=['atheist'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def atheist(message: types.Message):
    quote = random.choice(atheistQuotes)
    await message.reply(quote)

@dp.message_handler(commands=['satan'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def satan(message: types.Message):
    url = await getAPI("https://lucifer-quotes.vercel.app/api/quotes")
    quote = url[0].get("quote")
    author = url[0].get("author")
    await message.reply(f"{quote} © {author}")

async def getAPI(link):
    return requests.get(link).json()

@dp.message_handler(commands=['motivation'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def motivation(message: types.Message):
    file = csv.reader(open('motivational.csv', 'r'))
    chosen_row = random.choice(list(file))
    if chosen_row[0] == "":
        await message.reply(f"{chosen_row[1]}")
        return
    await message.reply(f"{chosen_row[1]} ~{chosen_row[0]}")

@dp.message_handler(commands="ud", chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def urbandictionary(message: types.Message):
    try:
        word = message.get_args()
    except Exception:
        await message.reply("Invalid command usage")
        return
    if word == "":
        await message.reply("Invalid command usage")
        return
    url = f"http://api.urbandictionary.com/v0/define?term={word}"
    response = requests.get(url)
    try:
        definition = response.json().get("list")[0].get("definition").replace("[", "").replace("]", "")
        # print(response.json().get("list"))
        example = response.json().get("list")[0].get("example").replace("[", "").replace("]", "")
        await message.reply(f"{definition}\n\n\n{example}")
    except Exception:
        await message.reply("No definition found")

@dp.message_handler(commands=['weather'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def weather(message : types.Message):
    try:
        city = message.get_args()
    except Exception:
        await message.reply("Invalid command usage")
        return
    if city == "":
        await message.reply("Invalid command usage")
        return
    WEATHER_API_KEY = "30b9ff2af389faf8feeb848735dadb6b"
    if city.isnumeric(): url = f"http://api.openweathermap.org/data/2.5/weather?q={city}, US&appid={WEATHER_API_KEY}&units=imperial"
    else: url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    try:
        data = response.json()
        coords = data.get("coord")
        lat = coords.get("lat")
        lon = coords.get("lon")

        temp = data.get("main").get("temp")
        feels_like = data.get("main").get("feels_like")
        humidity = data.get("main").get("humidity")
        country = data.get("sys").get("country")
        wind_speed = data.get("wind").get("speed")
        city = data.get("name")
        weather_name = data.get("weather")[0].get("main")
        weather_description = data.get("weather")[0].get("description")
        await message.reply(f"Place: {city} ({country}, Latitude: {lat}, Longitude: {lon}) \n \n*{weather_name} ({weather_description})*\nTemperature: {temp}°F\nFeels like: {feels_like}°F\nHumidity: {humidity}%\nWind speed: {wind_speed}mph", parse_mode = 'Markdown')
    except Exception as e:
        print(e)
        await message.reply("No weather found")


@dp.message_handler(commands=['surf'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def surf(message : types.Message):
    try:
        city = message.get_args()
    except Exception:
        await message.reply("Invalid command usage")
        return
    if city == "":
        await message.reply("Invalid command usage")
        return
    WEATHER_API_KEY = "30b9ff2af389faf8feeb848735dadb6b"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=imperial"
        response = requests.get(url).json()
        city = response.get("name")
        country = response.get("sys").get("country")
        coords = response.get("coord")
        lat = coords.get("lat")
        lon = coords.get("lon")

        responseSurf = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': lat,
            'lng': lon,
            'params': ','.join(['waveHeight', 'windDirection', 'windSpeed', 'waterTemperature', "swellHeight", "swellPeriod", "secondarySwellHeight"])
            # 'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            # 'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
        },
        headers={
            'Authorization': '0d833f2c-b1ea-11ed-bce5-0242ac130002-0d833fae-b1ea-11ed-bce5-0242ac130002'
        }
        )
        json_data = responseSurf.json()
        # print(json_data)
        currentDayStats = json_data.get('hours')[0]
        waterTemperature = round(random.choice(list(currentDayStats.get('waterTemperature').values()))*(9/5)+32, 2)
        waveHeight = random.choice(list(currentDayStats.get('waveHeight').values()))
        windDirection = random.choice(list(currentDayStats.get('windDirection').values()))
        windSpeed = random.choice(list(currentDayStats.get('windSpeed').values()))
        swellHeight = random.choice(list(currentDayStats.get('swellHeight').values()))
        swellPeriod = random.choice(list(currentDayStats.get('swellPeriod').values()))
        secondarySwellHeight = random.choice(list(currentDayStats.get('secondarySwellHeight').values()))
        await message.reply(f"Place: {city} ({country}, Latitude: {lat}, Longitude: {lon}) \n\nWater temperature: {waterTemperature}°F\n" +
                            f"Wave height: {round(float(waveHeight)*3.28, 2)} ft\n" +
                            f"Wind direction: {windDirection}° (0° = wind from North) \n" +
                            f"Wind speed: {round(float(windSpeed)*3.28, 2)} ft/s \n" +
                            f"Swell wave height: {round(float(swellHeight)*3.28, 2)} ft \n" +
                            f"Swell wave period: {swellPeriod}s \n" +
                            f"Height of secondary swell waves: {round(float(secondarySwellHeight)*3.28, 2)} ft") # + ""
    except Exception:
        await message.reply("No surf found in this area. You might consider checking your spelling")

import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "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"

# Set the model and prompt
model_engine = "gpt-3.5-turbo"
# prompt = '''Analyse this data for surfing. For which kind of surfers is it applicable? Is the weather good for surfing?
#         Place: Miami (US, Latitude: 25.7743, Longitude: -80.1937) 

#         Water temperature: 77.97°F
#         Wave height: 0.97m
#         Wind direction: 166.96° (0° = wind from North) 
#         Wind speed: 5.5m/s 
#         Swell wave height: 0.59m 
#         Swell wave period: 3.46s 
#         Height of secondary swell waves: 0.13m'''

# # Set the maximum number of tokens to generate in the response
# max_tokens = 1024




# print(request['choices'][0]['message']['content'])
# Generate a response
# completion = openai.Completion.create(
#     engine=model_engine,
#     prompt=prompt,
#     max_tokens=max_tokens,
#     temperature=0.5,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
# )

# # Print the response
# print(completion.choices[0].text)

@dp.message_handler(commands=['ai'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def ai(message : types.Message):
    try:
        city = message.get_args()
    except Exception:
        await message.reply("Invalid command usage")
        return
    if city == "":
        await message.reply("Invalid command usage")
        return
    WEATHER_API_KEY = "30b9ff2af389faf8feeb848735dadb6b"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=imperial"
        response = requests.get(url).json()
        city = response.get("name")
        country = response.get("sys").get("country")
        coords = response.get("coord")
        lat = coords.get("lat")
        lon = coords.get("lon")

        responseSurf = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': lat,
            'lng': lon,
            'params': ','.join(['waveHeight', 'windDirection', 'windSpeed', 'waterTemperature', "swellHeight", "swellPeriod", "secondarySwellHeight"])
            # 'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            # 'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
        },
        headers={
            'Authorization': '0d833f2c-b1ea-11ed-bce5-0242ac130002-0d833fae-b1ea-11ed-bce5-0242ac130002'
        }
        )
        json_data = responseSurf.json()
        # print(json_data)
        currentDayStats = json_data.get('hours')[0]
        waterTemperature = round(random.choice(list(currentDayStats.get('waterTemperature').values()))*(9/5)+32, 2)
        waveHeight = random.choice(list(currentDayStats.get('waveHeight').values()))
        windDirection = random.choice(list(currentDayStats.get('windDirection').values()))
        windSpeed = random.choice(list(currentDayStats.get('windSpeed').values()))
        swellHeight = random.choice(list(currentDayStats.get('swellHeight').values()))
        swellPeriod = random.choice(list(currentDayStats.get('swellPeriod').values()))
        secondarySwellHeight = random.choice(list(currentDayStats.get('secondarySwellHeight').values()))
        # prompt = f'''Analyse this data for surfing. For which kind of surfers is it applicable? Is the weather good for surfing?
        #         Place: {city} ({country}, Latitude: {lat}, Longitude: {lon}) \n\nWater temperature: {waterTemperature}°F\n
        #         Wave height: {waveHeight}m\n
        #         Wind direction: {windDirection}° (0° = wind from North) \n
        #         Wind speed: {windSpeed}m/s \n
        #         Swell wave height: {swellHeight}m \n
        #         Swell wave period: {swellPeriod}s \n
        #         Height of secondary swell waves: {secondarySwellHeight}m'''
        prompt = f'''Place: {city} ({country}, Latitude: {lat}, Longitude: {lon}) \n\nWater temperature: {waterTemperature}°F\n
                Wave height: {round(float(waveHeight)*3.28, 2)} ft \n
                Wind direction: {windDirection}° (0° = wind from North) \n
                Wind speed: {round(float(windSpeed)*3.28, 2)} ft/s \n
                Swell wave height: {round(float(swellHeight)*3.28, 2)} ft \n
                Swell wave period: {swellPeriod}s \n
                Height of secondary swell waves: {round(float(secondarySwellHeight)*3.28, 2)} ft'''
        await message.reply() # + ""
        request = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                    {"role": "system", "content": prompt}
                ]
        )
        await message.reply(request['choices'][0]['message']['content'])
    except Exception:
        await message.reply("No surf found in this area. You might consider checking your spelling")
    # responseSurf = requests.get(
    # 'https://api.chatbotkit.com/v1/conversation/clex0zici000hmd08kujur67h/send',
    #     method = 'POST',
    #     headers={
    #         'Authorization': 'Bearer sk-5084033fbdd35845446c0c39fefe226f29b471c4bfddde27b2ee2bcae713f382',
    #         'Content-Type': 'application/json'
    #     }
    # )

    # headers = {
    #     'Authorization': '',
    #     'Content-Type': 'application/json'
    # }

    # url = "https://api.chatbotkit.com/v1/conversation/clex0zici000hmd08kujur67h/send"

    # ae = requests.post(url, headers=headers)

    # # json_data = responseSurf.json()
    # await message.reply(ae)

async def how_to_name_user(user: types.User):
    if user.username != None:
        return f"@{user.username}"
    
    if user.first_name != None:
        if user.last_name != None:
            return f"{user.first_name} {user.last_name}"
        else:
            return f"{user.first_name}"

translator = Translator()

@dp.message_handler(commands=['translate'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def translate(message: types.Message):
    if message.reply_to_message != None: 
        translatedText = translator.translate(message.reply_to_message.text)
    elif message.get_args().replace(" ", "") != "":
        translatedText = translator.translate(message.get_args())
    else:
        await message.reply("Reply to a message or write something to translate!")
        return
    await message.reply(f"{translatedText.text} ({translatedText.src})")

@dp.message_handler(commands=['chatid'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], is_admin=True)
async def chat_id(message: types.Message):
    await message.reply(f"The ID of this group is: `{message.chat.id}`", parse_mode = 'Markdown')

# this_bot_id = config.TOKEN.split(":")[0]
# @dp.message_handler(content_types="new_chat_members", chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
# async def on_join(message: types.Message):
#     if str(message["new_chat_member"]["id"]) == this_bot_id:
#         await message.reply("Welcome to The Best Telegram Bot in The Universe! The Community decides what we build!")

lastMessageInChat = ""

# Setup prices
prices = [
    types.LabeledPrice(label='Tasty Waves Premium', amount=699),
    # types.LabeledPrice(label='Gift wrapping', amount=500),
]

# Setup shipping options
# shipping_options = [
#     types.ShippingOption(id='instant', title='WorldWide Teleporter').add(types.LabeledPrice('Teleporter', 1000)),
#     types.ShippingOption(id='pickup', title='Local pickup').add(types.LabeledPrice('Pickup', 300)),
# ]


# @dp.message_handler(commands=['start'])
# async def cmd_start(message: types.Message):
#     await bot.send_message(message.chat.id,
#                            "Hello, I'm the demo merchant bot."
#                            " I can sell you a Time Machine."
#                            " Use /buy to order one, /terms for Terms and Conditions")


# @dp.message_handler(commands=['terms'])
# async def cmd_terms(message: types.Message):
#     await bot.send_message(message.chat.id,
#                            'Thank you for shopping with our demo bot. We hope you like your new time machine!\n'
#                            '1. If your time machine was not delivered on time, please rethink your concept of time'
#                            ' and try again.\n'
#                            '2. If you find that your time machine is not working, kindly contact our future service'
#                            ' workshops on Trappist-1e. They will be accessible anywhere between'
#                            ' May 2075 and November 4000 C.E.\n'
#                            '3. If you would like a refund, kindly apply for one yesterday and we will have sent it'
#                            ' to you immediately.')


@dp.message_handler(commands=['premium'])
async def cmd_buy(message: types.Message):
    await bot.send_message(message.chat.id,
                           "*Tasty Waves Premium* \n\n"
                           "You are getting access to: \n"
                           " - Unlimited /ai <place> - generated surfing analytics in the place! \n"
                           " - Unlimited /surf <place> - surfing stats about any place (current limit: 5 calls a day) \n\n"
                           "Tasty Waves Premium is bought for the current chat: just 3.99$$ a month! \n\n"
                           "Demo: Use this test card number to pay: `4242 4242 4242 4242` + random other data"
                           , parse_mode='Markdown')
    await bot.send_invoice(message.chat.id, title='Tasty Waves Premium',
                           description="Remove any limits for just 3.99$ a month!",
                           provider_token="284685063:TEST:NTk1OTJlY2JhM2U5",
                           currency='usd',
                        #    photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
                        #    photo_height=512,  # !=0/None or picture won't be shown
                        #    photo_width=512,
                        #    photo_size=512,
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=prices,
                        #    start_parameter='time-machine-example',
                           payload='Waves Premium!')


# @dp.shipping_query_handler(lambda query: True)
# async def shipping(shipping_query: types.ShippingQuery):
#     await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
#                                     error_message='Oh, seems like our Dog couriers are having a lunch right now.'
#                                                   ' Try again later!')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="An error happened processing your payment."
                                                      "Try to pay again in a few minutes")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Thank you for your payment! Enjoy unlimited surfing!',
                           parse_mode='Markdown')

# import stripe
# # import smtplib
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from email.mime.text import MIMEText

# # Set up Stripe API with your API key
# stripe.api_key = "pk_test_51LGUrCKIWb6RHWtyz45OEzaxcQAqFj8g0rTrxWJPvmCVKrODRFNVuLZWoCJ5rMHYCDAfoZYkYnPkWPrcBM0PffGa00TalhaEWd"

# # Set up your SMTP email credentials
# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587
# # SMTP_USERNAME = "your_email@example.com"
# # SMTP_PASSWORD = "your_email_password"
# # EMAIL_FROM = "your_email@example.com"
# # EMAIL_SUBJECT = "Verification Code"

# # # Define a function to send an email
# # def send_email(to, verification_code):
# #     message = f"Your verification code is {verification_code}."
# #     msg = MIMEText(message)
# #     msg['Subject'] = EMAIL_SUBJECT
# #     msg['From'] = EMAIL_FROM
# #     msg['To'] = to

# #     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
# #         server.starttls()
# #         server.login(SMTP_USERNAME, SMTP_PASSWORD)
# #         server.sendmail(EMAIL_FROM, to, msg.as_string())

# class WebhookHandler(BaseHTTPRequestHandler):

#     # Define a method to handle incoming POST requests
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         payload = self.rfile.read(content_length)

#         # Retrieve the request's signature
#         sig_header = self.headers.get('Stripe-Signature')

#         # Verify the signature
#         try:
#             event = stripe.Webhook.construct_event(payload, sig_header, "YOUR_WEBHOOK_SECRET")
#         except ValueError as e:
#             # Invalid payload
#             self.send_response(400)
#             self.end_headers()
#             return
#         except stripe.error.SignatureVerificationError as e:
#             # Invalid signature
#             self.send_response(400)
#             self.end_headers()
#             return

#         # Handle the event
#         if event['type'] == 'payment_intent.succeeded':
#             handle_payment_intent_succeeded(event)

#         # Return a response to acknowledge receipt of the event
#         self.send_response(200)
#         self.end_headers()

#     def log_message(self, format, *args):
#         # Override log_message to suppress logging to stdout
#         return

# # Define a function to handle the 'payment_intent.succeeded' event
# def handle_payment_intent_succeeded(event):
#     payment_intent = event["data"]["object"]
#     customer_email = payment_intent["charges"]["data"][0]["billing_details"]["email"]
#     print(payment_intent)
#     print(customer_email)
#     # verification_code = "YOUR_VERIFICATION_CODE_HERE"
#     # send_email(customer_email, verification_code)

# # Set up a webhook endpoint URL to receive events
# def start_webhook_server():
#     httpd = HTTPServer(('localhost', 8000), WebhookHandler)
#     httpd.serve_forever()

# endpoint_secret = 'whsec_5d9cf870ac3be6d96a1ae180f41cddddecdc9f379ca41c9a85bbb9e5f2071e73'
# from flask import Flask, jsonify, request

# app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     event = None
#     payload = request.data

#     try:
#         event = json.loads(payload)
#     except:
#         print('⚠️  Webhook error while parsing basic request.' + str(e))
#         return jsonify(success=False)
#     if endpoint_secret:
#         # Only verify the event if there is an endpoint secret defined
#         # Otherwise use the basic event deserialized with json
#         sig_header = request.headers.get('stripe-signature')
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, endpoint_secret
#             )
#         except stripe.error.SignatureVerificationError as e:
#             print('⚠️  Webhook signature verification failed.' + str(e))
#             return jsonify(success=False)

#     # Handle the event
#     if event and event['type'] == 'payment_intent.succeeded':
#         payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
#         print('Payment for {} succeeded'.format(payment_intent['amount']))
#         # async def send():
#         #     await bot.send_message(chat_id, text)

#         # asyncio.run(send())
#         # Then define and call a method to handle the successful payment intent.
#         # handle_payment_intent_succeeded(payment_intent)
#     elif event['type'] == 'payment_method.attached':
#         payment_method = event['data']['object']  # contains a stripe.PaymentMethod
#         # Then define and call a method to handle the successful attachment of a PaymentMethod.
#         # handle_payment_method_attached(payment_method)
#     else:
#         # Unexpected event type
#         print('Unhandled event type {}'.format(event['type']))

#     return jsonify(success=True)

if __name__ == '__main__':
    executor.start_polling(dp)
