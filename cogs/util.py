import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogwatch import Watcher

from functions.join import join_to_authors_channel


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

class util_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_ready(self):
        watcher = Watcher(self.bot, path='cogs/util.py', preload=True, debug=False)
        await watcher.start()


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if "twitter.com" in message.content or "x.com" in message.content:
            await message.add_reaction("🐦")
            query = message.content.split(".com/")[-1]
            await message.channel.send("https://vxtwitter.com/" + query)


    @commands.slash_command(guild_ids=gids)
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author

        if self._last_member is None or self._last_member.id != member.id:
            await ctx.respond(f'Hello {member.name}~')
        else:
            await ctx.respond(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


    @commands.slash_command(guild_ids=gids)
    async def test(self, ctx):
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)
        vc = ctx.voice_client

        source = discord.FFmpegPCMAudio("resource/test.mp3")
        vc.play(source)
        await ctx.respond("Playing test music file!")


    @commands.slash_command(guild_ids=gids)
    async def akeome(self, ctx, num: int):
        for i in range(num):
            await ctx.respond("あけおめ ( 'ω')")


def setup(bot):
    bot.add_cog(util_cog(bot))
