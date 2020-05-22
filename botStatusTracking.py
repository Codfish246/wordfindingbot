#Made by Codfish246

import discord
import asyncio
from datetime import datetime
import re
import os
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
    
    await bot.change_presence(activity=discord.Game(name='!help'))

def contains_word(s, w):
    return f' {w} ' in f' {s} '

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

global userToCheck
global statusTrackChannel
#nonlocal userToCheck
#nonlocal statusTrackChannel
userToCheck = 0
statusTrackChannel = 0

@bot.event
async def on_message(message):
    global userToCheck
    global statusTrackChannel
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
        
        #mainly for reference purposes now, hence being called legacy search
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
        embed.add_field(name="Find section", value='-',inline=False)
        embed.add_field(name="!find", value="Main word finding command", inline=True)
        embed.add_field(name="!find2", value="Different word finding method, includes words inside other words, like 'word' in 'swordsmith'.", inline=True)
        embed.add_field(name="!legacyfind", value="Old version of the main word finding command.", inline=True)
        embed.add_field(name="User status tracking section", value='-', inline=False)
        embed.add_field(name="!trackuser", value="Sets a user id for tracking a user's status and sending an update when it changes.", inline=True)
        embed.add_field(name="!untrackuser", value="Untracks a user set by !trackuser", inline=True)
        embed.add_field(name="!trackingset", value="Shows the currently set user and logging channel.", inline=True)
        embed.set_footer(text="Sent " + dt_string)
        await channel.send(embed=embed)


    if message.content == ('!shutdown') and message.author.id == 102341036403068928:
        emoji = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)
        await bot.close()


    if message.content == ('!trackuser'):
        channel = message.channel
        await channel.send('Send user\'s id to track:')
        def check(m):
            return m.author == message.author and m.channel == channel
        userToCheckMsg = await bot.wait_for('message', check=check)
        """emoji = 'backslashN{THUMBS UP SIGN}'
        await userToCheckMsg.add_reaction(emoji)"""
        userToCheck = int(userToCheckMsg.content)

        changeChannelSet = False
        if statusTrackChannel != 0:
            trackuserFormatString = ('Channel id currently set to <#{0}> ({0}), Do you want to change it? React:').format(statusTrackChannel)
            await channel.send(trackuserFormatString)
            emojiYes = '\N{THUMBS UP SIGN}'
            emojiNo = '\N{THUMBS DOWN SIGN}'
            await message.add_reaction(emojiYes)
            await message.add_reaction(emojiNo)

            def check(reaction, user):
                return user == message.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('Timed out.')
            else:
                if str(reaction.emoji) == '👍':
                    changeChannelSet = True
                elif str(reaction.emoji) == '👎':
                    changeChannelSet = False

        if changeChannelSet == True:
            await channel.send('Send channel id to post tracking status updates in:')
            def check(m):
                return m.author == message.author and m.channel == channel
            statusTrackChannelMsg = await bot.wait_for('message', check=check)
            """emoji = 'backslashN{THUMBS UP SIGN}'
            await userToCheckMsg.add_reaction(emoji)"""
            statusTrackChannel = int(statusTrackChannelMsg.content)
            await channel.send('User id and channel id set and tracking started.')
        elif changeChannelSet == False and statusTrackChannel != 0 and userToCheck != 0:
            await channel.send('User id and channel id set and tracking started.')
        else:
            await channel.send('Error: probably something wrong with channel or user id, like it\'s not set or something.')

    if message.content == ('!untrackuser'):
        channel = message.channel
        """emoji = 'backslashN{THUMBS UP SIGN}'
        await message.add_reaction(emoji)"""

        userToCheck = 0
        #statusTrackChannel = 0;
        #await channel.send('User id and channel id unset and tracking stopped.')
        await channel.send('User id unset and tracking stopped.')


    if message.content == ('!trackingset'):
        channel = message.channel
        if userToCheck != 0:
            fetchedUser = await bot.fetch_user(userToCheck)
            trackingsetFormatString = ('User ID set is: {0}, aka: {1}/<@{0}> \nChannel ID set is: {2}, aka: <#{2}>').format(userToCheck, fetchedUser.name, statusTrackChannel)
            await channel.send(trackingsetFormatString)
        else:
            await channel.send('Error: User or channel (ID) is not set')



@bot.event
async def on_member_update(memberBefore, memberAfter):
    global userToCheck
    global statusTrackChannel
    if memberBefore.id == bot.user.id or userToCheck == 0:
        return


bot.run(TEST_TOKEN) #fishybot for testing 
#bot.run(PROD_TOKEN) #gchq bot