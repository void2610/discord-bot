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
from embeds.utils import oops_embed
from embeds.queue import queued_tracks_embed


load_dotenv()

bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game("( 'ω')"),)
gids = os.environ["GUILD_ID"].split(',')

g.now_playing: track = None
g.queue: list[track] = []


@bot.slash_command(guild_ids=gids)
async def now(ctx):
    if g.now_playing is None:
        await ctx.respond(embed=oops_embed("Now playing is None!"))
        return

    ec = track_embed(g.now_playing)
    await ctx.respond(embed=ec.embed, components=ec.components)


@bot.slash_command(guild_ids=gids)
async def queue(ctx):
    if g.now_playing is None:
        await ctx.respond(embed=oops_embed("Queue is empty!"))
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
    await ctx.respond(embed=queued_tracks_embed(new_track))

    if not ctx.voice_client.is_playing():
        await play_next_track(ctx)


token = os.environ["TOKEN"] or ""
bot.run(token)
