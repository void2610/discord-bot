import os

import discord
from discord import commands
from discord.ext import commands as extcommands
from dotenv import load_dotenv


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

class test_cog(extcommands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @extcommands.Cog.listener()
    async def on_ready(self):
        print('test_cog ready')

    @commands.application_command(guild_ids=gids)
    async def test(self, ctx):
        await ctx.respond("test")


def setup(bot):
    bot.add_cog(test_cog(bot))
