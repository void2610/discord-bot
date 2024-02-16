import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.music import music_cog
from cogs.util import util_cog
from cogs.test import test_cog
from auto_access import start_schedule_access


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        guild_ids = os.environ["GUILD_ID"].split(",")
        await self.tree.sync(guild=None)
        for g in guild_ids:
            try:
                await self.tree.sync(guild=g)
            except discord.errors.Forbidden:
                print(f"Guild {g} is not found.")


load_dotenv()

directory = "tmp/music"
if os.path.exists(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

bot = MyBot()

bot.add_cog(util_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(test_cog(bot))

bot.loop.create_task(start_schedule_access())
bot.run(os.environ["TOKEN"] or "")
