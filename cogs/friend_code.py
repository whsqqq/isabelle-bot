import random
import asyncio
import discord
import json
from datetime import datetime
from discord.ext import commands
import re
import os
import config


class FriendCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sw(self, ctx, action=None, sw=None):
        user_id = str(ctx.author.id)
        with open('text/sw.json', 'r') as f:
            sw_data = json.load(f)
        if action == 'add':
            if not sw or not isinstance(sw, str) or not re.match(config.sw_pattern, sw):
                embed = discord.Embed(
                    title="Неправильный формат данных. Учтите, что формат должен быть `XXXX-XXXX-XXXX`. Пример: `!sw add 1234-1234-1234`.")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            sw_data[user_id] = sw
            with open('text/sw.json', 'w') as f:
                json.dump(sw_data, f)
            embed = discord.Embed(title="Код друга добавлен в ваш паспорт!")
            embed.set_author(name="Изменения в паспорт внесены успешно!",
                             icon_url=config.NookIncPositive)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
        elif action == 'edit':
            if not sw or not isinstance(sw, str) or not re.match(config.sw_pattern, sw):
                embed = discord.Embed(
                    title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!sw edit 1234-1234-1234`.")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            if user_id not in sw_data:
                embed = discord.Embed(
                    title="Вы ещё не указали свой код друга. Чтобы это сделать, вы можете воспользоваться командой `!sw add`")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            sw_data[user_id] = sw
            with open('text/sw.json', 'w') as f:
                json.dump(sw_data, f)
            embed = discord.Embed(title="Вы успешно изменили свой код друга!")
            embed.set_author(name="Изменения в паспорт внесены успешно!",
                             icon_url=config.NookIncNeutral)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
        elif action == 'delete':
            if user_id not in sw_data:
                embed = discord.Embed(
                    title="Вы ещё не указали свой код друга. Чтобы это сделать, вы можете воспользоваться командой `!sw add`")
                embed.set_author(name="Что-то пошло не так...",
                                 icon_url=config.NookIncNegative)
                embed.set_footer(text=f"Выполнил: {ctx.author}")
                await ctx.send(embed=embed)
                return
            del sw_data[user_id]
            with open('text/sw.json', 'w') as f:
                json.dump(sw_data, f)
            embed = discord.Embed(title="Вы успешно удалили свой код друга!")
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
            print('Cog "FriendCode" loaded')


async def setup(bot):
    await bot.add_cog(FriendCode(bot))