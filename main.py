import os

import discord
from dotenv import load_dotenv

from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.play_youtube import play_youtube


load_dotenv()
bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)

gids = [int(os.environ["GUILD_ID"])]

@bot.event
async def on_ready():
    print("Ready!")


@bot.slash_command(guild_ids=gids)
async def ping(ctx):
    await ctx.respond(ctx.guild_id)


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

    play_youtube(ctx, url)


token = os.environ["TOKEN"] or ""
bot.run(token)
