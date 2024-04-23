import discord
from discord.ext import commands
import requests
import json
import random

# api
API = "http://127.0.0.1:8000/"

# Sets the bot to listen for all possible triggers
intents = discord.Intents.all()

# Creates a bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)


# Event that prints a message when bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord.")


@bot.command()
async def spells(ctx):
    data = json.loads(requests.get(f'{API}spells').content)[0]
    await ctx.send(data)


@bot.command()
async def spell(ctx, args):
    try:
        data = json.loads(requests.get(f'{API}spells/{args}').content)[0]
        await ctx.send(data)
    except:
        await ctx.send("Please make sure you input a valid Spell ID.")


@bot.command()
async def info(ctx):
    try:
        data = json.loads(requests.get(f'{API}user/{ctx.author.id}').content)
        data[0][0] = ctx.author.display_name
        await ctx.send(data[0])
    except:
        await ctx.send("This user could not be found, try using !hello first if you are new.")


@bot.command()
async def hello(ctx):
    temp = (requests.get(f'{API}user/{ctx.author.id}')).content
    if temp[0] == 91:
        requests.post(f'{API}user/new/{ctx.author.id}')
        await ctx.send("Welcome to the Wizbot!")


@bot.command()
async def duel(ctx):
    user = json.loads(requests.get(f'{API}user/{ctx.author.id}').content)[0]
    npc = json.loads(requests.get(f'{API}npc/{user[1]}').content)[0]
    await ctx.send(f"You are dueling {npc[1]} The {npc[2]}")
    results = await npcduel(ctx, npc, user)
    await ctx.send(results)


@bot.command()
async def test(ctx):
    await ctx.send("Tis' I Wizbot, I am definitely fully sentient because this not scripted at all!")


class Dueler:
    def __init__(self, name, hp, spell1, spell2):
        self.name = name
        self.hp = hp
        self.spell1 = spell1
        self.spell2 = spell2
        self.effect = 0

    def print(self):
        return(f"{self.name},{self.hp},{self.spell1},{self.spell2},{self.effect}")


async def npcduel(message, npc, user):
    duser = Dueler(message.author.display_name, (10 + user[1]) * 2,
                   (json.loads(requests.get(f'{API}spells/{user[2]}').content)[0]),
                   (json.loads(requests.get(f'{API}spells/{user[3]}').content))[0])
    dnpc = Dueler(f"{npc[1]} The {npc[2]}", duser.hp, (json.loads(requests.get(f'{API}spells/{user[2]}').content)[0]),
                  (json.loads(requests.get(f'{API}spells/{user[3]}').content))[0])
    gr = 0
    while duser.hp > 0 and dnpc.hp > 0:
        npcspell = random.randint(1, 2)
        if npcspell == 1:
            await message.send(f"{dnpc.name} is casting {dnpc.spell1[1]}")
            duser.hp = duser.hp - ((dnpc.spell1[2] + 1) * 4)
        else :
            await message.send(f"{dnpc.name} is casting {dnpc.spell2[1]}")
            dnpc.hp = dnpc.hp + ((dnpc.spell1[2] + 1) * 2)
        await message.send(f"{duser.hp}, {dnpc.hp}")
    if duser.hp <= 0:
        return("You have lost!")
    else:
        return("You have won!")

# Run bot with token
bot.run("MTIxMDMxNjk0NDk5Mzk0NzY3OA.GIZ0hO.l0aef7Z4i3r6MHOmsqy0QCn7p3ok-t7hlwhLBs")
