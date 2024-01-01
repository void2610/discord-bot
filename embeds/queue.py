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
