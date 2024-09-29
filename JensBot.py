import os
import discord
import youtube_dl
from discord.ext import commands


from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD : discord.Guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents(4194303)

bot : commands.Bot = commands.Bot(command_prefix="flih_", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected and ready !")

# === MUSIC ===

@bot.command(name="join", help="Permet au bot de rejoindre un chat vocal.")
async def viens(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("tu dois être en voc pour m'appeler connard")

@bot.command(name="play", help="Permet de jouer une musique dans un chat vocal")
async def joue(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        #TODO make the acual thing
    else:
        await ctx.send("tu dois être en voc pour m'appeler connard")




# === USELESS ===

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    text : str = message.content

    if "juif" in text:
        response = "c'est moi qui vait te déporter si tu continues avec ça"
        await message.channel.send(response)

    if "arabe" in text:
        response = "toujours les mêmes"
        await message.channel.send(response)

    

    if text == "bot --stop" and message.author.name == 'jensn':
        raise discord.DiscordException("Admin stopped the bot from running")

    await bot.process_commands(message)

bot.run(TOKEN)