import discord
from discord import Embed


class embed_view:
    def __init__(self, embed: Embed = None, view: discord.ui.View = None):
        self.embed = embed
        self.view = view
