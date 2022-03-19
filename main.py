from dotenv import load_dotenv
import discord
import os
from discord.ext import commands
import random
from audio_dict import audio

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True

activity = discord.Activity(type=discord.ActivityType.watching, name='?help')
bot = commands.Bot(intents=intents, command_prefix = '?', help_command=None, activity=activity)

@bot.event
async def on_ready():
  print('I am connected as {0.user}'.format(bot))

@bot.event
async def on_message(message):
  if message.content == "who is good":
    await message.channel.send(random.choice(message.channel.members))
    
@bot.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def help(ctx):
  help_text = 'This is help text.'
  await ctx.send(help_text)
    
bot.run(TOKEN)