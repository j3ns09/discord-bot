import discord
from discord.ext import commands
from utils.youtube import YTDLSource
import yt_dlp as youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command(help="Permet au bot de rejoindre un chat vocal.")
    async def viens(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Tu dois être en voc pour m'appeler.")

    @commands.command(help="Permet de jouer une musique dans un chat vocal en précisant l'url")
    async def joue_url(self, ctx, url):
        if ctx.author.voice:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Erreur: {e}') if e else None)
            await ctx.send(f"Playing {player.title}")
        else:
            await ctx.send("Tu dois être en voc pour m'appeler")


    @commands.command(help="Permet de jouer une musique dans un chat vocal en précisant le titre")
    async def joue_search(self, ctx, *title):
        ydl_opts = {
            'quiet': True,  # Suppress output messages
            'extract_flat': True,  # Only extract metadata
        }

        query = " ".join(title)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result : dict = ydl.extract_info(f"ytsearch1:{query}", download=False)

        if result["entries"] == []:
            await ctx.send("Résultats non trouvés")

        await self.joue_url(ctx, result["entries"][0]["url"])

    @commands.command(help="Fait quitter le bot du chat vocal")
    async def sors(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))
