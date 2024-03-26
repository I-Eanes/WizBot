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
    elif message.content == '/Spells':
        with open("spells.txt", "r") as spells:
            open_lines = spells.readlines()
            for line in open_lines:
                await message.author.send(line)
    elif message.content == '/info':
        # ui[0] = username, ui[1] = server, ui[2] = lvl, ui[3] = Spell1, ui[4] = Spell2, ui[5] = hp
        ui = data(message)
        spells = find_spell(ui[3]),find_spell(ui[4])
        await message.author.send(f"User: {ui[0]}\nServer: {ui[1]}\nLevel: {ui[2]}\nCurrent HP: {ui[5]}\nSpells: {spells}")
    # else:
    # await message.channel.send("I cast FUCK YOU")

# This code grabs the user's data, as well as their available spells.
def data(message):
    user = message.author
    server = message.guild
    search = f"{user},{server}"
    with open("users.txt", "r") as users:
        all_lines = users.readlines()
        for line in all_lines:
            if search in line:
                print("found")
                user_data = list(line.split(','))
                return user_data
        new_line = f"{user},{server},0,001,007,10"
        print("lost")
    if new_line != "":
        with open("users.txt", "a+") as fp:
            fp.write(f"\n{new_line}")
        user_data = list(new_line.split(','))
        return user_data

def find_spell(id):
    spell_num = id
    with open("spells.txt", "r") as spells:
        all_lines = spells.readlines()
        for line in all_lines:
            if spell_num in line:
                print("found")
                spell_data = list(line.split(','))
                return spell_data

# Run bot with token
bot.run("MTIxMDMxNjk0NDk5Mzk0NzY3OA.GIZ0hO.l0aef7Z4i3r6MHOmsqy0QCn7p3ok-t7hlwhLBs")