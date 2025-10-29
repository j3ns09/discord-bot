from cogs.events.scoring import format_time


def format_message_stats(message_counts, server) -> list[str]:
    if not message_counts:
        return ["Aucun message pour cet intervalle de temps."]
    lines = ["**Messages envoyés :**"]
    for uid, count in message_counts.items():
        member = server.get_member(uid)
        name = member.display_name if member else f"Utilisateur inconnu ({uid})"
        lines.append(f"- {name} : **{count} messages**")
    return lines


def format_voice_stats(voice_durations, server) -> list[str]:
    if not voice_durations:
        return ["Personne n'est allé en vocal."]
    lines = ["**Temps passé en vocal :**"]
    for uid, seconds in voice_durations.items():
        member = server.get_member(uid)
        name = member.display_name if member else f"Utilisateur inconnu ({uid})"
        lines.append(f"- {name} : **{format_time(seconds)}**")
    return lines
