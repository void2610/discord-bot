import os

import discord
from dotenv import load_dotenv

from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.play_youtube import play_youtube


load_dotenv()

bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)
gids = os.environ["GUILD_ID"].split(',')


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
        await join_to_authors_channel(ctx)

    await play_youtube(ctx, url)


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
