import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import PREFIX, TOKEN, intents


load_dotenv("t.env")

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def load_extensions():
    await bot.load_extension("cogs.fun")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.music")

async def init():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(init())
