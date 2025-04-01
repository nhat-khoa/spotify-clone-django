from youtubesearchpython import VideosSearch
import yt_dlp
import uuid

def search_youtube(song_name, artist):
    query = f"{song_name} {artist} official audio"
    search = VideosSearch(query, limit=1)
    result = search.result()["result"]
    if result:
        return result[0]["link"]
    return None

def download_audio(youtube_url, output_path="downloads"):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        "outtmpl": f"{output_path}/tracks/{uuid.uuid4()}.%(ext)s",
        "ffmpeg_location" : r"D:\programfile\ffmpeg-2025-03-27-git-114fccc4a5-full_build\bin"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# Ví dụ tìm kiếm và tải bài hát
song_name = "lost control"
artist = "alan walker"
video_url = search_youtube(song_name, artist)

if video_url:
    print(f"Found: {video_url}")
    download_audio(video_url)
else:
    print("Không tìm thấy bài hát trên YouTube.")
