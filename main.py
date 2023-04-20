import random
import asyncio
import config
import discord
import json
from datetime import datetime
from discord.ext import commands
import re
import os

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


# Loading data from JSON file with holiday phrases
with open('text/isabelle_holiday_phrases.json', 'r', encoding='utf-8') as f:
    holiday_phrases = json.load(f)

# Loading data from JSON file with birthday dates
with open("text/bdays.json", "r") as f:
    bdays = json.load(f)

# Loading data from TXT file with random phrases
with open('text/isabelle_random_phrases.txt', 'r', encoding='utf-8') as f:
    random_phrases = f.readlines()

# Loading data from TXT file with random greetings
with open('text/greetings.txt', 'r', encoding='utf-8') as f:
    random_greetings = f.readlines()

# Loading data from TXT file which appears if no users has birthday
with open("text/no_bday.txt", "r") as f:
    no_bday_phrases = f.readlines()


# Function that broadcasts message to Resident Services
async def send_broadcast_message(message):
    channel = bot.get_channel(int(config.BROADCAST_CHANNEL_ID))
    await channel.send(message)


# Function that just send messages lol
async def send_message(channel, message):
    await channel.send(message)


# Function that sends random message if no one has birthday
async def send_random_message(channel):
    message = random.choice(no_bday_phrases)
    await channel.send(message)


# Daily Broadcast to Resident Services
async def send_daily_message():
    while True:
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:
            holiday = config.is_holiday_today()
            if holiday:
                # Проверяем, есть ли пользователи, у которых сегодня день рождения
                today_bdays = [f"<@{u}>" for u, bday in bdays.items() if bday == datetime.today().strftime("%d.%m")]
                if today_bdays:
                    if len(today_bdays) > 1:
                        bdays_list = ", ".join(today_bdays)
                        message = f"Сегодня день рождения у пользователей: {bdays_list}! Поздравляем вас с этим замечательным днем!"
                    else:
                        message = f"Сегодня день рождения у {today_bdays[0]}! Поздравляем вас с этим замечательным днем!"
                else:
                    with open("text/no_bday.txt", "r", encoding="utf-8") as f:
                        phrases = f.readlines()
                    message = random.choice(phrases).strip()

                await send_broadcast_message(f'{holiday} \n{message}')
            else:
                now = datetime.today()
                day = now.day
                month = now.month
                month_name = config.months[month]

                # Проверяем, есть ли пользователи, у которых сегодня день рождения
                today_bdays = [f"<@{u}>" for u, bday in bdays.items() if bday == datetime.today().strftime("%d.%m")]

                if today_bdays:
                    if len(today_bdays) > 1:
                        bdays_list = ", ".join(today_bdays)
                        message = f"Сегодня день рождения у пользователей: {bdays_list}! Поздравляем вас с этим замечательным днем!"
                    else:
                        message = f"Сегодня день рождения у {today_bdays[0]}! Поздравляем вас с этим замечательным днем!"
                else:
                    with open("text/no_bday.txt", "r", encoding="utf-8") as f:
                        phrases = f.readlines()
                    message = random.choice(phrases).strip()
                await send_broadcast_message(
                    f'{config.get_random_greeting()}Сегодня - {day} {month_name}. {config.get_random_message()} \n{message}')

        await asyncio.sleep(60)


# Ping lol
@bot.command()
async def ping(ctx):
    latency = float('{:.3f}'.format(bot.latency))
    embed = discord.Embed(title="Pong! :flags:", description=f"Задержка - **{latency}**ms", color=0xff7a7a)
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!help ☆'))
    bot.loop.create_task(send_daily_message())


async def main():
    await load()


asyncio.run(main())

bot.run(config.TOKEN)
