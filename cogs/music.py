import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogwatch import Watcher

from classes.track import track
from classes.embed_view import embed_view
from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.music.youtube import get_track_from_youtube
from functions.music.play import play_next_track, stop_playing_track, resume_playing_track, pause_playing_track
from embeds.track import track_embed
from embeds.utils import oops_embed
from embeds.queue import queued_tracks_embed, queue_embed


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now_playing: track = None
        self.queue: list[track] = []

    @commands.Cog.listener()
    async def on_ready(self):
        if not discord.opus.is_loaded():
            discord.opus.load_opus(os.environ["OPUS_PATH"])

        watcher = Watcher(self.bot, path='cogs/music.py', preload=True, debug=False)
        await watcher.start()

    @commands.slash_command(guild_ids=gids)
    async def join(self, ctx):
        await join_to_authors_channel(ctx)


    @commands.slash_command(guild_ids=gids)
    async def leave(self, ctx):
        self.now_playing = None
        self.queue = []
        await leave_from_voice_channel(ctx)


    @commands.slash_command(guild_ids=gids)
    async def next(self, ctx):
        self.now_playing = await play_next_track(ctx, queue=self.queue, now_playing=self.now_playing)


    @commands.slash_command(guild_ids=gids)
    async def stop(self, ctx):
        await stop_playing_track(ctx)


    @commands.slash_command(guild_ids=gids)
    async def resume(self, ctx):
        await resume_playing_track(ctx)


    @commands.slash_command(guild_ids=gids)
    async def pause(self, ctx):
        await pause_playing_track(ctx)


    @commands.slash_command(guild_ids=gids)
    async def now(self, ctx):
        if self.now_playing is None:
            await ctx.respond(embed=oops_embed("Now playing is None!"))
            return

        ec = track_embed(self.now_playing)
        await ctx.respond(embed=ec.embed)


    @commands.slash_command(guild_ids=gids)
    async def queue(self, ctx):
        e = queue_embed(self.queue, self.now_playing)
        await ctx.respond(embed=e)


    @commands.slash_command(guild_ids=gids)
    async def play(self, ctx, url: str):
        await ctx.response.defer()
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)

        new_track = await get_track_from_youtube(url)
        self.queue.append(new_track)
        if len(self.queue) != 1:
            await ctx.respond(embed=queued_tracks_embed(new_track))

        if not ctx.voice_client.is_playing():
            self.now_playing = await play_next_track(ctx, self.bot, queue=self.queue, now_playing=self.now_playing)


    @commands.slash_command(guild_ids=gids)
    async def add(self, ctx, url: str):
        await ctx.response.defer()

        new_track = await get_track_from_youtube(url)
        self.queue.append(new_track)
        await ctx.respond(embed=queued_tracks_embed(new_track))


def setup(bot):
    bot.add_cog(music_cog(bot))
