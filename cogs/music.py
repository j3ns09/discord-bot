import discord
import asyncio
from discord.ext import commands
from utils.youtube import YTDLSource
import yt_dlp as youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.link_queue : list[str] = []
        self.ready_queue : list[YTDLSource] = []
        self.n_song : int = 0

    async def get_query(query: str):
        batch = []
        if query.startswith("https"):
            if "playlist" in query:
                url_list = await YTDLSource.playlist(query)
                batch.extend(url_list)
            else:
                batch.append(query)
        else:
            url = await YTDLSource.get_video_url(query)

            if not url:
                return 0
                await ctx.send("Musique non trouvée")

            batch.append(url)
        return batch

    async def add_to_queue(self, ctx, query: str):
        batch = await Music.get_query(query)

        if batch:
            self.link_queue.extend(batch)
            await ctx.send("Playlist ajoutée à la file d'attente") if len(batch) > 1 else await ctx.send("Lien youtube ajouté à la file d'attente")


        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def add_to_download(self, ctx, query):
        batch = await Music.get_query(query)
        players = []

        if batch:
            for link in batch:
                await ctx.send(f"Getting video {query}")
                player = await YTDLSource.video(link, stream=False)
                await ctx.send(f"Downloaded video {query}")

                players.append(player)

        self.ready_queue.extend(players)

    async def play_next(self, ctx):
        if len(self.link_queue) > 0:
            next_video = self.link_queue.pop(0)
            self.n_song += 1
            async with ctx.typing():
                if self.ready_queue:
                    ctx.voice_client.play(self.ready_queue.pop(), after=lambda e: print(e) if e else self.bot.loop.create_task(self.play_next(ctx)))

                player = await YTDLSource.video(next_video, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(e) if e else self.bot.loop.create_task(self.play_next(ctx)))
                # await ctx.send(f"Musique {self.n_song} en cours de lecture")
                await ctx.send(f"Lecture en cours de: {player.title}")
        else:
            await ctx.send("La playlist est vide.")


    @commands.command(help="Permet de visualiser la file d'attente")
    async def queue(self, ctx):
        nb_queue = len(self.link_queue)
        if nb_queue > 0:
            for i in range(len(self.link_queue)):
                await ctx.send(f"{i} : {self.link_queue[i]}")
        else:
            await ctx.send("La file d'attente est vide.")

    @commands.command(help="Permet au bot de rejoindre un chat vocal.")
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Tu dois être en voc pour m'appeler.")


    @commands.command(help="Permet de jouer une musique")
    async def play(self, ctx, query : str, *, standalone=False):
        print("Requesting a music to be played")
        if ctx.author.voice:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()

            options = {
                '-dl' : '-dl'
            }

            if options["-dl"] in query:
                await ctx.send("Option pour télécharger choisie")
                dl_k = options["-dl"]
                dl = query.find(dl_k)
                query = query[dl + len(dl_k)]
                await self.add_to_download(ctx, query)
            else:
                await self.add_to_queue(ctx, query)



    @commands.command(help="Permet de couper court à la musique en cours et de passer à la suivante")
    async def skip(self, ctx):
        await self.stop(ctx)
        await self.play_next(ctx)


    @commands.command(help="Fait quitter le bot du chat vocal")
    async def sors(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            await self.stop(ctx)
        self.bot.loop.stop()
        self.link_queue.clear()
        await ctx.guild.voice_client.disconnect()

    @commands.command(help="Arrête de jouer la musique en cours")
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Arrêt de l'audio en cours de lecture")

    @commands.command(help="Permet d'envoyer le bot jouer une musique à quelqu'un d'un autre salon vocal")
    async def gift(self, ctx, channel, *, query):
        for guild in self.bot.guilds:
            for chan in guild.channels:
                if channel == chan.name and isinstance(chan, discord.VoiceChannel):
                    if len(chan.members) > 0:
                        users = chan.members
                        await chan.connect()
                        await self.play(ctx, query)

                    else:
                        await ctx.send(f"Il n'y a personne dans le chat vocal {chan.name}")
                        return

# DEPRECATED

    # @commands.command(help="Permet de jouer une musique dans un chat vocal en précisant l'url")
    # async def play_url(self, ctx, url: str):
    #     if ctx.author.voice.channel:
    #         vc = await ctx.author.voice.channel.connect()
    #         print(f"bot connected to channel {ctx.author.voice.channel}")

    #         async with ctx.typing():
    #             player = await YTDLSource.video(url, stream=True)
    #             vc.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
    #             await ctx.send(f"Playing {player.title}")
    #     else:
    #         await ctx.send("Tu dois être en voc pour m'appeler")


    # @commands.command(help="Permet de jouer une musique dans un chat vocal en précisant le titre")
    # async def play_search(self, ctx, *title):
    #     ydl_opts = {
    #         'quiet': True,  # Suppress output messages
    #         'extract_flat': True,  # Only extract metadata
    #     }

    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         result : dict = ydl.extract_info(f"ytsearch1:{title}", download=False)

    #     if result["entries"] == []:
    #         await ctx.send("Résultats non trouvés")

    #     await self.play_url(ctx, result["entries"][0]["url"])