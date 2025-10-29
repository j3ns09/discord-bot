import time
from datetime import date, datetime


def score(nb_messages: int, voice_time: int) -> float:
    message_coeff = 1
    voice_coeff = 2.5
    return nb_messages * message_coeff + (voice_time / 60) * voice_coeff


def current_date() -> date:
    return date.fromtimestamp(time.time())


def current_datetime() -> datetime:
    return datetime.fromtimestamp(time.time())


def format_time(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"
