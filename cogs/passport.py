import random
import asyncio
import discord
from discord import app_commands
import json
from datetime import datetime
from discord.ext import commands
import re
import os
import config


class Passport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'"Passport" Loaded')

    @commands.hybrid_command(name='passport', description='Показать паспорт', with_app_command=True)
    async def passport(self, ctx, member: discord.Member = None):
        with open("text/bdays.json", "r") as f:
            bdays = json.load(f)
        with open('text/sw.json', 'r') as f:
            sw_data = json.load(f)
        user = ctx.author if not member else member
        user_avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        embed = discord.Embed(title=f"Паспорт пользователя {user.display_name}", color=random.choice(config.colors))
        embed.set_author(name="NookLink",
                         icon_url=config.NookLinkImg)
        embed.add_field(name="Имя пользователя:", value=f'{user.name}#{user.discriminator}', inline=True)
        if str(user.id) in bdays:

            embed.add_field(name="Дата рождения:", value=bdays[str(user.id)], inline=True)
        else:
            embed.add_field(name="Дата Рождения", value="Не указано", inline=True)
        if str(user.id) in sw_data:

            embed.add_field(name="Код друга:", value=f'SW-{sw_data[str(user.id)]}', inline=True)
        else:
            embed.add_field(name="Код друга:", value="Не указано", inline=True)
        embed.add_field(name="Прилетел на остров Юки:", value=user.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Роли:", value=", ".join([role.mention for role in user.roles[1:]]), inline=True)
        embed.set_thumbnail(url=user_avatar_url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Passport(bot))

