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


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    if message.content == ('!find'):
        channel = message.channel

        await channel.send('Send the word you wish to find:')
        def check(m):
            return m.channel == channel and m.author == message.author
        wordToFind = await bot.wait_for('message', check=check)

        await channel.send('Send the text you wish to search:')
        def check(m):
            return m.author == message.author and m.channel == channel
        textToSearch = await bot.wait_for('message', check=check)

        findWordFunct = findWholeWord(wordToFind.content)(textToSearch.content)
        
        emoji = '\N{THUMBS UP SIGN}'
        await textToSearch.add_reaction(emoji)
        
        if (findWordFunct is not None):
            await channel.send('Word ' + wordToFind.content + ' found in text, at text character span: ' +  str(findWordFunct.span()))
        else:
            await channel.send('Word ' + wordToFind.content + ' not found in text.')

        #findWholeWord('seek')('those who seek shall find') #match


bot.run(TEST_TOKEN) #fishybot for testing 
#bot.run(PROD_TOKEN) #gchq bot