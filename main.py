import os
import replit
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
  print(f'SYSTEMS GOING ONLINE...')
  for guild in bot.guilds:
    if guild.name == GUILD:
      break

  print(
    f'SUCCESS!\n'
    f'SERVER_NAME: {guild.name}\n'
    f'SERVER_ID: {guild.id}'
    )

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3].upper()} EXTENSION ADDED!')

replit.replit()
bot.run(TOKEN)