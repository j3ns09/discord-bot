import os
import discord
from dotenv import load_dotenv

load_dotenv("t.env")

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
PREFIX = "&lex "

intents = discord.Intents.all()
