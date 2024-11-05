import discord
from discord.ext import commands
from random import randint
from utils.insults import get_random_insult

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Pour terminer les débats -- Chiffre aléatoire entre 0 et le chiffre spécifié")
    async def roll(self, ctx, num: str):
        if num.isdigit():
            await ctx.send(randint(0, int(num)))
        else:
            await ctx.send("Envoie une commande correcte.")

    @commands.command(help="Insulte le ping")
    async def insulte(self, ctx, user):
        insult = get_random_insult()
        await ctx.send(f"{user} {insult}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
