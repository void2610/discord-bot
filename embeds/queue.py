from discord import Embed


def queued_tracks_embed(track) -> Embed:
    embed = Embed(
        title="Queued",
        description="",
        color=0x6fff00,
        url=track.url
    )
    embed.add_field(name=track.title, value=track.uploader, inline=False)

    return embed


def queue_embed(queue, now_playing) -> Embed:
    embed = Embed(
        title="Queue",
        description="",
        color=0x6fff00,
    )
    if now_playing is not None:
        embed.add_field(name="Now Playing", value=now_playing.title, inline=False)
    if len(queue) > 0:
        for i, track in enumerate(queue):
            embed.add_field(name=f"{i + 1}: {track.title}", value=track.uploader, inline=False)
    else:
        embed.add_field(name="Queue is empty!", value="Add some tracks!", inline=False)

    return embed
