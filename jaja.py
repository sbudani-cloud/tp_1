import tkinter as tk
from tkinter import ttk
import pygame as pg
import mutagen, json

duration_song=350 # temporal

# ____________ . ✰ * Funciones * ✰ . ____________
def play(filename):
    pg.mixer.init(frequency=16000)
    pg.mixer.music.load(filename)
    pg.mixer.music.play()
    while pg.mixer.music.get_busy() == True:
        continue

def increase_progress_bar():
    pass

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

for i in range(5):
    options_f.columnconfigure(i, weight=1)

# ____________ . ✰ * Adentro de los Frames * ✰ . ____________
aleatorio_b = ttk.Button(options_f, text="Aleatorio").grid(row=0, column=0, pady=15)
anterior_b = ttk.Button(options_f, text="Anterior").grid(row=0, column=1, pady=15) #si esta en medio d la cancnion tiene q reiniciarla en vez de ir a lka anetrior (comom spotify)
play_b = ttk.Button(options_f, text="Play/Pausar").grid(row=0, column=2, pady=15)
siguiente_b = ttk.Button(options_f, text="Siguiente").grid(row=0, column=3, pady=15)
loop_b = ttk.Button(options_f, text="Repetir").grid(row=0, column=4, pady=15)

progress_song = ttk.Progressbar(songinfo_f, orient="horizontal", length=duration_song, mode='determinate')
progress_song.pack(padx=10, pady=10) #quiero q arriba d ekla profress bar aparexca la fotito del album

tree_musica = ttk.Treeview(songselect_f, columns=("Nombre", "Album", "Artista"), show="headings")
tree_musica.pack(fill="both", expand=True, padx=10, pady=10)

# ____________ . ✰ * MainLoop * ✰ . ____________
root.mainloop()

"""
codigo para poner gifs.... capaz lo use (depende pero capaz no) pq quiero q
la foto del alnum sea un circulo cn un disco atras y q eso gire cuando esta en play

import tkinter as tk

root = tk.Tk()
label = tk.Label(root)
label.pack()

# Cargar frames (asumiendo gif con 160 frames)
frames = [tk.PhotoImage(file='imagen.gif', format=f'gif -index {i}') for i in range(160)]

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == 160: ind = 0
    label.configure(image=frame)
    root.after(20, update, ind)

root.after(0, update, 0)
root.mainloop()
"""