async def leave_from_voice_channel(ctx):
    if ctx.voice_client is None:
        await ctx.respond("I'm not in a voice channel!")
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.respond("Left voice channel.")
