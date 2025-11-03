import discord
from discord.ext import commands, tasks

from cogs.events.constants import *
from cogs.events.tracking import Tracker
from cogs.events.logger import Logger
from cogs.events.storage import Storage
from cogs.events.scoring import score, current_date
from cogs.events.reporting import format_message_stats, format_voice_stats


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.tracker: Tracker = Tracker()
        self.logger: Logger = Logger()
        self.storage: Storage = Storage()
        self.start_date = current_date()
        self.first_run: bool = True

    def reset_date(self):
        self.start_date = current_date()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is ready!")
        channel = self.bot.get_channel(TEST_CHANNEL_ID)
        await channel.send("Alexandre là pour vous servir")

        if not self.reset_stats.is_running():
            self.reset_stats.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not any(role.id == OGSS_ROLE_ID for role in message.author.roles):
            return
        self.tracker.add_message(message.author.id)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if not any(role.id == OGSS_ROLE_ID for role in member.roles):
            return
        if before.channel is None and after.channel is not None:
            self.tracker.start_voice_session(member.id)
            self.storage.add_log(
                member.id,
                self.storage.methods.JOIN,
                after.channel.name,
                len(after.channel.members),
            )

        elif before.channel is not None and after.channel is None:
            self.tracker.stop_voice_session(member.id)
            self.storage.add_log(
                member.id,
                self.storage.methods.QUIT,
                before.channel.name,
                len(before.channel.members) - 1,
            )

    @commands.command(name="trolleur")
    async def show_weekly_stats(self, ctx):
        server = ctx.guild
        await ctx.send(f"**Stats depuis le {self.start_date.strftime('%d/%m/%y')}**")
        await ctx.send(
            "\n".join(format_message_stats(self.tracker.message_counts, server))
        )
        await ctx.send(
            "\n".join(format_voice_stats(self.tracker.voice_durations, server))
        )

    @tasks.loop(hours=168)
    async def reset_stats(self):
        if self.first_run:
            self.first_run = False
            self.tracker.clear()
            return

        server: discord.Guild = self.bot.get_guild(SERVER_ID)
        channel = self.bot.get_channel(OGS_CHANNEL_ID)
        await channel.send(
            f"**Stats de la semaine du {self.start_date.strftime('%d/%m/%y')}**"
        )

        await channel.send(
            "\n".join(format_message_stats(self.tracker.message_counts, server))
        )
        await channel.send(
            "\n".join(format_voice_stats(self.tracker.voice_durations, server))
        )

        activity_scores: dict[int, float] = {}
        for member in server.members:
            if member.bot or not any(r.id == OGSS_ROLE_ID for r in member.roles):
                continue
            messages = self.tracker.message_counts.get(member.id, 0)
            seconds = self.tracker.voice_durations.get(member.id, 0)
            activity_scores[member.id] = score(messages, seconds)

        if not activity_scores:
            await channel.send("Aucune donnée pour cette semaine.")
            return

        loser_id = min(activity_scores, key=activity_scores.get)
        winner_id = max(activity_scores, key=activity_scores.get)
        loser = server.get_member(loser_id)
        winner = server.get_member(winner_id)

        loser_role = server.get_role(TROLL_ROLE_ID)
        winner_role = server.get_role(PUANT_ROLE_ID)

        for m in server.members:
            if loser_role in m.roles and m != loser:
                await m.remove_roles(loser_role)
            if winner_role in m.roles and m != winner:
                await m.remove_roles(winner_role)

        await loser.add_roles(loser_role)
        await winner.add_roles(winner_role)

        await channel.send(
            f"Le moins actif est **{loser.display_name}**, rôle {loser_role.mention}"
        )
        await channel.send(
            f"Le plus actif est **{winner.display_name}**, rôle {winner_role.mention}"
        )

        # Reset
        self.tracker.clear()
        self.reset_date()
        self.logger.clean()
        self.storage.clear_logs()

    @reset_stats.before_loop
    async def before_reset_stats(self):
        await self.bot.wait_until_ready()
