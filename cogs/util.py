import random
import os

import discord
from discord import commands
from discord.ext import commands as extcommands
from dotenv import load_dotenv

from functions.join import join_to_authors_channel
from functions.utils.twitter import send_vx_twitter
from resource.meigen import meigen


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

class util_cog(extcommands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @extcommands.Cog.listener()
    async def on_ready(self):
        print("util_cog is ready.")

    @extcommands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if "twitter.com" in message.content or "x.com" in message.content:
            res = send_vx_twitter(message)
            await message.channel.send(res)
            await message.delete()


    @commands.application_command(guild_ids=gids)
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author

        if self._last_member is None or self._last_member.id != member.id:
            await ctx.respond(f'Hello {member.name}~')
        else:
            await ctx.respond(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


    @commands.application_command(guild_ids=gids)
    async def sound_test(self, ctx):
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)
        vc = ctx.voice_client

        source = discord.FFmpegPCMAudio("resource/test.mp3")
        vc.play(source)
        await ctx.respond("Playing test music file!")


    @commands.application_command(guild_ids=gids)
    async def akeome(self, ctx, num: int):
        for i in range(num):
            await ctx.respond("あけおめ ( 'ω')")

    @commands.application_command(guild_ids=gids)
    async def budo(self, ctx):
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)

        await ctx.respond("🍇")
        source = discord.FFmpegPCMAudio("resource/lovehotel_BUDO.mp3")
        ctx.voice_client.stop()
        ctx.voice_client.play(source)


    @commands.application_command(guild_ids=gids)
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
