import csv
from itertools import islice
import uuid
import os
import yt_dlp
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.artists.models import Artist
from apps.tracks.models import Track
from apps.albums.models import Album

MEDIA_ROOT = "media/"
start_line = 48
end_line = 49  
file_path = r"D:\User\workspace\ProjectsOnSchool\spotify-clone-data\spotify_songs.csv\spotify_songs.csv" # url đến file csv
ffmpeg_location = r"D:\programfile\ffmpeg-2025-03-27-git-114fccc4a5-full_build\bin" 
# đường dẫn đến ffmpeg.exe, chưa có thì tải về từ https://ffmpeg.org/download.html 
# và giải nén vào thư mục nào đó, sau đó chỉ cần chỉ đường dẫn đến ffmpeg.exe là được



class Command(BaseCommand):
    help = "Import tracks from a CSV file and fetch audio files from YouTube"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("file_path", type=str, help="Path to the CSV file", default=r"D:\User\workspace\ProjectsOnSchool\spotify-clone-data\spotify_songs.csv\spotify_songs.csv")

    def handle(self, *args, **kwargs):
        self.import_tracks(file_path)

    def import_tracks(self, file_path):
        
        
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in islice(reader, start_line, end_line):
                
                track_id = row["track_id"].strip()
                track_name = row["track_name"].strip()
                artist_name = row["track_artist"].strip()
                duration = int(row.get("duration_ms", 0))  # Convert ms to seconds
                popularity = int(row.get("track_popularity", 0))
                album_id = row.get("track_album_id", "").strip() or None
                album_name = row.get("track_album_name", "").strip() or None
                is_instrumental = False  # 1 = instrumental
                language = row.get("language", "").strip() or None
                plain_lyrics = row.get("lyrics", "").strip() or None
                source = "imported_from_csv"
                

                # Kiểm tra và tạo nghệ sĩ
                artist, created = Artist.objects.get_or_create(
                    name=artist_name,
                    defaults={"user": self.create_random_user(artist_name)}
                )
                
                # Kiểm tra và tạo album (nếu có album_name)
                album = None
                if album_name:
                    album = Album.objects.create(
                        artist=artist,
                        title=album_name or "Unknown Album",
                    )   

                # Đặt đường dẫn file nhạc
                audio_file_path = f"tracks/{str(uuid.uuid4())}"
                audio_file_path2 = audio_file_path + ".mp3"

                # Tạo model Track
                track = Track.objects.create(
                    artist=artist,
                    album=album,
                    title=track_name,
                    duration_ms=duration,
                    popularity=popularity,
                    is_instrumental=is_instrumental,
                    language=language,
                    plain_lyrics=plain_lyrics,
                    source=source,
                    audio_file_path=audio_file_path2
                )

                # Tải file nhạc từ YouTube
                self.download_track(track_name, artist_name, audio_file_path)

    def create_random_user(self, artist_name):
        """Tạo user ngẫu nhiên nếu nghệ sĩ chưa có tài khoản."""
        random_email = f"{artist_name}{uuid.uuid4().hex[:8]}@example.com"
        user = User.objects.create(email=random_email, full_name=artist_name, username=random_email)
        user.set_password("123456")  # Đặt mật khẩu mặc định
        user.save()
        return user

    def download_track(self, track_name, artist_name, file_path):
        """Tìm kiếm trên YouTube và tải file MP3 về"""
        search_query = f"{track_name} {artist_name} audio"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(MEDIA_ROOT, file_path),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            "ffmpeg_location" : ffmpeg_location
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                search_results = ydl.extract_info(f"ytsearch:{search_query}", download=False)
                video_url = search_results["entries"][0]["webpage_url"]
                ydl.download([video_url])
                print(f"Downloaded: {file_path}")
            except Exception as e:
                print(f"Failed to download {track_name} - {artist_name}: {e}")
