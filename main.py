import os

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

# ボットが接続するボイスチャンネルの辞書
connected_channels = {}

@bot.event
async def on_ready():
    pass

@bot.command(name='join')
async def join(ctx):
    # ボイスチャンネルに接続
    if ctx.guild.id not in connected_channels:
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()
        connected_channels[ctx.guild.id] = voice_channel

@bot.command(name='play')
async def play(ctx, url):
    # ボイスチャンネルに接続
    if ctx.guild.id not in connected_channels:
      channel = ctx.author.voice.channel
      voice_channel = await channel.connect()
      connected_channels[ctx.guild.id] = voice_channel

    # YouTubeから音声を再生
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_channel.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))

@bot.command(name='stop')
async def stop(ctx):
    # ボイスチャンネルから切断
    if ctx.guild.id in connected_channels:
        voice_channel = connected_channels[ctx.guild.id]
        voice_channel.stop()
        await voice_channel.disconnect()
        del connected_channels[ctx.guild.id]


token = os.environ["TOKEN"] or ""
bot.run(token)
