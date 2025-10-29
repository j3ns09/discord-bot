import time
from collections import defaultdict


class Tracker:
    def __init__(self):
        self.message_counts: defaultdict[int, int] = defaultdict(int)
        self.voice_durations: defaultdict[int, int] = defaultdict(int)
        self.voice_sessions: dict[int, float] = {}

    def add_message(self, user_id: int):
        self.message_counts[user_id] += 1

    def start_voice_session(self, user_id: int):
        self.voice_sessions[user_id] = time.time()

    def stop_voice_session(self, user_id: int):
        start = self.voice_sessions.pop(user_id, None)
        if start:
            self.voice_durations[user_id] += int(time.time() - start)

    def clear(self):
        self.message_counts.clear()
        self.voice_durations.clear()
