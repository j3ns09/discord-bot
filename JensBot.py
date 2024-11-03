import os
import discord
from discord.ext import commands
from random import randint, choice


from dotenv import load_dotenv

load_dotenv("t.env")

TOKEN : str = os.getenv("DISCORD_TOKEN")
GUILD : discord.Guild = os.getenv("DISCORD_GUILD")

PREFIX = "_flih "


intents = discord.Intents(4194303)

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

@bot.command(help="Permet au bot de rejoindre un chat vocal.")
async def viens(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("tu dois être en voc pour m'appeler connard")

@bot.command(help="Permet de jouer une musique dans un chat vocal")
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
        return

    if "arabe" in text:
        response = "toujours les mêmes"
        await message.channel.send(response)
        return

    

    if text == "bot --stop" and message.author.name == 'jensn':
        raise discord.DiscordException("Admin stopped the bot from running")

    await bot.process_commands(message)

@bot.command(help="Pour terminer les débats -- Chiffre aléatoire entre 0 et le chiffre spécifié")
async def roll(ctx):
    command_name = "roll"

    text : str = ctx.message.content
    ptr : int = len(PREFIX) + len(command_name)
    try:
        max_num = int(text[ptr:])
        x = randint(0, max_num)
        await ctx.send(x)
    except ValueError:
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
async def insulte(ctx):
    command_name = "insulte"
    text = ctx.message.content
    ptr = len(PREFIX) + len(command_name)
    user = text[ptr:]
    
    import json
    
    with open("insultes.json", "r", encoding="UTF-8") as file:
        insultes = json.load(file)

    insulte = "Espèce de "
    
    for part in insultes:
        ins = choice(insultes[part])
        insulte += ins + " "
    
    
    await ctx.send(f"{user} {insulte}")

try:
    bot.run(TOKEN)
except discord.errors.DiscordException:
    pass