import tkinter as tk
from tkinter import ttk
import pygame as pg
import mutagen, json

duration_song=178 # temporal
canciones=[]

# ____________ . ✰ * Funciones * ✰ . ____________
def play(filename):
    pg.mixer.init(frequency=16000)
    pg.mixer.music.load(filename)
    pg.mixer.music.play()

    progress_song["value"] = 0
    increase_progress_bar()

def increase_progress_bar():
    if progress_song["value"] < duration_song:
        progress_song["value"] += 1
        root.after(1000, increase_progress_bar) 

def cargar_json():
    global canciones
    try:
        with open("songs.json", "r") as archivo:
            canciones = json.load(archivo)
    except FileNotFoundError:
        canciones = []

def show_songs_tree():
    for s in canciones:
        tree_musica.insert("", tk.END, values=(
        s["Nombre"],
        s["Album"],
        s["Artista"],
    ))

# ____________ . ✰ * Root * ✰ . ____________
root = tk.Tk()
root.title("Música")
root.geometry("800x500")
root.resizable(False, False)

# ____________ . ✰ * Estilos * ✰ . ____________
style = ttk.Style()
style.theme_use('clam') #clam me gusta

style.configure("TLabelframe", background="#f79eb9")
style.configure("TLabelframe.Label", foreground="white", background="#f79eb9", font=("Arial", 10))
root.configure(bg="#ffc9d6")

style.configure("TButton", background="#e97799", foreground="white") #dps borrar pq ni voy a usar botones de texto

style.configure("Treeview.Heading", background="#e97799", foreground="white")
style.configure("Treeview", background="#fadce2", fieldbackground="#fde9ed", foreground="#b4365b")

style.configure("TLabel", foreground="white", background="#f79eb9", font=("Arial", 10))

style.configure("Custom.Horizontal.TProgressbar",
                troughcolor="#fde9ed",
                background="#e97799")

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

progress_song = ttk.Progressbar(songinfo_f, orient="horizontal", length=290, maximum=duration_song, mode='determinate', style="Custom.Horizontal.TProgressbar")
progress_song.grid(row=0, column=1, pady=15, padx=5) #quiero q arriba d ekla profress bar aparexca la fotito del album
time_song = ttk.Label(songinfo_f, text="0:00").grid(row=0, column=0, pady=15, padx=5)
time_left = ttk.Label(songinfo_f, text="-2:58").grid(row=0, column=2, pady=15, padx=5)

tree_musica = ttk.Treeview(songselect_f, columns=("Nombre", "Album", "Artista"), show="headings")
tree_musica.heading("Nombre", text="Nombre")
tree_musica.column("Nombre", width=120)
tree_musica.heading("Album", text="Álbum")
tree_musica.column("Album", width=120)
tree_musica.heading("Artista", text="Artista")
tree_musica.column("Artista", width=100)
tree_musica.pack(fill="both", expand=True, padx=10, pady=10)#voy a hacer q las cancniones sean hijitos de las playlist para q se puedan hacer o algo asi, dps veo

# ____________ . ✰ * Cargar * ✰ . ____________
cargar_json()
show_songs_tree()

# ____________ . ✰ * MainLoop * ✰ . ____________
progress_song["value"] = 0
increase_progress_bar()

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