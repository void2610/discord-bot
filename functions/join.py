async def join_to_authors_channel(ctx):
    if ctx.author.voice is None:
        await ctx.respond("You are not in a voice channel!")
        return

    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.respond("Connected to #" + channel.name + " !")
