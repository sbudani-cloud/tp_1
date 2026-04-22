import tkinter as tk
from tkinter import ttk
import pygame as pg
from player import Player
from library import Library

class Luliiapp:
    def __init__(self, root):
        self.root = root
        self.player = Player()
        self.library = Library()
        self.loop = False
        self.aleatorio = False
        self.setup_ui()
        self.setup_events()
        self.load_data()

    def setup_ui(self):
        # ____________ . ✰ * Frames * ✰ . ____________
        songinfo_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        songinfo_f.place(x=10, y=10, width=385, height=400)

        songselect_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        songselect_f.place(x=405, y=10, width=385, height=400)

        options_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        options_f.place(x=10, y=420, width=780, height=80)

        for i in range(5):
            options_f.columnconfigure(i, weight=1)

        playlists_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        playlists_f.place(x=800, y=10, width=290, height=350)

        pl_options_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        pl_options_f.place(x=800, y=370, width=290, height=130)

        for i in range(2):
            pl_options_f.columnconfigure(i, weight=1)

        vol_frame = ttk.LabelFrame(self.root, text="  + . * ✰ * . +  ")
        vol_frame.place(x=1100, y=10, width=90, height=490)

    def setup_events(self):
        pass

    def load_data(self):
        self.library.load_json()
        print(self.library.canciones)