import discord
import asyncio
from datetime import datetime
import re
from os import getenv
from dotenv import load_dotenv

load_dotenv()
TEST_TOKEN = os.getenv('TEST_DISCORD_TOKEN')
PROD_TOKEN = os.getenv('PROD_DISCORD_TOKEN')

bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    emoji = '\N{ROBOT FACE}'
    activity = discord.Activity(name='!help', emoji=emoji, type=discord.ActivityType.custom)
    await bot.change_presence(activity=activity)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return



bot.run(TEST_TOKEN) #fishybot for testing 
#bot.run(PROD_TOKEN) #gchq bot