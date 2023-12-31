import os

import discord
from dotenv import load_dotenv

from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.music.play_youtube import add_youtube_to_queue
from functions.music.play import play_next_music


load_dotenv()

bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)
gids = os.environ["GUILD_ID"].split(',')

now_playing = None
queue = []


@bot.event
async def on_ready():
    if not discord.opus.is_loaded():
        discord.opus.load_opus(os.environ["OPUS_PATH"])
    print("Ready!")


@bot.slash_command(guild_ids=gids)
async def join(ctx):
    await join_to_authors_channel(ctx)


@bot.slash_command(guild_ids=gids)
async def leave(ctx):
    await leave_from_voice_channel(ctx)


@bot.slash_command(guild_ids=gids)
async def play(ctx, url: str):
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx,)

    await add_youtube_to_queue(ctx, url, queue)
    await play_next_music(ctx, queue, now_playing)


@bot.slash_command(guild_ids=gids)
async def test(ctx):
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx)
    vc = ctx.voice_client

    source = discord.FFmpegPCMAudio("resource/test.mp3")
    vc.play(source)
    await ctx.respond("Playing test music file!")


token = os.environ["TOKEN"] or ""
bot.run(token)
