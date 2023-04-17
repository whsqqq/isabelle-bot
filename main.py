import random
import asyncio
import config
import discord
import json
from datetime import datetime
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help")

# Загрузка данных из JSON файла
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


# Функция для отправки сообщения в Бюро Услуг
async def send_broadcast_message(message):
    channel = bot.get_channel(int(config.BROADCAST_CHANNEL_ID))
    await channel.send(message)


# Функция для отправки сообщений
async def send_message(channel, message):
    await channel.send(message)


# Функция для отправки случайного сообщения в случае того, что дня рождения ни у кого нет
async def send_random_message(channel):
    message = random.choice(no_bday_phrases)
    await channel.send(message)


# Функция, которая будет выполняться каждый день в 9 утра
async def send_daily_message():
    while True:
        now = datetime.now()
        if now.hour == 14 and now.minute == 17:
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


@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Вот что у меня для вас есть!",
                          color=random.choice(config.colors))
    embed.add_field(name="День рождения",
                    value="`!bday add 01.01` - Добавить \n`!bday edit 20.12` - Изменить \n `!bday delete` - Удалить")
    embed.add_field(name="Посмотреть паспорт", value="`!passport`")
    await ctx.send(embed=embed)


# Команда, которая позволяет добавить, изменить или удалить свою дату рождения
@bot.command()
async def bday(ctx, action=None, bday=None):
    user_id = str(ctx.author.id)
    with open('text/bdays2.json', 'r') as f:
        bdays = json.load(f)
    if action == 'add':
        if not bday or not re.match(r'^\d{1,2}\.\d{1,2}$', bday):
            embed = discord.Embed(
                title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!bday add 01.01`.")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url="https://media.discordapp.net/attachments/782323112699887657/1097491978901540894/nook_inc_negative.png?width=670&height=670")
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        bdays[user_id] = bday
        with open('text/bdays2.json', 'w') as f:
            json.dump(bdays, f)
        embed = discord.Embed(title="Дата рождения добавлена в ваш паспорт!")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url="https://media.discordapp.net/attachments/782323112699887657/1097489775210012802/Nook_Inc.png?width=670&height=670")
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)
    elif action == 'edit':
        if not bday or not re.match(r'^\d{1,2}\.\d{1,2}$', bday):
            embed = discord.Embed(
                title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!bday add 01.01`.")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url="https://media.discordapp.net/attachments/782323112699887657/1097491978901540894/nook_inc_negative.png?width=670&height=670")
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        if user_id not in bdays:
            embed = discord.Embed(
                title="Вы ещё не указали свой день рождения. Чтобы это сделать, вы можете воспользоваться командой `!bday add`")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url="https://media.discordapp.net/attachments/782323112699887657/1097491978901540894/nook_inc_negative.png?width=670&height=670")
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        bdays[user_id] = bday
        with open('text/bdays2.json', 'w') as f:
            json.dump(bdays, f)
        embed = discord.Embed(title="Вы успешно изменили свою дату рождения")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url="https://media.discordapp.net/attachments/782323112699887657/1097491978326900766/Nook_Inc_neutral.png?width=670&height=670")
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)
    elif action == 'delete':
        if user_id not in bdays:
            embed = discord.Embed(
                title="Вы ещё не указали свой день рождения. Чтобы это сделать, вы можете воспользоваться командой `!bday add`")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url="https://media.discordapp.net/attachments/782323112699887657/1097491978901540894/nook_inc_negative.png?width=670&height=670")
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        del bdays[user_id]
        with open('text/bdays2.json', 'w') as f:
            json.dump(bdays, f)
        embed = discord.Embed(title="Вы успешно удалили свою дату рождения!")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url="https://media.discordapp.net/attachments/782323112699887657/1097489775210012802/Nook_Inc.png?width=670&height=670")
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Неправильное действие, укажите, что конкретно вы хотите, `add` `edit` `delete`")
        embed.set_author(name="Что-то пошло не так...",
                         icon_url="https://media.discordapp.net/attachments/782323112699887657/1097491978901540894/nook_inc_negative.png?width=670&height=670")
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)


@bot.command()
async def passport(ctx, member: discord.Member = None):
    with open("text/bdays2.json", "r") as f:
        bdays = json.load(f)
    user = ctx.author if not member else member
    user_avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    embed = discord.Embed(title=f"Паспорт пользователя {user.display_name}", color=random.choice(config.colors))
    embed.set_author(name="NookLink",
                     icon_url="https://media.discordapp.net/attachments/1093486430967304223/1097524248039411772/Nook_Inc_passport.png?width=670&height=670")
    embed.add_field(name="Имя пользователя:", value=f'{user.name}#{user.discriminator}', inline=True)
    if str(user.id) in bdays:

        embed.add_field(name="Дата рождения:", value=bdays[str(user.id)], inline=True)
    else:
        embed.add_field(name="Дата Рождения", value="Не указано", inline=True)
    embed.add_field(name="Прилетел на остров Юки:", value=user.joined_at.strftime("%m/%d/%Y"), inline=True)
    embed.add_field(name="Роли:", value=", ".join([role.mention for role in user.roles[1:]]), inline=True)
    embed.set_thumbnail(url=user_avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def say(ctx):
    if ctx.message.author.id != int(config.OWNER_ID):
        await ctx.message.delete()
        return

    message = ctx.message.content[5:]  # получаем текст сообщения без префикса команды
    await ctx.send(message)
    await ctx.message.delete()


@bot.command()
async def ping(ctx):
    latency = float('{:.3f}'.format(bot.latency))
    embed = discord.Embed(title="Pong! :flags:", description=f"Задержка - **{latency}**ms", color=0xff7a7a)
    await ctx.send(embed=embed)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(config.DODOAIRLINES_CHANNEL_ID)
    await channel.send(f'Приветствую, <@{member.id}>! Рады тебя видеть! Ознакомься с чатами слева, там ты найдешь правила, объявления и многое другое! Приятного времяпровождения! ☀️😺🐾')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(config.DODOAIRLINES_CHANNEL_ID)
    await channel.send(f'Прощай, <@{member.id}> Возвращайся, будем ждать!😘🐾')


# Обработчик события "ready"
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(send_daily_message())  # Создание объекта Task для отправки сообщений каждый день


bot.run(config.TOKEN)
