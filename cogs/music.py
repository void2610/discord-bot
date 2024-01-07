import os

import discord
from discord import commands
from discord.ext import commands as extcommands
from dotenv import load_dotenv

from classes.track import track
from classes.embed_view import embed_view
from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.music.youtube import get_track_from_youtube, search_track_id_from_title
from functions.music.play import play_next_track, stop_playing_track, resume_playing_track, pause_playing_track
from embeds.track import track_embed
from embeds.utils import oops_embed
from embeds.queue import queued_tracks_embed, queue_embed


load_dotenv()
gids = os.environ["GUILD_ID"].split(',')

class music_cog(extcommands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now_playing: track = None
        self.queue: list[track] = []

    @extcommands.Cog.listener()
    async def on_ready(self):
        if not discord.opus.is_loaded():
            discord.opus.load_opus(os.environ["OPUS_PATH"])
        print("music_cog is ready.")

    @commands.application_command(guild_ids=gids)
    async def join(self, ctx):
        await join_to_authors_channel(ctx)


    @commands.application_command(guild_ids=gids)
    async def leave(self, ctx):
        self.now_playing = None
        self.queue = []
        await leave_from_voice_channel(ctx)


    @commands.application_command(guild_ids=gids)
    async def next(self, ctx):
        self.now_playing = await play_next_track(ctx, self.bot, queue=self.queue, now_playing=self.now_playing)


    @commands.application_command(guild_ids=gids)
    async def stop(self, ctx):
        await stop_playing_track(ctx)


    @commands.application_command(guild_ids=gids)
    async def resume(self, ctx):
        await resume_playing_track(ctx)


    @commands.application_command(guild_ids=gids)
    async def pause(self, ctx):
        await pause_playing_track(ctx)


    @commands.application_command(guild_ids=gids)
    async def now(self, ctx):
        if self.now_playing is None:
            await ctx.respond(embed=oops_embed("Now playing is None!"))
            return

        ec = track_embed(self.now_playing)
        await ctx.respond(embed=ec.embed)


    @commands.application_command(guild_ids=gids)
    async def queue(self, ctx):
        e = queue_embed(self.queue, self.now_playing)
        await ctx.respond(embed=e)


    @commands.application_command(guild_ids=gids)
    async def play(self, ctx, url: str):
        if not ctx.response.is_done():
            await ctx.response.defer()
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)

        new_track = await get_track_from_youtube(url)
        self.queue.append(new_track)
        if len(self.queue) != 1 or ctx.voice_client.is_playing():
            await ctx.respond(embed=queued_tracks_embed(new_track))

        if not ctx.voice_client.is_playing():
            self.now_playing = await play_next_track(ctx, self.bot, queue=self.queue, now_playing=self.now_playing)


    @commands.application_command(guild_ids=gids)
    async def add(self, ctx, url: str):
        await ctx.response.defer()

        new_track = await get_track_from_youtube(url)
        self.queue.append(new_track)
        await ctx.respond(embed=queued_tracks_embed(new_track))


    @commands.application_command(guild_ids=gids)
    async def search(self, ctx, query: str):
        await ctx.response.defer()

        id = await search_track_id_from_title(query)
        if id is None:
            await ctx.respond(embed=oops_embed("No tracks found!"))
            return

        url = f"https://www.youtube.com/watch?v={id}"
        await self.play(ctx, url)


def setup(bot):
    bot.add_cog(music_cog(bot))
