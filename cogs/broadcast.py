import discord
from discord.ext import commands, tasks
import json
import random
import datetime
import config


class Broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_holiday.start()

    @tasks.loop(count=1)
    async def check_holiday(self):
        now = datetime.datetime.now()
        key = f"{now.day}.{now.month}"
        with open("text/isabelle_holiday_phrases.json", "r", encoding="utf-8") as f:
            holiday_data = json.load(f)
        with open("text/bdays.json", "r") as f:
            bdays = json.load(f)
        today_bdays = [f"<@{u}>" for u, bday in bdays.items() if bday == datetime.datetime.today().strftime("%d.%m")]
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
        if key in holiday_data:
            await self.bot.get_channel(config.BROADCAST_CHANNEL_ID).send(f'{holiday_data[key]} \n{message}')
        else:
            now = datetime.datetime.today()
            day = now.day
            month = now.month
            month_name = config.months[month]
            with open("text/isabelle_random_phrases.txt", "r", encoding="utf-8") as f:
                random_phrases = f.read().splitlines()
            await self.bot.get_channel(config.BROADCAST_CHANNEL_ID).send(f'{config.get_random_greeting()}Сегодня - {day} {month_name}. {config.get_random_message()} \n{message}')

    @check_holiday.before_loop
    async def before_check_holiday(self):
        now = datetime.datetime.now()
        target_time = datetime.time(hour=8)
        if now.time() > target_time:
            tomorrow = now + datetime.timedelta(days=1)
            next_check = datetime.datetime.combine(tomorrow.date(), target_time)
        else:
            next_check = datetime.datetime.combine(now.date(), target_time)
        await discord.utils.sleep_until(next_check)


async def setup(bot):
    await bot.add_cog(Broadcast(bot))
