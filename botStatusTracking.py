"""
discord.on_member_update(before, after)
Called when a Member updates their profile.

This is called when one or more of the following things change:

status

activity

nickname

roles
"""

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
    
    await client.change_presence(activity=discord.Game(name='!help'))

def contains_word(s, w):
    return f' {w} ' in f' {s} '

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

userToCheck = 0


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
        

    if message.content.startswith('!help'):
        channel = message.channel
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        embed=discord.Embed(title="Help", description="Commands", color=0x191919)
        #embed=discord.Embed(title="Help", description="Commands\n(All time out in 60 secs)", color=0x191919)
        embed.set_author(name="GCHQ", icon_url="https://pbs.twimg.com/profile_images/1216637466440097792/6OmvLk7Y_400x400.jpg")
        embed.add_field(name="Find section", value="", inline=False)
        embed.add_field(name="!find", value="Main word finding command", inline=True)
        embed.add_field(name="!find2", value="Different word finding method, includes words inside other words, like 'word' in 'swordsmith'.", inline=True)
        embed.add_field(name="!legacyfind", value="Old version of the main word finding command.", inline=True)
        embed.add_field(name="User status tracking section", value="", inline=False)
        embed.add_field(name="!trackuser", value="Sets a user id for tracking a user's status and sending an update when it changes.", inline=True)
        embed.add_field(name="!untrackuser", value="Untracks a user set by !trackuser", inline=True)
        embed.add_field(name="!userset", value="Shows the currently set user.", inline=True)
        embed.set_footer(text="Sent " + dt_string)
        await channel.send(embed=embed)

    if message.content == ('!shutdown') and message.author.id == 102341036403068928:
        emoji = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)
        await bot.close()

    if message.content == ('!trackuser')
    	channel = message.channel
    	await channel.send('Send user\'s id to track:')
        def check(m):
            return m.author == message.author and m.channel == channel

        userToCheckMsg = await bot.wait_for('message', check=check)
        """emoji = '\N{THUMBS UP SIGN}'
        await userToCheckMsg.add_reaction(emoji)"""
        userToCheck = userToCheckMsg.content
        await channel.send('User id set and tracking started.')

    if message.content == ('!untrackuser')
    	channel = message.channel
        """emoji = '\N{THUMBS UP SIGN}'
        await userToCheckMsg.add_reaction(emoji)"""
        userToCheck = 0
        await channel.send('User id unset and tracking stopped.')

    if message.content == ('!userset')
    	channel = message.channel
    	if userToCheck != 0:
    		fetchedUser = await bot.fetch_user(userToCheck)
    		await channel.send('User id set is: ' + userToCheck + ', aka: ' + fetchedUser.name)
    	else:
    		await channel.send('Error: User (ID) is not set')
        


    	


@bot.event
async def on_member_update(memberBefore, memberAfter):
	if memberBefore.id == bot.user.id or memberAfter == bot.user.id or userToCheck == 0:
		return





bot.run(TEST_TOKEN) #fishybot for testing 
#bot.run(PROD_TOKEN) #gchq bot