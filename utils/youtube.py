import asyncio
import discord
import yt_dlp as youtube_dl

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.35):
        super().__init__(source, volume=volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def playlist(cls, url):
        videos = []
        ydl_opts = {
            'quiet': True,  # Suppress output messages
            'extract_flat': True,  # Only extract metadata
        }

        # Create a YDL context with options
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"{url}", download=False)

        for entry in result["entries"]:
            videos.append(entry["url"])

        return videos

    @classmethod
    async def get_video_url(cls, url):
        ydl_opts = {
                'quiet': True,  # Suppress output messages
                'extract_flat': True,  # Only extract metadata
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result : dict = ydl.extract_info(f"ytsearch1:{url}", download=False)

        if result["entries"] == []:
            return 1

        return result["entries"][0]["url"]

    @classmethod
    async def video(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
