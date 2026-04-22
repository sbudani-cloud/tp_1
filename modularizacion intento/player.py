import pygame as pg
import random
from mutagen.mp3 import MP3

class Player:
    def __init__(self):
        pg.mixer.init(frequency=16000)
        pg.mixer.music.set_volume(0.5)

        self.current_song = None
        self.paused = False
        self.offset = 0
        self.duration = 0

        self.playlist_shuffle = []

    # -------- AUDIO --------
    def load(self, filename):
        self.current_song = filename
        self.duration = MP3(filename).info.length
        pg.mixer.music.load(filename)

    def play(self, start=0):
        pg.mixer.music.play(start=start)
        self.paused = False

    def pause(self):
        pg.mixer.music.pause()
        self.paused = True

    def unpause(self):
        pg.mixer.music.unpause()
        self.paused = False

    def toggle_play(self):
        if self.paused:
            self.unpause()
            return "unpause"
        else:
            self.pause()
            return "pause"

    def play_song(self, filename):
        if self.current_song == filename:
            return self.toggle_play()

        self.load(filename)
        self.play(0)
        self.offset = 0
        return "new_song"

    def preparar_shuffle(self, playlist):
        self.playlist_shuffle = playlist[:]
        random.shuffle(self.playlist_shuffle)

    def get_next_shuffle(self):
        if not self.playlist_shuffle:
            return None
        return self.playlist_shuffle.pop(0)

    def cambiar_tiempo(self, nuevo_tiempo):
        self.offset = nuevo_tiempo
        pg.mixer.music.play(start=nuevo_tiempo)