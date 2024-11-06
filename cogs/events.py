import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is connected and ready!")
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if str(channel) == "test-bot":
                    await channel.send("bot connecté")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "juif" in message.content:
            await message.channel.send("C'est moi qui vais te déporter si tu continues.")
        elif "arabe" in message.content:
            await message.channel.send("Toujours les mêmes.")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Events(bot))
