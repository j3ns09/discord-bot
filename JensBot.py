import os
import asyncio
import discord
from discord.ext import commands
from random import randint, choice
import yt_dlp as youtube_dl

from dotenv import load_dotenv

load_dotenv("t.env")

TOKEN : str = os.getenv("DISCORD_TOKEN")
GUILD : discord.Guild = os.getenv("DISCORD_GUILD")

PREFIX = "&lex "


intents = discord.Intents.all()

bot : commands.Bot = commands.Bot(command_prefix=PREFIX, intents=intents)

'''
Le bot peut effectuer ces commandes spéciales avec le préfixe _flih

Le bot répond aux messages contenant "juif" et "arabe"

'''

@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected and ready !")

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "test-bot":
                await channel.send("bot connecté")
                # \nhttps://tenor.com/view/the-deep-the-boys-gif-26305579

# === MUSIC ===

# Options pour youtube-dl
youtube_dl.utils.bug_reports_message = lambda: ''
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
    'options': '-vn' # --lazy-playlist
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.35):
        super().__init__(source, volume=volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url: str, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        
        if url.startswith("https://www.youtube.com/playlist"):
            stream = True

        if 'entries' in data:
            data = data["entries"][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)
        return cls(audio_source, data=data)


queue = []

@bot.command(help="Permet au bot de rejoindre un chat vocal.")
async def viens(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("tu dois être en voc pour m'appeler connard")

@bot.command(help="Permet de jouer une musique dans un chat vocal")
async def joue_url(ctx, url):
    if ctx.author.voice:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Erreur: {e}') if e else None)
            
        await ctx.send(f"Playing {player.title}") 
    else:
        await ctx.send("tu dois être en voc pour m'appeler connard")

@bot.command(help="Permet de jouer une musique dans un chat vocal en entrant le titre")
async def joue_search(ctx, *title):
    ydl_opts = {
        'quiet': True,  # Suppress output messages
        'extract_flat': True,  # Only extract metadata
    }
    
    query = " ".join(title)
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=False)

    if result["entries"] == []:
        await ctx.send("Résultats non trouvés")

    await joue_url(ctx, result["entries"][0]["url"])


def play_next(ctx):
    if queue:  # Vérifie si la file d'attente n'est pas vide
        next_song = queue.pop(0)  # Récupère le prochain morceau
        ctx.voice_client.play(next_song, after=lambda e: play_next(ctx))
    else:
        asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), bot.loop)
    

@bot.command(help="Permet de jouer une musique dans un chat vocal")
async def joue_playlist(ctx, url):
    if ctx.author.voice:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
        async with ctx.typing():
            try:
                songs = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
                for song in songs:
                    queue.append(song)
                
                if not ctx.voice_client.is_playing():
                    play_next(ctx)
                    
                await ctx.send(f"Ajouté {len(songs)} chanson(s) à la file d'attente.")
            except Exception as e:
                await ctx.send("Une erreur est survenue lors de la lecture de la musique.")
                print(f'Erreur lors de la lecture de la musique : {e}')

@bot.command(help="Fait quitter le bot du chat vocal")
async def sors(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()

@bot.command(help="Arrête de jouer la musique en cours")
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()


# === USELESS ===

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    text : str = message.content

    if "juif" in text:
        response = "c'est moi qui vait te déporter si tu continues avec ça"
        await message.channel.send(response)
        return

    if "arabe" in text:
        response = "toujours les mêmes"
        await message.channel.send(response)
        return

    

    if text == "bot --stop" and message.author.name == 'jensn':
        raise discord.DiscordException("Admin stopped the bot from running")

    await bot.process_commands(message)

@bot.command(help="Pour terminer les débats -- Chiffre aléatoire entre 0 et le chiffre spécifié")
async def roll(ctx, num: str):
    command_name = "roll"

    if num.isdigit():
        max_num = int(num)
        x = randint(0, max_num)
        await ctx.send(x)
    else:
        await ctx.send("Envoie une commande correcte stp")

@bot.command(help="Envoie un meme aléatoire")
async def meme(ctx):
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get("https://www.generatormix.com/random-memes?number=1")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    div = soup.find(class_="thumbnail-col-1")
    img = div.find("img", class_="lazy thumbnail aspect-square-contain")

    img_source = img.get("data-src")
    
    await ctx.send(img_source)

@bot.command(help="Insulte le ping")
async def insulte(ctx, user):
    import json
    
    with open("insultes.json", "r", encoding="UTF-8") as file:
        insultes = json.load(file)

    insulte = "Espèce de "
    
    for part in insultes:
        ins = choice(insultes[part])
        insulte += ins + " "
    
    
    await ctx.send(f"{user} {insulte}")

if __name__ == "__main__":
    bot.run(TOKEN)