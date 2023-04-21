import random
import asyncio
import discord
import json
from datetime import datetime
from discord.ext import commands
import re
import os
import config


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bday(self, ctx, action=None, bday=None):
        user_id = str(ctx.author.id)
        with open('text/bdays.json', 'r') as f:
            bday_data = json.load(f)
        if action == 'add':
            if not bday or not re.match(r'^\d{1,2}\.\d{1,2}$', bday) or int(bday.split(".")[0]) > 31 or int(bday.split(".")[1]) > 12:
                embed = discord.Embed(
                    title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!bday add 01.01`.")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            bday_data[user_id] = bday
            with open('text/bdays.json', 'w') as f:
                json.dump(bday_data, f)
            embed = discord.Embed(title="Дата рождения добавлена в ваш паспорт!")
            embed.set_author(name="Изменения в паспорт внесены успешно!",
                             icon_url=config.NookIncPositive)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
        elif action == 'edit':
            if not bday or not re.match(r'^\d{1,2}\.\d{1,2}$', bday) or int(bday.split(".")[0]) > 31 or int(bday.split(".")[1]) > 12:
                embed = discord.Embed(
                    title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!bday add 01.01`.")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            if user_id not in bday_data:
                embed = discord.Embed(
                    title="Вы ещё не указали свой день рождения. Чтобы это сделать, вы можете воспользоваться командой `!bday add`")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            bday_data[user_id] = bday
            with open('text/bdays.json', 'w') as f:
                json.dump(bday_data, f)
            embed = discord.Embed(title="Вы успешно изменили свою дату рождения")
            embed.set_author(name="Изменения в паспорт внесены успешно!",
                             icon_url=config.NookIncNeutral)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
        elif action == 'delete':
            if user_id not in bday_data:
                embed = discord.Embed(
                    title="Вы ещё не указали свой день рождения. Чтобы это сделать, вы можете воспользоваться командой `!bday add`")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            del bday_data[user_id]
            with open('text/bdays.json', 'w') as f:
                json.dump(bday_data, f)
            embed = discord.Embed(title="Вы успешно удалили свою дату рождения!")
            embed.set_author(name="Изменения в паспорт внесены успешно!",
                             icon_url=config.NookIncPositive)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Неправильное действие, укажите, что конкретно вы хотите, `add` `edit` `delete`")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url=config.NookIncNegative)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)

        @commands.Cog.listener()
        async def on_ready(self):
            print('Cog "Birthday" loaded')


async def setup(bot):
    await bot.add_cog(Birthday(bot))