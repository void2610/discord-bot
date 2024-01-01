from embeds.utils import oops_embed

async def leave_from_voice_channel(ctx):
    if ctx.voice_client is None:
        await ctx.respond(embed=oops_embed("Not in a voice channel!"))
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.respond("Left voice channel.")
