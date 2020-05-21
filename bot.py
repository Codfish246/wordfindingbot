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

def contains_word(s, w):
    return f' {w} ' in f' {s} '

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

    #if message.content.startswith('!find2')
    if message.content == ('!find2'):
        channel = message.channel

        await channel.send('Send the word you wish to find:')
        def check(m):
            return m.author == message.author and m.channel == channel
        
        wordToFind = await bot.wait_for('message', check=check)

        await channel.send('Send the text you wish to search:')
        def check(m):
            return m.author == message.author and m.channel == channel
        
        textToSearch = await bot.wait_for('message', check=check)


        #async with channel.typing():
        emoji = '\N{THUMBS UP SIGN}'
        await textToSearch.add_reaction(emoji)
        
        if wordToFind.content in textToSearch.content:
            await channel.send('Word ' + wordToFind.content + ' found in text.')
        else:
            await channel.send('Word ' + wordToFind.content + ' not found anywhere in text.')

    if message.content == ('!legacyfind'):
        channel = message.channel
        
        await channel.send('Send the word you wish to find:')
        def check(m):
            return m.author == message.author and m.channel == channel

        wordToFind = await bot.wait_for('message', check=check)
        """try:
            wordToFind = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('*Input timed out!*')
        else:
            await channel.send('Send the text you wish to search:')"""

        ######------------------------------#######

        await channel.send('Send the text you wish to search:')
        def check(m):
            return m.author == message.author and m.channel == channel
        
        textToSearch = await bot.wait_for('message', check=check)
        
        emoji = '\N{THUMBS UP SIGN}'
        await textToSearch.add_reaction(emoji)
        
        #async with channel.typing():
        if (contains_word(textToSearch.content, wordToFind.content)):
            await channel.send('Word ' + wordToFind.content + ' found in text!')
        else:
            await channel.send('Word ' + wordToFind.content + ' not found in text.')
        """try:
            textToSearch = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('*Input timed out!*')
        else:
            async with channel.typing():
                if (contains_word(textToSearch.content, wordToFind.content)):
                    await channel.send('Word ' + wordToFind.content + ' found in text!')
                else:
                    await channel.send('Word ' + wordToFind.content + ' not found in text.')"""


bot.run(TEST_TOKEN) #fishybot for testing 
#bot.run(PROD_TOKEN) #gchq bot