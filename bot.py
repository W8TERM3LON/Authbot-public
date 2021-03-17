#bot.py
import discord, os, time, random, logging, asyncio
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

description = '''To authenticate users'''
bot = commands.Bot(command_prefix='~', description=description)
client = discord.Client()
intents = discord.Intents().all()

# Setup basic logging for the bot
logging.basicConfig(level=logging.WARNING)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


#prints bot ID into shell
@client.event
async def on_ready():
    print('I have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Suggestions."))

#kick user
@bot.command(pass_context=True, hidden=True)
async def kicker(message):
    await message.author.kick()

#prints channel name where message was sent to
@client.event
async def on_message(message):
    #prevents a bot message feeding into bot input
    if message.author == client.user:
        return

    print('-------------------------------------------')
    print('A message was sent to ' + str(message.channel) + ', by ' + str(message.author) + ', On ' + str(message.guild))
    print('-------------------------------------------')

    #sends channel name if channel name = verification
    if str(message.channel) == 'verification':
        time.sleep(0.5)
        await message.channel.send('Verification request sent by ' + '**' + str(message.author) + '**' + ' at ' + str(message.created_at) + ' UTC time.')
            #replace @student.school.edu with desired email 
        if '@student.school.edu' in message.content:
            await message.channel.send('Verifying....')
            sleeping = random.randint(1,6)
            print('Waiting ' + str(sleeping) + ' Seconds. (Verified)')
            time.sleep(sleeping)
            await message.author.add_roles(discord.utils.get(message.guild.roles, name='Verified')) #add the role
            time.sleep(0.5)
            await message.channel.send('I just verified: ' + (message.author.mention))

            #replace @student.school.edu with desired email 
        if not '@student.school.edu' in message.content:
            await message.channel.send('Verifying....')
            sleeping = random.randint(1,6)
            print('Waiting ' + str(sleeping) + ' Seconds. (Kicked)')
            time.sleep(sleeping)
            await message.channel.send('---**Unauthorized**---')
            time.sleep(0.7)
            await message.channel.send('Removing ' + (message.author.mention) + ' from server.')
            time.sleep(2)
            await kicker(message)
    if not str(message.channel) == 'verification':
        return


client.run(TOKEN)