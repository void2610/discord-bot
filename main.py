import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


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
for filename in os.listdir("tmp/music"):
    os.remove(f"tmp/music/{filename}")

bot = MyBot()

bot.load_extension("cogs.music")
bot.load_extension("cogs.util")

bot.run(os.environ["TOKEN"] or "")
