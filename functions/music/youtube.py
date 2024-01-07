import os
import uuid

import yt_dlp
from dotenv import load_dotenv
from apiclient.discovery import build

from classes.track import track

load_dotenv()

API_KEY = os.environ["YOUTUBE_API_KEY"] or ""
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

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


async def search_track_id_from_title(title: str) -> str:
    youtube_query = youtube.search().list(
        part='id,snippet',
        q=title,
        type='video',
        maxResults=1,
        order='relevance',
    )

    # execute()で検索を実行
    youtube_response = youtube_query.execute()

    res = youtube_response.get('items', [])
    if len(res) == 0:
        return None
    id = res[0]['id']['videoId']
    print(f"Found video from [{title}]")
    return id

