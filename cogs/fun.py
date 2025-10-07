from discord.ext import commands
from random import randint
from asyncio import sleep
from utils.insults import get_random_insult


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.server: int = 458935607373332480

    @commands.command(
        help="Pour terminer les débats -- Chiffre aléatoire entre 0 et le chiffre spécifié"
    )
    async def roll(self, ctx, num: str = 10):
        if num.isdigit():
            await ctx.send(randint(0, int(num)))
        else:
            await ctx.send("Envoie une commande correcte.")

    @commands.command(help="Insulte le ping")
    async def insulte(self, ctx, user):
        insult = get_random_insult()
        await ctx.send(f"{user} {insult}")

    @commands.command(help="Spam ping")
    async def spam(self, ctx, person, number):
        if self.bot.get_guild(self.server).get_member_named(person) is None:
            return
        if number.isdigit():
            number = int(number)
            if number > 15:
                await ctx.send("Le nombre de ping est trop grand.")
                return
            for _ in range(number):
                await ctx.send(f"{person}")
                await sleep(1)
