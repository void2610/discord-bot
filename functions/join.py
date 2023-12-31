async def join_to_authors_channel(ctx):
    if ctx.author.voice is None:
        await ctx.respond("You are not in a voice channel!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.respond("Moved to #" + channel.name + " !")
        return

    await channel.connect()
    await ctx.respond("Connected to #" + channel.name + " !")
