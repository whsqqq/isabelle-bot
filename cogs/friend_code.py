import discord
import json
from discord.ext import commands
import re
import config


class FriendCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'"FriendCode" Loaded')

    @commands.hybrid_group(name='sw', invoke_without_command=True)
    async def sw(self, ctx):
        embed = discord.Embed(
            title="Неправильное действие, укажите, что конкретно вы хотите, `add` `edit` `delete`")
        embed.set_author(name="Что-то пошло не так...",
                         icon_url=config.NookIncNegative)
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)

    @sw.command(name='add', description='Добавить свой код друга', with_app_command=True)
    async def add(self, ctx, friend_code=None):
        user_id = str(ctx.author.id)
        with open('text/sw.json', 'r') as f:
            sw_data = json.load(f)

        if not friend_code or not isinstance(friend_code, str) or not re.match(config.sw_pattern, friend_code):
            embed = discord.Embed(
                title="Неправильный формат данных. Учтите, что формат должен быть `XXXX-XXXX-XXXX`. Пример: `!sw add 1234-1234-1234`")
            embed.set_author(name="Что-то пошло не так...",
                             icon_url=config.NookIncNegative)
            embed.set_footer(text=f"Выполнил: {ctx.author}")
            await ctx.send(embed=embed)
            return
        sw_data[user_id] = friend_code
        with open('text/sw.json', 'w') as f:
            json.dump(sw_data, f)
        embed = discord.Embed(title="Код друга добавлен в ваш паспорт!")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url=config.NookIncPositive)
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)

    @sw.command(name='edit', description='Изменить свой код друга', with_app_command=True)
    async def edit(self, ctx, friend_code=None):
        user_id = str(ctx.author.id)
        with open('text/sw.json', 'r') as f:
            sw_data = json.load(f)
        if not friend_code or not isinstance(friend_code, str) or not re.match(config.sw_pattern, friend_code):
            embed = discord.Embed(
                title="Неправильный формат данных. Учтите, что формат должен быть `число.месяц`. Пример: `!sw edit 1234-1234-1234`")
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
        sw_data[user_id] = friend_code
        with open('text/sw.json', 'w') as f:
            json.dump(sw_data, f)
        embed = discord.Embed(title="Вы успешно изменили свой код друга!")
        embed.set_author(name="Изменения в паспорт внесены успешно!",
                         icon_url=config.NookIncNeutral)
        embed.set_footer(text=f"Выполнил: {ctx.author}")
        await ctx.send(embed=embed)

    @sw.command(name='delete', description='Удалить свой код друга', with_app_command=True)
    async def delete(self, ctx):
        user_id = str(ctx.author.id)
        with open('text/sw.json', 'r') as f:
            sw_data = json.load(f)
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


async def setup(bot):
    await bot.add_cog(FriendCode(bot))
