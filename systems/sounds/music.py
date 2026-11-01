import os
from systems.sounds.audio_effects import DynamicMusic

music_player = DynamicMusic(
    os.path.join("assets/music", "Distopia.wav"),
    volume=0.2
)

def start_bg_music():
    music_player.play()