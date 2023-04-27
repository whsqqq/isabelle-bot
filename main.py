import config
import discord
from discord.ext import commands
import os


class Isabelle(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None,
                         application_id=1097152527193096282)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await bot.tree.sync()


bot = Isabelle()


# Ping lol
@bot.hybrid_command(name='ping', description='Показывает задержку между сервером бота', with_app_command=True)
async def ping(ctx):
    latency = float('{:.3f}'.format(bot.latency))
    embed = discord.Embed(title="Pong! :flags:", description=f"Задержка - **{latency}**ms", color=0xff7a7a)
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!help ☆'))


bot.run(config.TOKEN)
