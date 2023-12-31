import os

import discord
from dotenv import load_dotenv

from functions.join import join_to_authors_channel


load_dotenv()
bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)


@bot.event
async def on_ready():
    print("Ready!")


@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.slash_command()
async def join(ctx):
    await join_to_authors_channel(ctx)


token = os.environ["TOKEN"] or ""
bot.run(token)
