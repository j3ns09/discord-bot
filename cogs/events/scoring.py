import time
from datetime import date, datetime

MESSAGE_COEFF = 1
VOICE_COEFF = 2.5


def score(nb_messages: int, voice_time: int) -> float:
    return nb_messages * MESSAGE_COEFF + (voice_time / 60) * VOICE_COEFF


def current_date() -> date:
    return date.fromtimestamp(time.time())


def current_datetime() -> datetime:
    return datetime.fromtimestamp(time.time())


def format_time(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"
