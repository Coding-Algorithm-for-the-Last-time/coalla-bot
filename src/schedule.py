import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
env = os.environ.get

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{env('DISCORD_BOT_ID')}> ", intents=intents)


@bot.event
async def on_ready():
    await bot.get_channel(env("DISCORD_TEST_CHANNEL_ID")).send("hello")
    exit(0)


bot.run(env("DISCORD_BOT_TOKEN"))
