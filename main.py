import discord
from discord.ext import commands

# Sets the bot to listen for all possible triggers
intents = discord.Intents.all()

# Creates a bot with a command prefix
bot = commands.Bot(command_prefix='1', intents=intents)

# Event that prints a message when bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord.")

@bot.event
async def on_message(message):
    # This part is to prevent the bot from responding to itself, that just sounds like a recursive nightmare.
    if message.author == bot.user:
        return
    elif message.content == '!Spellbook':
        with open("spells.txt", "r") as fp:
            open_lines = fp.readlines()
            for lines in open_lines:
                await message.channel.send(lines)
    else:
        await message.channel.send("I cast FUCK YOU")

# Run bot with token
bot.run("MTIxMDMxNjk0NDk5Mzk0NzY3OA.GIZ0hO.l0aef7Z4i3r6MHOmsqy0QCn7p3ok-t7hlwhLBs")