import random
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogwatch import Watcher

from functions.join import join_to_authors_channel
from resource.meigen import meigen


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

    @commands.slash_command(guild_ids=gids)
    async def budo(self, ctx):
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)

        await ctx.respond("🍇")
        source = discord.FFmpegPCMAudio("resource/lovehotel_BUDO.mp3")
        ctx.voice_client.stop()
        ctx.voice_client.play(source)


    @commands.slash_command(guild_ids=gids)
    async def meigen(self, ctx, index: int = -1, loop: int = 1):
        for i in range(loop):
            if index > 0:
                try:
                    await ctx.respond(meigen[index - 1])
                except IndexError:
                    await ctx.respond("ぶどう先生の次回作にご期待ください🍇")
            else:
                await ctx.respond(random.choice(meigen))


def setup(bot):
    bot.add_cog(util_cog(bot))
