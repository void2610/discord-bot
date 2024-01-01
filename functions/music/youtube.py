import os
import uuid

import yt_dlp

from classes.track import track


async def get_track_from_youtube(url: str) -> track:
    filename = f"{uuid.uuid4()}.webm"
    new_track = track(url=url, filename=filename)

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            new_track.title = info_dict.get('title', None)
            new_track.thumbnail_url = info_dict.get('thumbnail', None)
            new_track.uploader = info_dict.get('uploader', None)
            new_track.duration = info_dict.get('duration', None)
            ydl.download([url])
            os.rename("downloaded_audio.webm", f"tmp/music/{filename}")

        print(f"Downloaded {new_track.title}")
        return new_track
    except Exception as e:
        return None
