import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

import leetcode
import github

load_dotenv()
env = os.environ.get

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{env('DISCORD_BOT_ID')}> ", intents=intents)

problem_list = {}
# {
#   id: {
#
#       },
#   id: {

#       },
# }


@bot.event
async def on_ready():
    print(f"Login bot: {bot.user}")


@bot.event
async def on_message(message):
    # TODO 깃헙 연동을 위해 봇이 답변 받아서 처리하기 위한 코드
    # if message.reference and message.reference.id in problem_list:
    #     print(message.author.id)
    #     print(message.content)
    #     print(message.reference)

    channel_id = [
        int(env("DISCORD_TEST_CHANNEL_ID")),
        int(env("DISCORD_COALLA_CHANNEL_ID")),
    ]
    if bot.user not in message.mentions:
        return
    if message.channel.id not in channel_id:
        await message.channel.send(
            "coalla 스터디 채널에서 질문해주세요! https://discordapp.com/channels/987566840257589298/1081911427213840404"
        )
        return

    await bot.process_commands(message)


def errer_msg(id):
    return f"""<@{id}> 해당 명령어를 찾을 수 없습니다. 사용 가능한 명령어는 다음과 같습니다.
1. "핑" : 봇의 응답속도 확인
2. "문제골라줘 <난이도: 쉬움, 중간, 어려움>" : leetcode 문제 고르기"""


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(errer_msg(ctx.message.author.id))
    else:
        print(f"에러 발생: {error}")


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
        # TODO 깃허브와 연동을 위해 선택된 문제 저장
        # problem_list[msg.id] = {"author": ctx.author.id, **result["result"]}
        # print(problem_list)


# TODO 깃허브에 자동 push
# @bot.command()
# async def 문제담아줘(ctx, arg=None):


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


bot.run(env("DISCORD_BOT_TOKEN"))
