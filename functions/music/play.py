import discord

import global_variables as g
from classes.track import track
from classes.embed_view import embed_view
from embeds.track import track_embed

async def play_next_track(ctx):
    vc = ctx.voice_client

    if len(g.queue) > 0:
        if vc.is_playing():
            vc.stop()
        g.now_playing = g.queue.pop(0)

        player = discord.FFmpegPCMAudio("tmp/music/" + g.now_playing.filename)
        vc.play(player)

        ev = track_embed(g.now_playing)
        await ctx.respond(embed=ev.embed, view=ev.view)
    else:
        await ctx.respond("Queue is empty!")


async def stop_playing_track(ctx):
    vc = ctx.voice_client

    if vc.is_playing():
        vc.stop()
        await ctx.respond("Stopped playing music!")
    else:
        await ctx.respond("Not playing music!")


async def pause_playing_track(ctx):
    vc = ctx.voice_client

    if vc.is_playing():
        vc.pause()
        await ctx.respond("Paused playing music!")
    else:
        await ctx.respond("Not playing music!")


async def resume_playing_track(ctx):
    vc = ctx.voice_client

    if vc.is_paused():
        vc.resume()
        await ctx.respond("Resumed playing music!")
    else:
        await ctx.respond("Not paused!")
