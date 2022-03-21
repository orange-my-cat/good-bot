from dotenv import load_dotenv
import os
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

from audio_dict import audio_list


load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True

activity = discord.Activity(type=discord.ActivityType.watching, name='?help')
bot = commands.Bot(intents=intents, command_prefix = '?', help_command=None, activity=activity)

bot.lavalink_nodes = [{"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"}]

@bot.event
async def on_ready():
  print('I am connected as {0.user}'.format(bot))

@bot.event
async def on_message(message):
  if message.content.lower().startswith('who') and len(message.content.split(' ')) >= 2:
    user_tag = '<@' + str(random.choice([member.id for member in message.channel.members if member.bot == False])) + '>'
    is_what = ' '.join(message.content.split(' ')[1:])
    await message.channel.send(user_tag + is_what)

  await bot.process_commands(message)
    
@bot.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def help(ctx):
  help_text = 'This is help text.'
  await ctx.send(help_text)

@bot.command()
async def say(ctx, audio):
  if (ctx.author.voice) and (audio in audio_list):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None:
      voice_client = await voice.connect()
    else:
      await voice_client.move_to(channel)

    voice_client.play(FFmpegPCMAudio('./audio/' + audio_list[audio]))

  elif audio not in audio_list:
    await ctx.send('Sound has not been added.')
  else:
    await ctx.send('Please join a channel.')

bot.load_extension('dismusic')
    
bot.run(TOKEN)