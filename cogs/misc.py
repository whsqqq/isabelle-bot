import random
import asyncio
import discord
import json
from datetime import datetime
from discord.ext import commands
import re
import os
import config


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='help', description='Показывает команды этого бота', with_app_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Вот что у меня для вас есть!",
                              color=random.choice(config.colors))
        embed.add_field(name="День рождения",
                        value="`!bday add 01.01` - Добавить \n`!bday edit 20.12` - Изменить \n `!bday delete` - Удалить")
        embed.add_field(name="Код друга",
                        value="`!sw add 1234-1234-1234` - Добавить \n`!sw edit 1234-1234-1234` - Изменить \n `!sw delete` - Удалить")
        embed.add_field(name="Посмотреть паспорт", value="`!passport`")
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx):
        if ctx.message.author.id != int(config.OWNER_ID):
            await ctx.message.delete()
            return

        message = ctx.message.content[5:]  # получаем текст сообщения без префикса команды
        await ctx.send(message)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'"Misc" Loaded')


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
