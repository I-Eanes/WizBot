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
async def spellbook(ctx):
    data = json.loads(requests.get(f'{API}spells').content)
    list = ""
    for spell in data:
        list += (f"Page Number: {spell[0]} Name: {spell[1]}\n")
    await ctx.send(list)


@bot.command()
async def page(ctx, args):
    try:
        data = json.loads(requests.get(f'{API}spells/{args}').content)[0]
        await ctx.send((f"Page Number: {data[0]} \nName: {data[1]} \nLVL: {data[2]} \nDescription: {data[3]}\n"))
    except:
        await ctx.send("Please make sure you input a valid Spell ID.")


@bot.command()
async def info(ctx):
    try:
        data = json.loads(requests.get(f'{API}user/{ctx.author.id}').content)[0]
        data[0] = ctx.author.display_name
        await ctx.send(f"Name: {data[0]}\n  LVL: {data[1]}\n  Spell 1: {data[2]}\n  Spell 2: {data[3]}")
    except:
        await ctx.send("This user could not be found, try using !hello first if you are new.")


@bot.command()
async def hello(ctx):
    temp = (requests.get(f'{API}user/{ctx.author.id}')).content
    if temp[0] == 91:
        requests.post(f'{API}user/new/{ctx.author.id}')
        await ctx.send("Welcome to the Wizbot!\n Commands:\n    !info - shows your user information\n    !spellbook - shows you all spells\n"
                       "    !page (Page #) - shows you more in depth information about a spell\n    !duel - allows you to use your spells in a duel with an NPC")


@bot.command()
async def duel(ctx):
    user = json.loads(requests.get(f'{API}user/{ctx.author.id}').content)[0]
    npc = json.loads(requests.get(f'{API}npc/{user[1]}').content)[0]
    await ctx.send(f"You are dueling {npc[1]} The {npc[2]}")
    results = await npcduel(ctx, npc, user)
    await ctx.send(results)


@bot.command()
async def duel(ctx, args):
    if ctx.message.mentions:
        foe = (await bot.fetch_user(int((f"{ctx.message.mentions}".split("=")[1]).split(" ")[0])))
        await pvpduel(ctx, json.loads(requests.get(f'{API}user/{ctx.author.id}').content)[0], json.loads(requests.get(f'{API}user/{foe.id}').content)[0])

class Dueler:
    def __init__(self, name, hp, spell1, spell2, id):
        self.name = name
        self.hp = hp
        self.spell1 = spell1
        self.spell2 = spell2
        self.effect = 0
        self.id = id

    def print(self):
        return(f"{self.name},{self.hp},{self.spell1},{self.spell2},{self.effect}")


async def npcduel(message, npc, user):
    duser = Dueler(message.author.display_name, (10 + user[1]) * 2,
                   (json.loads(requests.get(f'{API}spells/{user[2]}').content)[0]),
                   (json.loads(requests.get(f'{API}spells/{user[3]}').content))[0], message.author.id)
    dnpc = Dueler(f"{npc[1]} The {npc[2]}", duser.hp, (json.loads(requests.get(f'{API}spells/{user[2]}').content)[0]),
                  (json.loads(requests.get(f'{API}spells/{user[3]}').content))[0], 0)
    spellmod = 1
    while duser.hp > 0 and dnpc.hp > 0:
        npcspell = random.randint(1, 2)
        await userturn(message, duser, dnpc, spellmod)
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


async def pvpduel(ctx, chall, foe):
    dchall = Dueler(ctx.author.display_name, (10 + chall[1]) * 2,
                   (json.loads(requests.get(f'{API}spells/{chall[2]}').content)[0]),
                   (json.loads(requests.get(f'{API}spells/{chall[3]}').content))[0], chall[0])
    dfoe = Dueler((await bot.fetch_user(int((f"{ctx.message.mentions}".split("=")[1]).split(" ")[0]))).display_name, (10 + foe[1]) * 2,
                   (json.loads(requests.get(f'{API}spells/{foe[2]}').content)[0]),
                   (json.loads(requests.get(f'{API}spells/{foe[3]}').content))[0], foe[0])
    spellmod = 1
    while dchall.hp > 0 and dfoe.hp > 0:
        await userturn(ctx, dchall, dfoe, spellmod)
        await userturn(ctx, dchall, dfoe, spellmod)
    await ctx.send(f"{dchall.hp}, {dfoe.hp}")
    if dchall.hp <= 0:
        return("You have lost!")
    else:
        return("You have won!")

async def userturn(ctx, user, foe, spellmod):
    await ctx.send("What will you cast?")
    valid = 0
    discuser = await bot.fetch_user(user.id)
    while (valid != 1):
        msg = await bot.wait_for('message', check=lambda ctx: ctx.author.id == discuser)
        print("Check")
        if (int(msg.content) == user.spell1[0]):
            if 100 <= user.spell1[0] <= 199:
                foe.hp = foe.hp - (((foe.spell1[2] + 1) * 4) * spellmod)
                await ctx.send(f"You have cast {user.spell1[1]}")
            elif 200 <= user.spell1[0] <= 299:
                user.hp = user.hp + (((user.spell1[2] + 1) * 2) * spellmod)
                await ctx.send(f"You have cast {user.spell1[1]}")
            else:
                await ctx.send("Special Effect spells are not yet implemented, sorry.")
            valid = 1
        elif (int(msg.content) == user.spell2[0]):
            if 100 <= user.spell2[0] <= 199:
                foe.hp = foe.hp - (((foe.spell2[2] + 1) * 4) * spellmod)
                await ctx.send(f"You have cast {user.spell2[1]}")
            elif 200 <= user.spell2[0] <= 299:
                user.hp = user.hp + (((user.spell2[2] + 1) * 2) * spellmod)
                await ctx.send(f"You have cast {user.spell2[1]}")
            else:
                await ctx.send("Special Effect spells are not yet implemented, sorry.")
            valid = 1
        else:
            await ctx.send(
                f"Sorry, that is not a valid spell please cast either {user.spell1[0]} ({user.spell1[1]}) or {user.spell2[0]} ({user.spell2[1]})")


# Run bot with token
bot.run("MTIxMDMxNjk0NDk5Mzk0NzY3OA.GIZ0hO.l0aef7Z4i3r6MHOmsqy0QCn7p3ok-t7hlwhLBs")
