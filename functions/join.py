from embeds.utils import success_embed, oops_embed


async def join_to_authors_channel(ctx):
    if ctx.author.voice is None:
        await ctx.respond(embed=oops_embed("You are not connected to any voice channel!"))
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.respond(embed=success_embed("Moved to #" + channel.name + " !"))
        return

    await channel.connect()
    await ctx.respond(embed=success_embed("Joined to #" + channel.name + " !"))
