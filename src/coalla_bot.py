import discord
from discord.ui import View, Button, Select
from discord.ext import commands, tasks
from discord.ui.item import Item
from dotenv import load_dotenv
import os
from datetime import datetime


from leetcode import Random_problem
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


# @tasks.loop(minutes=1)  # 메시지를 보낼 주기 설정 (1분으로 설정)
# async def send_message():
#     now_utc = datetime.utcnow()  # UTC로 현재시간 확인
#     if (
#         now_utc.weekday() == 4 and now_utc.hour == 11 and now_utc.minute == 0
#     ):  # 한국 금요일 20시는 UTC로 금요일 11시
#         content = f"이번 주 스터디 참석 여부를 확인합니다.\n스터디는 토요일 오전 8시 ~ 10시까지 진행됩니다.\n참석 여부는 이모지로 알려주세요. 🐨"
#         message = await bot.get_channel(DISCORD_TEST_CHANNEL_ID).send(content)
#         await message.add_reaction("✅")
#         await message.add_reaction("❌")

# @tasks.loop(minutes=1)  # 메시지를 보낼 주기 설정 (1분으로 설정)
# async def send_message():
#     now_utc = datetime.utcnow()  # UTC로 현재시간 확인
#     if (
#         now_utc.weekday() == 4 and now_utc.hour == 22 and now_utc.minute == 30
#     ):  # 한국 토요일 7시는 UTC로 금요일 22시
#         content = f"스터디 시작 30분 전입니다! "
#         message = await bot.get_channel(DISCORD_TEST_CHANNEL_ID).send(content)
#         await message.add_reaction("✅")
#         await message.add_reaction("❌")


@bot.event
async def on_ready():
    print(f"Login bot: {bot.user}")
    # send_message.start()  # 주기적으로 메시지 보내는 작업 시작


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
            f'<@{ctx.message.author.id}> 해당 명령어를 찾을 수 없습니다. 사용 가능한 명령어는 다음과 같습니다.\n1. "핑" : 봇의 응답속도 확인\n2. "문제골라줘" : leetcode 문제 고르기'
        )
    else:
        print(f"에러 발생: {error}")
        await ctx.send(f"<@{ctx.message.author.id}> 에러가 발생하였습니다. error: {error}")


# 명령어
@bot.command()
async def 핑(ctx):
    await ctx.send(
        f"<@{ctx.message.author.id}> 퐁! {round(round(bot.latency, 4)*1000)}ms"
    )


@bot.command()
async def 문제골라줘(ctx):
    tag_opt = [
        discord.SelectOption(label=lable, value=value)
        for lable, value in [
            ("Array", "array"),
            ("String", "string"),
            ("Hash Table", "hash-table"),
            ("Dynamic Programming", "dynamic-programming"),
            # ("Math",        "math"),
            ("Sorting", "sorting"),
            ("Greedy", "greedy"),
            ("Depth-First Search", "depth-first-search"),
            # ("Database",        "database"),
            # ("Binary Search",        "binary-search"),
            ("Breadth-First Search", "breadth-first-search"),
            ("Tree", "tree"),
            ("Matrix", "matrix"),
            ("Two Pointers", "two-pointers"),
            # ("Binary Tree",        "binary-tree"),
            # ("Bit Manipulation",        "bit-manipulation"),
            ("Heap (Priority Queue)", "heap-priority-queue"),
            ("Stack", "stack"),
            ("Graph", "graph"),
            # ("Prefix Sum",        "prefix-sum"),
            # ("Design",        "design"),
            # ("Simulation",        "simulation"),
            ("Counting", "counting"),
            # ("Backtracking",        "backtracking"),
            ("Sliding Window", "sliding-window"),
            # ("Union Find",        "union-find"),
            ("Linked List", "linked-list"),
            # ("Ordered Set",        "ordered-set"),
            ("Monotonic Stack", "monotonic-stack"),
            ("Recursion", "recursion"),
            # ("Enumeration",        "enumeration"),
            # ("Trie",        "trie"),
            ("Divide and Conquer", "divide-and-conquer"),
            # ("Binary Search Tree",        "binary-search-tree"),
            # ("Bitmask",        "bitmask"),
            ("Queue", "queue"),
            # ("Number Theory",        "number-theory"),
            ("Memoization", "memoization"),
            # ("Segment Tree",        "segment-tree"),
            # ("Geometry",        "geometry"),
            # ("Topological Sort",        "topological-sort"),
            # ("Binary Indexed Tree",        "binary-indexed-tree"),
            # ("Hash Function",        "hash-function"),
            # ("Game Theory",        "game-theory"),
            # ("Shortest Path",        "shortest-path")
        ]
    ]

    easy_btn = Button(label="EASY", emoji="😙")
    medium_btn = Button(label="MEDIUM", emoji="🤔")
    hard_btn = Button(label="HARD", emoji="🤯")
    btn_view = View(
        easy_btn, medium_btn, hard_btn, timeout=30.0, disable_on_timeout=True
    )

    select = Select(
        select_type=discord.ComponentType.string_select,
        options=tag_opt,
        placeholder="주제를 골라주세요.",
    )
    select_view = View(select, timeout=30.0, disable_on_timeout=True)

    problem_arg = {"diff": None, "tag": None}

    class Callback:
        def __init__(self, msg=""):
            self.msg = msg

        async def btn_callack(self, interaction):
            problem_arg["diff"] = self.msg
            easy_btn.disabled = True
            medium_btn.disabled = True
            hard_btn.disabled = True
            await interaction.response.edit_message(
                content=f"<@{ctx.message.author.id}> {self.msg} (이)가 선택되었습니다.",
                view=btn_view,
            )
            await ctx.send(f"<@{ctx.message.author.id}> 주제를 골라주세요.", view=select_view)

        async def select_callback(self, interaction):
            problem_arg["tag"] = interaction.data["values"][0]
            select.disabled = True
            await interaction.response.edit_message(
                content=f"<@{ctx.message.author.id}> '{interaction.data['values'][0]}' (이)가 선택되었습니다.",
                view=select_view,
            )
            problem = Random_problem(problem_arg["diff"], problem_arg["tag"])
            if problem.id:
                msg = f"<@{ctx.message.author.id}> 문제를 찾았습니다!\n\n1. 번호: {problem.id}\n2. 문제: {problem.title}\n3. 난이도: {problem.difficulty}\n4. 성공률: {round(problem.ac_rate, 1)}%\n5. 좋아요:{problem.likes}\n6. 싫어요:{problem.dislikes}\n7. 태그: {', '.join([tag['name'] for tag in problem.topic_tags])}\nhttps://leetcode.com/problems/{problem.title_slug}"
            else:
                msg = f"<@{ctx.message.author.id}> 문제를 찾지 못했습니다. 다시 시도해주세요."
            await ctx.send(msg)

    easy_btn.callback = Callback("EASY").btn_callack
    medium_btn.callback = Callback("MEDIUM").btn_callack
    hard_btn.callback = Callback("HARD").btn_callack
    select.callback = Callback().select_callback

    await ctx.send(f"<@{ctx.message.author.id}> 난이도를 골라주세요.", view=btn_view)


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
