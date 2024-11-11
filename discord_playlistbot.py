import os
import discord
from discord.ext import commands
import yt_dlp

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Init
intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ftn playlist
def get_playlist_videos(playlist_url):
    ydl_opts = {
        'extract_flat': True,  
        'playlist_items': '1-7' # video limit 
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return [entry['url'] for entry in info['entries']]

# play playlist
@bot.command(name='play')
async def play(ctx, playlist_url):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        vc = await voice_channel.connect()
        videos = get_playlist_videos(playlist_url)

        for video in videos:
            vc.play(discord.FFmpegPCMAudio(video))
            await ctx.send(f"Lecture de : {video}")
            while vc.is_playing():
                await asyncio.sleep(1)  # waiting no music
        await vc.disconnect()
    else:
        await ctx.send("Man, t'es censé être dans le channel vocal pour que ça fonctionne")

@bot.event
async def on_ready():
    print(f"{bot.user.name} la musique a démarré")

# Lancer le bot
bot.run(TOKEN)
