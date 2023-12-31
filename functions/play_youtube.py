import os
import uuid

import discord
import yt_dlp

from functions.join import join_to_authors_channel

async def play_youtube(ctx, url: str):
    if ctx.voice_client is None:
        await join_to_authors_channel(ctx)

    filename = f"{uuid.uuid4()}.webm"

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            os.rename("downloaded_audio.webm", f"music/{filename}")
        player = discord.FFmpegPCMAudio("music/" + filename)
        ctx.voice_client.play(player)
    except Exception as e:
        await ctx.respond(f"Error: {e}")
        return

    await ctx.respond("Playing!")
