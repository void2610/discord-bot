import discord
from discord import Embed

from classes.embed_view import embed_view


def success_embed(description: str) -> Embed:
    embed = Embed(
        title="Success!",
        description=description,
        color=discord.Colour.green()
    )

    return embed


def oops_embed(description: str) -> Embed:
    embed = Embed(
        title="Oops!",
        description=description,
        color=discord.Colour.red()
    )

    return embed
