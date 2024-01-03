import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import global_variables as g
from classes.track import track
from classes.embed_view import embed_view
from functions.join import join_to_authors_channel
from functions.leave import leave_from_voice_channel
from functions.music.youtube import get_track_from_youtube
from functions.music.play import play_next_track, stop_playing_track, resume_playing_track, pause_playing_track
from embeds.track import track_embed
from embeds.utils import oops_embed
from embeds.queue import queued_tracks_embed


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
        print("Music ready!")

    @commands.slash_command(guild_ids=gids)
    async def join(self, ctx):
        await join_to_authors_channel(ctx)


    @commands.slash_command(guild_ids=gids)
    async def leave(self, ctx):
        g.now_playing = None
        g.queue = []
        await leave_from_voice_channel(ctx)


    @commands.slash_command(guild_ids=gids)
    async def next(self, ctx):
        await play_next_track(ctx, queue=self.queue, now_playing=self.now_playing)


    @commands.slash_command(guild_ids=gids)
    async def stop(self, ctx):
        await stop_playing_track(ctx, now_playing=self.now_playing)


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
        await ctx.respond(embed=ec.embed, components=ec.components)


    @commands.slash_command(guild_ids=gids)
    async def queue(self, ctx):
        if self.now_playing is None:
            await ctx.respond(embed=oops_embed("Queue is empty!"))
            return

        message = "Now playing:" + self.now_playing.title + "\nQueue:\n"
        if len(self.queue) > 0:
            for i, track in enumerate(self.queue):
                message += f"{i + 1}: {track.title} \n"
        await ctx.respond(message)


    @commands.slash_command(guild_ids=gids)
    async def play(self, ctx, url: str):
        await ctx.response.defer()
        if ctx.voice_client is None:
            await join_to_authors_channel(ctx)

        new_track = await get_track_from_youtube(url)
        self.queue.append(new_track)
        await ctx.respond(embed=queued_tracks_embed(new_track))
        print(self.queue)

        if not ctx.voice_client.is_playing():
            await play_next_track(ctx, queue=self.queue, now_playing=self.now_playing)
            print(self.now_playing)



