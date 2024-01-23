import random
import os

import discord
from discord import commands
from discord.ext import commands as extcommands
from dotenv import load_dotenv
from openstack import connection

from functions.join import join_to_authors_channel
from functions.utils.twitter import send_vx_twitter
from resource.meigen import meigen


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

auth = {
    'auth_url': os.environ.get('OS_AUTH_URL'),
    'project_name': os.environ.get('OS_TENANT_NAME'),
    'username': os.environ.get('OS_USERNAME'),
    'password': os.environ.get('OS_PASSWORD'),
}

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
        if loop == 1:
            if index > 0:
                try:
                    await ctx.respond(meigen[index - 1])
                except IndexError:
                    await ctx.respond("ぶどう先生の次回作にご期待ください🍇")
            else:
                await ctx.respond(random.choice(meigen))
        else:
            await ctx.respond("🍇")
            for i in range(loop):
                if index > 0:
                    try:
                        await ctx.send(meigen[index - 1])
                    except IndexError:
                        await ctx.send("ぶどう先生の次回作にご期待ください🍇")
                else:
                    await ctx.send(random.choice(meigen))


    @commands.user_command(guild_ids=gids, description="ユーザーのアカウント作成日を表示します")
    async def account_creation_date(self, ctx, member: discord.Member):
        await ctx.respond(f"{member.nick}が生まれ落ちたのは{member.created_at}だよ ( 'ω')")


    @commands.application_command(guild_ids=gids, description="VPSサーバーのステータスを表示します")
    async def vps_status(self, ctx):
        # OpenStackに接続
        conn = connection.Connection(**auth)

        # サーバーのステータスを取得
        server_id = 'vm-3dc818db-b0'
        server = conn.compute.find_server(server_id)

        if server:
            await ctx.respond(f"{server_id} のステータス: **{server.status}**")
        else:
            await ctx.respond(f"{server_id} が見つかりません")


    @commands.application_command(guild_ids=gids, description="VPSサーバーを起動します")
    async def start_vps(self, ctx):
        # OpenStackに接続
        conn = connection.Connection(**auth)

        # サーバーを起動
        server_id = 'vm-3dc818db-b0'
        server = conn.compute.find_server(server_id)
        conn.compute.start_server(server)
        await ctx.respond(f"Starting server {server_id}...")


    @commands.application_command(guild_ids=gids, description="VPSサーバーを再起動します")
    async def reboot_vps(self, ctx):
        # OpenStackに接続
        conn = connection.Connection(**auth)

        # サーバーを再起動
        server_id = 'vm-3dc818db-b0'
        server = conn.compute.find_server(server_id)
        conn.compute.reboot_server(server)
        await ctx.respond(f"Rebooting server {server_id}...")


    @commands.application_command(guild_ids=gids, description="VPSサーバーを停止します")
    async def stop_vps(self, ctx):
        # OpenStackに接続
        conn = connection.Connection(**auth)

        # サーバーを停止
        server_id = 'vm-3dc818db-b0'
        server = conn.compute.find_server(server_id)
        conn.compute.stop_server(server)
        await ctx.respond(f"Stopping server {server_id}...")


def setup(bot):
    bot.add_cog(util_cog(bot))
