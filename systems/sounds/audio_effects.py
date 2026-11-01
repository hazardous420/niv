import sounddevice as sd
import soundfile as sf

import pygame
import numpy as np

_cache = {}

def get_distorted_sound(sound, amount):
    if amount <= 0:
        return sound

    amount = round(amount * 10) / 10
    key = (id(sound), amount)

    if key in _cache:
        return _cache[key]

    samples = pygame.sndarray.array(sound).copy()
    dtype = samples.dtype
    peak = np.iinfo(dtype).max

    levels = max(8, int(128 - amount * 120))
    step = max(1, int(1 + amount * 7))

    indices = (np.arange(len(samples)) // step) * step
    samples = samples[indices]

    quantisation = peak / levels
    samples = np.round(samples / quantisation) * quantisation
    samples = np.clip(samples, -peak, peak).astype(dtype)

    distorted = pygame.sndarray.make_sound(samples)
    _cache[key] = distorted

    return distorted

def play_sound(sound, sanity, volume=1.0):
    amount = max(0, (100 - sanity) / 100)

    distorted = get_distorted_sound(sound, amount)
    channel = distorted.play()

    if channel:
        channel.set_volume(volume)

    return channel

class DynamicMusic:
    def __init__(self, filepath, volume=0.2):
        self.audio, self.samplerate = sf.read(
            filepath,
            dtype="float32",
            always_2d=True
        )

        self.position = 0
        self.volume = volume
        self.amount = 0.0
        self.channels = self.audio.shape[1]

        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self.callback,
            blocksize=1024
        )

    def callback(self, outdata, frames, time, status):
        end = self.position + frames

        if end <= len(self.audio):
            samples = self.audio[self.position:end].copy()
        else:
            remaining = len(self.audio) - self.position
            samples = np.concatenate((
                self.audio[self.position:],
                self.audio[:frames - remaining]
            ))

        self.position = end % len(self.audio)

        amount = self.amount

        if amount > 0:
            levels = max(8, int(128 - amount * 120))
            samples = np.round(samples * levels) / levels

            step = max(1, int(1 + amount * 7))
            samples[::step] = samples[::step]

        outdata[:] = samples * self.volume

    def update(self, sanity):
        self.amount = max(0.0, min(1.0, (100 - sanity) / 100))

    def play(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
        self.stream.close()