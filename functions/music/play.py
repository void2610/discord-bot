import discord

import global_variables as g

async def play_next_music(ctx):
    vc = ctx.voice_client

    if len(g.queue) > 0:
        if vc.is_playing():
            vc.stop()
        g.now_playing = g.queue.pop(0)

        player = discord.FFmpegPCMAudio("tmp/music/" + g.now_playing)
        vc.play(player)

        await ctx.respond(f"Playing {g.now_playing}!")
    else:
        await ctx.respond("Queue is empty!")
