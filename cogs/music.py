import discord
import asyncio
from threading import Thread
from discord.ext import commands
from utils.youtube import YTDLSource
import yt_dlp as youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.is_in_voice = False
        self.queue : list[YTDLSource] = []

    async def is_user_voice(ctx):
        if not ctx.author.voice:
            await ctx.send("Tu ]dois être en voc pour m'appeler")
            return False
        return True
    
    async def add_to_playlist(self, ctx, url):
        # await ctx.send("Téléchargement de la musique...")
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        # await ctx.send("Musique téléchargée...")
        if len(self.queue) > 0:
            await ctx.send("Son ajouté à la playlist")
        
        self.queue.append(player)
        
        if ctx.voice_client.is_playing():
            return
        else:
            await self.play_audio(ctx)

    def play_next(self):
        print(self.queue)
        if self.queue:
            song = self.queue.pop(0)
            return song
        return False

    async def play_audio(self, ctx):
        async with ctx.typing():
            song = self.play_next()

            if song == False:
                await ctx.send(f"Fin playlist")
                return
            
            await ctx.send(f"Playing {song.title}")
            ctx.voice_client.play(song, after=lambda: self.play_next)

    async def auto_join(self, ctx):
        await ctx.author.voice.channel.connect()
        self.is_in_voice = True

    @commands.command(help="Permet au bot de rejoindre un chat vocal.")
    async def viens(self, ctx):
        # Si user is in voice channel
        if await Music.is_user_voice(ctx):
            await self.auto_join(ctx)

    @commands.command(help="Permet de jouer une musique dans un chat vocal en précisant l'url")
    async def play_url(self, ctx, url):
        if not await Music.is_user_voice(ctx):
            return

        if not self.is_in_voice:
            await self.auto_join(ctx)
        await self.add_to_playlist(ctx, url)

    @commands.command(help="Permet de jouer une musique dans un chat vocal en précisant le titre")
    async def play_search(self, ctx, *, title):
        ydl_opts = YTDLSource.ydl_opts
        
        query = " ".join(title)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result : dict = ydl.extract_info(f"ytsearch1:{query}", download=False)
            
        if result["entries"] == []:
            await ctx.send("Résultats non trouvés")

        await self.play_url(ctx, result["entries"][0]["url"])

    @commands.command(help="Fait quitter le bot du chat vocal")
    async def sors(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()

    @commands.command(help="Arrête de jouer la musique en cours")
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Arrêt de l'audio en cours de lecture")

    @commands.command(help="Permet d'envoyer le bot jouer une musique à quelqu'un d'un autre salon vocal")
    async def gift(self, ctx, channel, *, url):
        for guild in self.bot.guilds:
            for chan in guild.channels:
                if channel == chan.name and isinstance(chan, discord.VoiceChannel):
                    if len(chan.members) > 0:
                        users = chan.members
                        await chan.connect()
                        await self.add_to_playlist(ctx, url)

                    else:
                        await ctx.send(f"Il n'y a personne dans le chat vocal {chan.name}")    
                        return

async def setup(bot):
    await bot.add_cog(Music(bot))
