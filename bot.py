import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.util import util_cog
from cogs.music import music_cog


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        guild_ids = os.environ["GUILD_ID"].split(',')
        await self.tree.sync(guild=None)
        for g in guild_ids:
            try:
                await self.tree.sync(guild=g)
            except discord.errors.Forbidden:
                print(f"Guild {g} is not found.")


load_dotenv()
token = os.environ["TOKEN"] or ""
bot = MyBot()

bot.add_cog(util_cog(bot))
bot.add_cog(music_cog(bot))

bot.run(token)
