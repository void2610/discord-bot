import discord

import global_variables as g
from classes.track import track
from classes.embed_view import embed_view
from embeds.track import track_embed
from embeds.utils import oops_embed

async def play_next_track(ctx, queue: list[track], now_playing: track):
    vc = ctx.voice_client

    if len(queue) > 0:
        if vc.is_playing():
            vc.stop()
        now_playing = queue.pop(0)

        player = discord.FFmpegPCMAudio("tmp/music/" + now_playing.filename)
        vc.play(player)

        ev = track_embed(now_playing)
        await ctx.respond(embed=ev.embed)
    else:
        await ctx.respond(embed=oops_embed("Queue is empty!"))


async def stop_playing_track(ctx, now_playing: track):
    vc = ctx.voice_client

    if vc.is_playing():
        vc.stop()
        now_playing = None
        await ctx.respond("Stopped playing music!")
    else:
        await ctx.respond(embed=oops_embed("Not playing music!"))


async def pause_playing_track(ctx):
    vc = ctx.voice_client

    if vc.is_playing():
        vc.pause()
        await ctx.respond("Paused playing music!")
    else:
        await ctx.respond(embed=oops_embed("Not playing music!"))


async def resume_playing_track(ctx):
    vc = ctx.voice_client

    if vc.is_paused():
        vc.resume()
        await ctx.respond("Resumed playing music!")
    else:
        await ctx.respond(embed=oops_embed("Not paused!"))
