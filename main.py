from dotenv import load_dotenv
import discord
import os
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents, command_prefix = '?')
client.remove_command('help')

idle = None

@client.event
async def on_ready():
  print('I am connected as {0.user}'.format(client))
    
@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def help(ctx):
  help_text = 'This is help text.'
  await ctx.send(help_text)
    
client.run(TOKEN)