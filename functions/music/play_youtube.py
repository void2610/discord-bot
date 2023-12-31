import os
import uuid

import discord
import yt_dlp
from importlib import reload

import global_variables as g
from functions.join import join_to_authors_channel
from functions.music.play import play_next_music


async def add_youtube_to_queue(ctx, url: str):
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx)
    vc = ctx.voice_client

    filename = f"{uuid.uuid4()}.webm"

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            os.rename("downloaded_audio.webm", f"tmp/music/{filename}")

        g.queue.append(filename)
        print(g.queue)
    except Exception as e:
        await ctx.respond(f"Error: {e}")
        return

    await ctx.respond(f"Added {filename} to queue!")

    if not vc.is_playing():
            await play_next_music(ctx)
