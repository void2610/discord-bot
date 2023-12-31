import os

import discord
from dotenv import load_dotenv

import global_variables as g
from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.music.play_youtube import add_youtube_to_queue
from functions.music.play import play_next_music, stop_playing_music, resume_playing_music


load_dotenv()

bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)
gids = os.environ["GUILD_ID"].split(',')

g.now_playing = None
g.queue = []



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
    g.now_playing = None
    g.queue = []
    await leave_from_voice_channel(ctx)


@bot.slash_command(guild_ids=gids)
async def next(ctx):
    await play_next_music(ctx)


@bot.slash_command(guild_ids=gids)
async def stop(ctx):
    await stop_playing_music(ctx)


@bot.slash_command(guild_ids=gids)
async def resume(ctx):
    await resume_playing_music(ctx)


@bot.slash_command(guild_ids=gids)
async def queue(ctx):
    if len(g.queue) > 0:
        await ctx.respond(f"Now playing: {g.now_playing}\nQueue: {g.queue}")
    else:
        await ctx.respond("Queue is empty!")


@bot.slash_command(guild_ids=gids)
async def play(ctx, url: str):
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx)

    await add_youtube_to_queue(ctx, url)

    if not ctx.voice_client.is_playing():
        await play_next_music(ctx)


@bot.slash_command(guild_ids=gids)
async def test(ctx):
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx)
    vc = ctx.voice_client

    source = discord.FFmpegPCMAudio("resource/test.mp3")
    vc.play(source)
    await ctx.respond("Playing test music file!")


@bot.slash_command(guild_ids=gids)
async def akeome(ctx, num: int):
    for i in range(num):
        await ctx.respond("あけおめ ( 'ω')")


token = os.environ["TOKEN"] or ""
bot.run(token)
