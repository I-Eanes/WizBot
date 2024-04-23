import discord
from discord.ext import commands
import requests
import json

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
    text = requests.get(f'{API}spells')
    data = json.loads(text.content)
    await ctx.send(data)

@bot.command()
async def spell(ctx, args):
    try:
        text = requests.get(f'{API}spells/{args}')
        data = json.loads(text.content)
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
async def test(ctx):
    await ctx.send("Tis' I Wizbot, I am definitely fully sentient because this not scripted at all!")

# Run bot with token
bot.run("MTIxMDMxNjk0NDk5Mzk0NzY3OA.GIZ0hO.l0aef7Z4i3r6MHOmsqy0QCn7p3ok-t7hlwhLBs")