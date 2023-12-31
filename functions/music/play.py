import discord

async def play_next_music(ctx, queue: list[str], now_playing: str):
    vc = ctx.voice_client

    if len(queue) > 0:
        if vc.is_playing():
            vc.stop()
        now_playing = queue.pop(0)
        await ctx.respond(f"Playing {now_playing}!")
        player = discord.FFmpegPCMAudio("tmp/music/" + now_playing)
        vc.play(player)

    else:
        await ctx.respond("Queue is empty!")
