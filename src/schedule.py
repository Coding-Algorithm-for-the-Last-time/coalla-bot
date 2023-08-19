import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
env = os.environ.get

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{env('DISCORD_BOT_ID')}> ", intents=intents)
message = f"코!🐨알!🐨라!🐨\n이번에도 알고리즘 끝장내봅시다!!🐨\n\n<@{env('DISCORD_COALLA_TEAM_ID')}>이번주 토요일에 참석하는 분은 아래 이모지를 눌러주세요. 찡긋"

@bot.event
async def on_ready():
    sent_message = await bot.get_channel(int(env("DISCORD_COALLA_CHANNEL_ID"))).send(message)
    await sent_message.add_reaction("✅")
    await bot.close()


bot.run(env("DISCORD_BOT_TOKEN"))
