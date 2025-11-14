from dataclasses import dataclass
from typing import Any

@dataclass
class VoiceState:
    before: Any
    after: Any
    
    @property
    def became_unmuted(self):
        return (self.before.deaf or self.before.mute or self.before.self_mute or self.before.self_deaf) and not (self.after.deaf or self.after.mute or self.after.self_mute or self.after.self_deaf)

    @property
    def became_muted(self):
        return not (self.before.deaf or self.before.mute or self.before.self_mute or self.before.self_deaf) and (self.after.deaf or self.after.mute or self.after.self_mute or self.after.self_deaf)

    @property
    def has_joined_voice(self):
        return self.before.channel is None and self.after.channel is not None

    @property
    def has_left_voice(self):
        return self.before.channel is not None and self.after.channel is None