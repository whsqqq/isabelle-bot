import discord
import json
from discord.ext import commands
import re
import config


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name='bday', invoke_without_command=True)
    async def bday(self, ctx):
        user_id = str(ctx.author.id)
        with open('text/bdays.json', 'r') as f:
            bday_data = json.load(f)
        embed = discord.Embed(
            title="Неправильное действие, укажите, что конкретно вы хотите, `add` `edit` `delete`")
        embed.set_author(name="Что-то пошло не так...",
                         icon_url=config.NookIncNegative)
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)

    @bday.command(name='add', description='Добавить свой день рождения', with_app_command=True)
    async def add(self, ctx, birthday=None):
        user_id = str(ctx.author.id)
        with open('text/bdays.json', 'r') as f:
            bday_data = json.load(f)
        if not birthday or not re.match(r'^\d{1,2}\.\d{1,2}$', birthday):
            embed = discord.Embed(
                title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!bday add 01.01`")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url=config.NookIncNegative)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        if user_id in bday_data:
            embed = discord.Embed(
                title="Вы уже указали свой день рождения! Чтобы изменить его, воспользуйтесь командой `/bday edit`")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url=config.NookIncNegative)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        bday_data[user_id] = birthday
        with open('text/bdays.json', 'w') as f:
            json.dump(bday_data, f)
        embed = discord.Embed(title="Дата рождения добавлена в ваш паспорт!")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url=config.NookIncPositive)
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)

    @bday.command(name='edit', description='Изменить свой день рождения', with_app_command=True)
    async def edit(self, ctx, birthday=None):
        user_id = str(ctx.author.id)
        with open('text/bdays.json', 'r') as f:
            bday_data = json.load(f)
        if not birthday or not re.match(r'^\d{1,2}\.\d{1,2}$', birthday):
            embed = discord.Embed(
                title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!bday add 01.01`")
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
        bday_data[user_id] = birthday
        with open('text/bdays.json', 'w') as f:
            json.dump(bday_data, f)
        embed = discord.Embed(title="Вы успешно изменили свою дату рождения")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url=config.NookIncNeutral)
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)

    @bday.command(name='delete', description='Удалить свой день рождения', with_app_command=True)
    async def delete(self, ctx):
        user_id = str(ctx.author.id)
        with open('text/bdays.json', 'r') as f:
            bday_data = json.load(f)

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

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'"Birthday" Loaded')


async def setup(bot):
    await bot.add_cog(Birthday(bot))