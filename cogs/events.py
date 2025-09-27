import discord
from discord.ext import commands, tasks
from collections import defaultdict

import time, json
from datetime import date

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        
        self.server : int = 458935607373332480
        self.test_channel_id : int = 1295153171081072720
        self.ogs_channel_id : int = 1120761434045939822

        self.ogss_role_id : int = 1135009307688177789
        self.troll_role_id : int = 1408007325716975648

        self.counting_start = Events.current_date()
        self.message_counts = defaultdict(int)
        self.voice_durations = defaultdict(int)

        self.voice_sessions : dict = {}

        self.first_run = True

    # Voice time in seconds
    @staticmethod
    def score(nb_messages: int, voice_time: int):
        message_coeff = 1
        voice_coeff = 2.5
        return nb_messages * message_coeff + (voice_time / 60) * voice_coeff

    # Get current date
    @staticmethod
    def current_date():
        return date.fromtimestamp(time.time())

    def get_counting_start(self):
        return self.counting_start.strftime("%d/%m/%y")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is connected and ready!")
        test_channel = self.bot.get_channel(self.test_channel_id)
        await test_channel.send("Alexandre là pour vous servir")
        # await channel.send("bot connecté\nhttps://tenor.com/view/the-deep-the-boys-gif-26305579")

        if not self.reset_stats.is_running():
            self.reset_stats.start()

    @commands.command("trolleur", help="Le trolleur de la semaine à commencer du début du compte")
    async def get_current_stats(self, ctx):
        server = self.server

        await ctx.send(f"📊 **Stats de la semaine à partir du {self.get_counting_start()} ** 📊")

        if self.message_counts:
            msg_lines = ["**Messages envoyés :**"]
            for user_id, count in self.message_counts.items():
                member = self.bot.get_guild(self.server).get_member(user_id)
                username = member.display_name if member else f"Utilisateur inconnu ({user_id})"
                msg_lines.append(f"- {username} : **{count} messages**")
            await ctx.send("\n".join(msg_lines))
        else:
            await ctx.send("Aucun message pour cet intervalle de temps.")

        if self.voice_durations:
            voc_lines = ["**Temps passé en vocal :**"]
            for user_id, seconds in self.voice_durations.items():
                member = self.bot.get_guild(self.server).get_member(user_id)
                username = member.display_name if member else f"Utilisateur inconnu ({user_id})"

                hours, remainder = divmod(seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                voc_lines.append(f"- {username} : **{hours}h {minutes}m**")
            await ctx.send("\n".join(voc_lines))
        else:
            await ctx.send("Personne n'est allé en vocal pour cet intervalle de temps.")

        if self.message_counts or self.voice_durations:
            activity_scores = {}

            for member in server.members:
                if member.bot:
                    continue
                if not any(role.id == self.ogss_role_id for role in member.roles):
                    continue
                messages = self.message_counts.get(member.id, 0)
                seconds = self.voice_durations.get(member.id, 0)
                score = Events.score(messages, seconds)
                activity_scores[member.id] = score

            loser_id = min(activity_scores, key=activity_scores.get)
            loser_member = server.get_member(loser_id)

            await ctx.send(f"Le moins actif pour cet intervalle est **{loser_member.display_name}**")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not any(role.id == self.ogss_role_id for role in message.author.roles): 
            return
        
        self.message_counts[message.author.id] += 1

        if "juif" in message.content:
            await message.channel.send("C'est moi qui vais te déporter si tu continues.")
        elif "arabe" in message.content:
            await message.channel.send("Toujours les mêmes.")

        if message.author.name.lower() == "jensn" and message.content == "bot --stop":
            try:
                await self.bot.logout()
            except:
                self.bot.clear()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not any(role.id == self.ogss_role_id for role in member.roles):
            return
        if before.channel is None and after.channel is not None:
            self.voice_sessions[member.id] = time.time()
        elif before.channel is not None and after.channel is None:
            m_id = member.id
            if m_id in self.voice_sessions:
                duration = int(time.time() - self.voice_sessions[m_id])
                self.voice_durations[m_id] += duration
                del self.voice_sessions[m_id]

    @tasks.loop(hours=168)
    async def reset_stats(self):
        if self.first_run:
            self.first_run = False
            self.message_counts.clear()
            self.voice_durations.clear()
            return
        
        server = self.bot.get_guild(self.server)
        ogs_channel = self.bot.get_channel(self.ogs_channel_id)
        
        await ogs_channel.send(f"📊 **Stats de la semaine du {self.get_counting_start()}** 📊")

        if self.message_counts:
            msg_lines = ["**Messages envoyés :**"]
            for user_id, count in self.message_counts.items():
                member = self.bot.get_guild(self.server).get_member(user_id)
                username = member.display_name if member else f"Utilisateur inconnu ({user_id})"
                msg_lines.append(f"- {username} : **{count} messages**")
            await ogs_channel.send("\n".join(msg_lines))
        else:
            await ogs_channel.send("Aucun message cette semaine.")

        if self.voice_durations:
            voc_lines = ["**Temps passé en vocal :**"]
            for user_id, seconds in self.voice_durations.items():
                member = self.bot.get_guild(self.server).get_member(user_id)
                username = member.display_name if member else f"Utilisateur inconnu ({user_id})"

                hours, remainder = divmod(seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                voc_lines.append(f"- {username} : **{hours}h {minutes}m**")
            await ogs_channel.send("\n".join(voc_lines))
        else:
            await ogs_channel.send("Personne n'est allé en vocal cette semaine.")

        if self.message_counts or self.voice_durations:
            activity_scores = {}

            for member in server.members:
                if member.bot:
                    continue
                if not any(role.id == self.ogss_role_id for role in member.roles):
                    continue
                messages = self.message_counts.get(member.id, 0)
                seconds = self.voice_durations.get(member.id, 0)
                score = Events.score(messages, seconds)
                activity_scores[member.id] = score

            loser_id = min(activity_scores, key=activity_scores.get)
            loser_member = server.get_member(loser_id)
            loser_role = server.get_role(self.troll_role_id)

            for m in server.members:
                if loser_role in m.roles and m != loser_member:
                    await m.remove_roles(loser_role)

            await loser_member.add_roles(loser_role)
            await ogs_channel.send(f"🏆 Le moins actif cette semaine est **{loser_member.display_name}**, "
                                f"il reçoit le rôle de {loser_role.mention} !")

        # Sauvegarde dans un JSON
        # with open("stats.json", "w") as f:
        #     json.dump({
        #         "messages": self.message_counts,
        #         "vocal": self.voice_durations
        #     }, f, default=int, indent=2)

        self.message_counts.clear()
        self.voice_durations.clear()
        self.counting_start = Events.current_date()

    @reset_stats.before_loop
    async def before_reset_stats(self):
        await self.bot.wait_until_ready()