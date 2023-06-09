import random
import discord
import json
from discord.ext import commands
import config


class Passport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'"Passport" Loaded')

    @commands.hybrid_command(name='passport', description='Показать паспорт', with_app_command=True, aliases=['p', 'ps'])
    async def passport(self, ctx, member: discord.Member = None):
        with open("text/bdays.json", "r") as f:
            bdays = json.load(f)
        with open('text/sw.json', 'r') as f:
            sw_data = json.load(f)
        user = ctx.author if not member else member
        user_avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        embed = discord.Embed(title=f"Паспорт пользователя `{user.display_name}`", color=random.choice(config.colors))
        embed.set_author(name="NookLink",
                         icon_url=config.NookLinkImg)
        if user.discriminator == '0':
            embed.add_field(name="Имя пользователя:", value=f'@{user.name}', inline=True)
        else:
            embed.add_field(name="Имя пользователя:", value=f'{user.name}#{user.discriminator}', inline=True)
        if str(user.id) in bdays:
            day, month_num = map(int, bdays[str(user.id)].split('.'))
            month_name = config.months[month_num]
            embed.add_field(name="Дата рождения:", value=f'{day} {month_name}', inline=True)
        else:
            embed.add_field(name="Дата Рождения", value="Не указано", inline=True)
        if str(user.id) in sw_data:

            embed.add_field(name="Код друга:", value=f'SW-{sw_data[str(user.id)]}', inline=True)
        else:
            embed.add_field(name="Код друга:", value="Не указано", inline=True)
        embed.add_field(name="Прилетел на остров Юки:", value=user.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Роли:", value=", ".join([role.mention for role in reversed(user.roles[1:])]), inline=True)
        embed.set_thumbnail(url=user_avatar_url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Passport(bot))
