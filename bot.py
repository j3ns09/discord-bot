import asyncio
from discord.ext import commands
from dotenv import load_dotenv

from config.config import PREFIX, TOKEN, intents

from cogs.events.core import Events
from cogs.fun import Fun
from cogs.music import Music


load_dotenv("t.env")

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


async def load_extensions():
    await bot.add_cog(Events(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Music(bot))


async def init():
    await load_extensions()


async def close():
    await bot.close()


if __name__ == "__main__":
    asyncio.run(init())
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        asyncio.run(bot.close())
