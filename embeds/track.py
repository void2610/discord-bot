import discord
from discord import Embed, Button, ButtonStyle, ActionRow

from classes.embed_view import embed_view


# class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
#     @discord.ui.button(label="pause playing", style=discord.ButtonStyle.primary, emoji="⏸️")
#     async def pause_playing_button_callback(self, button, interaction):
#         await pause_playing_track(interaction)

#     @discord.ui.button(label="next track", style=discord.ButtonStyle.primary, emoji="⏭️")
#     async def next_track_button_callback(self, button, interaction):
#         await play_next_track(interaction)


def track_embed(track) -> embed_view:
    embed = Embed(
        title="Now Playing",
        description="",
        color=0x6fff00,
        url= track.url
    )
    embed.set_thumbnail(url= track.thumbnail_url)
    embed.add_field(name= track.title, value=track.uploader, inline=False)

    return embed_view(embed=embed)

