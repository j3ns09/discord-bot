from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is connected and ready!")
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if str(channel) == "test-bot":
                    await channel.send("Alexandre là pour vous servir")
                    # await channel.send("bot connecté\nhttps://tenor.com/view/the-deep-the-boys-gif-26305579")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "juif" in message.content:
            await message.channel.send("C'est moi qui vais te déporter si tu continues.")
        elif "arabe" in message.content:
            await message.channel.send("Toujours les mêmes.")

        if message.author.name.lower() == "jensn" and message.content == "bot --stop":
            try:
                await self.bot.logout()
            except:
                self.bot.clear()