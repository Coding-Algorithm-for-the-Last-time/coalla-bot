import discord
from discord.ui import View, Button, Select
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from datetime import datetime


import leetcode
import github

load_dotenv()
env = os.environ.get

DISCORD_BOT_TOKEN = env("DISCORD_BOT_TOKEN")
DISCORD_BOT_ID = int(env("DISCORD_BOT_ID"))
DISCORD_TEST_CHANNEL_ID = int(env("DISCORD_TEST_CHANNEL_ID"))
DISCORD_COALLA_CHANNEL_ID = int(env("DISCORD_COALLA_CHANNEL_ID"))


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{DISCORD_BOT_ID}> ", intents=intents)


@tasks.loop(minutes=1)  # 메시지를 보낼 주기 설정 (1분으로 설정)
async def send_message():
    now_utc = datetime.utcnow()  # UTC로 현재시간 확인
    if (
        now_utc.weekday() == 4 and now_utc.hour == 11 and now_utc.minute == 0
    ):  # 한국 금요일 20시는 UTC로 금요일 11시
        content = f"이번 주 스터디 참석 여부를 확인합니다.\n스터디는 토요일 오전 8시 ~ 10시까지 진행됩니다.\n참석 여부는 이모지로 알려주세요. 🐨"
        message = await bot.get_channel(DISCORD_TEST_CHANNEL_ID).send(content)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

@tasks.loop(minutes=1)  # 메시지를 보낼 주기 설정 (1분으로 설정)
async def send_message():
    now_utc = datetime.utcnow()  # UTC로 현재시간 확인
    if (
        now_utc.weekday() == 4 and now_utc.hour == 22 and now_utc.minute == 30
    ):  # 한국 토요일 7시는 UTC로 금요일 22시
        content = f"스터디 시작 30분 전입니다! "
        message = await bot.get_channel(DISCORD_TEST_CHANNEL_ID).send(content)
        await message.add_reaction("✅")
        await message.add_reaction("❌")


@bot.event
async def on_ready():
    print(f"Login bot: {bot.user}")
    send_message.start()  # 주기적으로 메시지 보내는 작업 시작


@bot.event
async def on_message(message):
    channel_id = [DISCORD_TEST_CHANNEL_ID, DISCORD_COALLA_CHANNEL_ID]
    if bot.user not in message.mentions:
        return
    if message.channel.id not in channel_id:
        await message.channel.send(
            "coalla 스터디 채널에서 질문해주세요! https://discordapp.com/channels/987566840257589298/1081911427213840404"
        )
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"""<@{ctx.message.author.id}> 해당 명령어를 찾을 수 없습니다. 사용 가능한 명령어는 다음과 같습니다.
            1. "핑" : 봇의 응답속도 확인
            2. "문제골라줘 <난이도: 쉬움, 중간, 어려움>" : leetcode 문제 고르기"""
        )
    else:
        print(f"에러 발생: {error}")


# 명령어
@bot.command()
async def 핑(ctx):
    await ctx.send(
        f"<@{ctx.message.author.id}> 퐁! {round(round(bot.latency, 4)*1000)}ms"
    )


@bot.command()
async def 문제골라줘(ctx, arg=None):
    diff_dict = {"쉬움": "EASY", "중간": "MEDIUM", "어려움": "HARD"}
    diff = diff_dict.get(arg, None)
    result = leetcode.random_problem(diff=diff)
    if result["ok"]:
        data = result["result"]
        msg = await ctx.send(
            f"<@{ctx.message.author.id}> 네 문제를 골라드릴게요!\n\n1. 번호: {data['questionId']}\n2. 문제: {data['title']}\n3. 난이도: {data['difficulty']}\n4. 성공률: {round(data['acRate'], 1)}%\n5. 좋아요:{data['likes']}\n6. 싫어요:{data['dislikes']}\n7. 태그: {', '.join([tag['name'] for tag in data['topicTags']])}\nhttps://leetcode.com/problems/{data['titleSlug']}"
        )


# TODO 특정 조건에 해당하는 문제들 불러오기
# @bot.command()
# async def 문제보여줘(ctx, diff=None, order=0, sort=0, page=1):
#     print(ctx, diff, order, sort)
#     result = leetcode.random_problem(diff=diff, order=order, sort=sort)
#     if result["ok"]:
#         await ctx.send(
#             f"<@{ctx.message.author.id}> {leetcode.random_problem(diff=diff, order=order, sort=sort)}"
#         )


# TODO 특정 조건에 해당하는 문제 하나만 불러오기
# @bot.command()
# async def 한문제보여줘(ctx, diff=None, order=0, sort=0):
#     print(ctx, diff, order, sort)
#     await ctx.send(
#         f"<@{ctx.message.author.id}> {leetcode.random_problem(diff=diff, order=order, sort=sort)}"
#     )

# TODO 깃허브에 자동 push
# @bot.command()
# async def 문제담아줘(ctx, arg=None):


# @bot.command()
# async def 테스트(ctx):

#     button1 = Button(style=discord.ButtonStyle.green, label="네", emoji="🙆‍♂️")
#     button2 = Button(style=discord.ButtonStyle.red, label="아니오", emoji="🙅‍♂️")

#     opt = [
#         discord.SelectOption(label="label1", value="value1"),
#         discord.SelectOption(label="label2", value="value2"),
#         discord.SelectOption(label="label3", value="value3"),
#         discord.SelectOption(label="label4", value="value4"),

#            ]
#     select = Select(select_type=discord.ComponentType.string_select, options=opt, placeholder="주제를 골라주세요.")

#     async def callback(interaction):
#         print(interaction.data)
#         await interaction.followup.send(f"'{interaction.data['values'][0]}' (이)가 선택되었습니다.")

#     select.callback = callback

#     view = View(button1, button2, select, timeout=30.0)

#     await ctx.send(f"<@{ctx.message.author.id}> 주제를 골라주세요.", view=view)


# @bot.command()
# async def 역할선택(ctx):

#     # button1 = Button(style=discord.ButtonStyle.green, label="네", emoji="🙆‍♂️")
#     # button2 = Button(style=discord.ButtonStyle.red, label="아니오", emoji="🙅‍♂️")

#     # opt = [
#     #     discord.SelectOption(label="label1", value="value1"),
#     #     discord.SelectOption(label="label2", value="value2"),
#     #     discord.SelectOption(label="label3", value="value3"),
#     #     discord.SelectOption(label="label4", value="value4"),

#     #        ]
#     # select1 = Select(select_type=discord.ComponentType.string_select, options=opt, placeholder="주제를 골라주세요.")
#     select2 = Select(select_type=discord.ComponentType.role_select, placeholder="역할 고르기")

#     async def callback(interaction):
#         print(interaction.data)
#         await interaction.response.send_message(f"{interaction.data['resolved']['roles'][interaction.data['values'][0]]['name']}이 선택되었습니다.")


#     select2.callback = callback

#     # view = View(button1, button2, select1, select2, timeout=30.0, disable_on_timeout=True)
#     view = View(select2, timeout=30.0, disable_on_timeout=True)

#     await ctx.send(f"<@{ctx.message.author.id}>", view=view)

bot.run(DISCORD_BOT_TOKEN)
