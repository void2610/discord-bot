import os

import discord
from dotenv import load_dotenv

import global_variables as g
from classes.track import track
from classes.embed_view import embed_view
from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.music.youtube import get_track_from_youtube
from functions.music.play import play_next_track, stop_playing_track, resume_playing_track, pause_playing_track
from embeds.track import track_embed


load_dotenv()

bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)
gids = os.environ["GUILD_ID"].split(',')

g.now_playing: track = None
g.queue: list[track] = []


@bot.event
async def on_ready():
    if not discord.opus.is_loaded():
        discord.opus.load_opus(os.environ["OPUS_PATH"])
    print("Ready!")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if "twitter.com" in message.content or "x.com" in message.content:
        await message.add_reaction("🐦")
        query = message.content.split(".com/")[-1]
        await message.channel.send("https://vxtwitter.com/" + query)


@bot.slash_command(guild_ids=gids)
async def join(ctx):
    await join_to_authors_channel(ctx)


@bot.slash_command(guild_ids=gids)
async def leave(ctx):
    g.now_playing = None
    g.queue = []
    await leave_from_voice_channel(ctx)


@bot.slash_command(guild_ids=gids)
async def now(ctx):
    if g.now_playing is None:
        embed = discord.Embed(title="Oops!",description="Now playing is None!",color=discord.Colour.red())
        await ctx.respond(embed=embed)
        return

    ec = track_embed(g.now_playing)
    await ctx.respond(embed=ec.embed, components=ec.components)


@bot.slash_command(guild_ids=gids)
async def next(ctx):
    await play_next_track(ctx)


@bot.slash_command(guild_ids=gids)
async def stop(ctx):
    await stop_playing_track(ctx)


@bot.slash_command(guild_ids=gids)
async def resume(ctx):
    await resume_playing_track(ctx)


@bot.slash_command(guild_ids=gids)
async def pause(ctx):
    await pause_playing_track(ctx)


@bot.slash_command(guild_ids=gids)
async def queue(ctx):
    if g.now_playing is None:
        embed = discord.Embed(title="Oops!",description="Queue is empty!",color=discord.Colour.red())
        await ctx.respond(embed=embed)
        return

    message = "Now playing:" + g.now_playing.title + "\nQueue:\n"
    if len(g.queue) > 0:
        for i, track in enumerate(g.queue):
            message += f"{i + 1}: {track.title}"
    await ctx.respond(message)


@bot.slash_command(guild_ids=gids)
async def play(ctx, url: str):
    await ctx.response.defer()
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx)

    new_track = await get_track_from_youtube(url)
    g.queue.append(new_track)
    await ctx.respond(f"Queued {new_track.title}!")

    if not ctx.voice_client.is_playing():
        await play_next_track(ctx)


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
