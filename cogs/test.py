import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

class test_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_ready(self):
        print('test_cog ready')

    @commands.hybrid_command(guild_ids=gids)
    async def test(self, ctx):
        await ctx.respond("test")


def setup(bot):
    bot.add_cog(test_cog(bot))
