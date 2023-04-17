import random
import json
from datetime import datetime

TOKEN = 'MTA5NzE1MjUyNzE5MzA5NjI4Mg.Grds5a.cwCusizARhx-OqkcNHcT7d1qFNn4b2q0wqeo00'

BROADCAST_CHANNEL_ID = '1093486430967304223'
DODOAIRLINES_CHANNEL_ID = '973616908106604578'

OWNER_ID = '298410723586080768'

months = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}

colors = [0x9dffb0, 0x81f1f7, 0xfffffa, 0xc48d3f, 0xfff563, 0x84d9e0]

with open('text/isabelle_holiday_phrases.json', 'r', encoding='utf-8') as f:
    holiday_phrases = json.load(f)

# Загрузка данных из JSON файла
with open("text/bdays2.json", "r") as f:
    bdays = json.load(f)

# Загрузка данных из TXT файла с сообщениями
with open('text/isabelle_random_phrases.txt', 'r', encoding='utf-8') as f:
    random_phrases = f.readlines()

# Загрузка данных из TXT файла с приветствиями
with open('text/greetings.txt', 'r', encoding='utf-8') as f:
    random_greetings = f.readlines()

# Открываем файл с обычными сообщениями
with open("text/no_bday.txt", "r") as f:
    no_bday_phrases = f.readlines()


# Функция для выбора случайного сообщения из TXT файла с сообщениями
def get_random_message():
    return random.choice(random_phrases)


# Функция для выбора случайного сообщения из TXT файла с приветствиями
def get_random_greeting():
    return random.choice(random_greetings)


# Функция для проверки, является ли текущая дата праздником
def is_holiday_today():
    today = datetime.today()
    month_day = f'{today.day:02d}.{today.month:02d}'
    holiday = holiday_phrases.get(month_day)
    return holiday
