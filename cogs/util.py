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
            if res is not None:
                await message.channel.send(res)
                await message.delete()


    @commands.application_command(guild_ids=gids, description="テスト用の音声ファイルを再生します")
    async def sound_test(self, ctx):
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)
        vc = ctx.voice_client

        source = discord.FFmpegPCMAudio("resource/test.mp3")
        vc.play(source)
        await ctx.respond("Playing test music file!")


    @commands.application_command(guild_ids=gids, description="あけおめを指定回数送信します")
    async def akeome(self, ctx, num: discord.Option(int, "あけおめの回数") = 1):
        for i in range(num):
            await ctx.respond("あけおめ ( 'ω')")

    @commands.application_command(guild_ids=gids, description="ぶどう先生からのありがたいメッセージを再生します🍇")
    async def budo(self, ctx):
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)

        await ctx.respond("🍇")
        source = discord.FFmpegPCMAudio("resource/lovehotel_BUDO.mp3")
        ctx.voice_client.stop()
        ctx.voice_client.play(source)


    @commands.application_command(guild_ids=gids, description="ぶどう先生から名言を賜ります🍇")
    async def meigen(self, ctx, index: discord.Option(int, "名言の番号") = -1, loop: discord.Option(int, "ループ回数") = 1):
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
