import tkinter as tk
from tkinter import ttk
import pygame as pg
import mutagen, json

# ____________ . ✰ * Funciones * ✰ . ____________
def play(filename):
    pg.mixer.init(frequency=16000)
    pg.mixer.music.load(filename)
    pg.mixer.music.play()
    while pg.mixer.music.get_busy() == True:
        continue

# ____________ . ✰ * Root * ✰ . ____________
root = tk.Tk()
root.title("Música")
root.geometry("800x500")
root.resizable(False, False)

# ____________ . ✰ * Frames * ✰ . ____________
songinfo_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
songinfo_f.place(x=10, y=10, width=385, height=400)

songselect_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
songselect_f.place(x=405, y=10, width=385, height=400)

options_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
options_f.place(x=10, y=410, width=780, height=80)

# ____________ . ✰ * jaja * ✰ . ____________
play_b = ttk.Button(options_f, text="Play").grid(row=0, column=0, padx=5, pady=5)

# ____________ . ✰ * MainLoop * ✰ . ____________
root.mainloop()