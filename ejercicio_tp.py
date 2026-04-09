import tkinter as tk
from tkinter import ttk
import pygame as pg
from mutagen.mp3 import MP3
import json

# ____________ . ✰ * Variables * ✰ . ____________
filename = None
duration_song=0
current_song = None
paused = False
bar_moment = None
canciones=[]
loop = False #todavia no lo hice pero ya lo voy preparando

# ____________ . ✰ * Funciones * ✰ . ____________
def segundos_a_minutos(segundos):
    minutos = segundos//60
    segundos = segundos % 60
    if segundos >= 0 and segundos <= 9:
        segundos = f"0{segundos}"
    return f"{minutos}:{segundos}"
def play(filename):
    global duration_song, current_song, paused, bar_moment
    pg.mixer.init(frequency=16000)
    if current_song == filename:
        if paused:
            pg.mixer.music.unpause()
            paused = False
            increase_progress_bar()
        else:
            pg.mixer.music.pause()
            paused = True
            if bar_moment: 
                root.after_cancel(bar_moment)
    else:
        pg.mixer.music.load(filename)
        pg.mixer.music.play()
        current_song = filename
        print(current_song)

        duration_song = MP3(current_song).info.length
        progress_song["maximum"] = duration_song

        paused = False
        progress_song["value"] = 0 
        increase_progress_bar()

def increase_progress_bar():
    global bar_moment
    if not paused and current_song:
        pos_ms = pg.mixer.music.get_pos()
        if pos_ms != -1:
            segundos = pos_ms / 1000
            progress_song["value"] = segundos

            restante = duration_song - segundos
            time_left["text"] = f"-{segundos_a_minutos(int(restante))}"

            time_song["text"] = segundos_a_minutos(int(segundos))
    bar_moment = root.after(200, increase_progress_bar)

def cargar_json():
    global canciones
    try:
        with open("songs.json", "r") as archivo:
            canciones = json.load(archivo)
    except FileNotFoundError:
        canciones = []

def show_songs_tree():
    for i, s in enumerate(canciones):
        tree_musica.insert("", tk.END, values=(
        s["Nombre"], s["Album"], s["Artista"], s["Duracion"], ))

def seleccionar_cancion(event):
    global filename
    selec = tree_musica.selection()
    if selec: 
        id = int(selec[0].strip("I0"))
        cancion = canciones[id-1]
        filename = cancion["direc"]

# ____________ . ✰ * Root * ✰ . ____________
root = tk.Tk()
root.title("Música")
root.geometry("1100x510")
root.resizable(False, False)

# ____________ . ✰ * Estilos * ✰ . ____________
style = ttk.Style()
style.theme_use('clam')

style.configure("TLabelframe", background="#f79eb9")
style.configure("TLabelframe.Label", foreground="white", background="#f79eb9", font=("Arial", 10))
root.configure(bg="#ffc9d6")

style.configure("TButton", background="#e97799", foreground="white") #dps borrar pq ni voy a usar botones de texto

style.configure("Treeview.Heading", background="#e97799", foreground="white")
style.configure("Treeview", background="#fadce2", fieldbackground="#fde9ed", foreground="#b4365b")

style.configure("TLabel", foreground="white", background="#f79eb9", font=("Arial", 10))

style.configure("Custom.Horizontal.TProgressbar", troughcolor="#fde9ed", background="#e97799")

# ____________ . ✰ * Frames * ✰ . ____________
songinfo_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
songinfo_f.place(x=10, y=10, width=385, height=400)

songselect_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
songselect_f.place(x=405, y=10, width=385, height=400)

options_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
options_f.place(x=10, y=420, width=780, height=80)

for i in range(5):
    options_f.columnconfigure(i, weight=1)

playlists_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
playlists_f.place(x=800, y=10, width=290, height=350)

pl_options_f = ttk.LabelFrame(root, text="+ . * ✰ * . +")
pl_options_f.place(x=800, y=370, width=290, height=130)

# ____________ . ✰ * Adentro de los Frames * ✰ . ____________
aleatorio_b = ttk.Button(options_f, text="Aleatorio").grid(row=0, column=0, pady=15)
anterior_b = ttk.Button(options_f, text="Anterior").grid(row=0, column=1, pady=15) #si esta en medio d la cancnion tiene q reiniciarla en vez de ir a lka anetrior (comom spotify)
play_b = ttk.Button(options_f, text="Play/Pausar", command=lambda: play(filename)).grid(row=0, column=2, pady=15)
siguiente_b = ttk.Button(options_f, text="Siguiente").grid(row=0, column=3, pady=15)
loop_b = ttk.Button(options_f, text="Repetir").grid(row=0, column=4, pady=15)

progress_song = ttk.Progressbar(songinfo_f, orient="horizontal", length=290, maximum=duration_song, mode='determinate', style="Custom.Horizontal.TProgressbar")
progress_song.grid(row=0, column=1, pady=15, padx=5) #quiero q arriba d ekla profress bar aparexca la fotito del album

time_song = ttk.Label(songinfo_f, text=segundos_a_minutos(int(duration_song)))
time_song.grid(row=0, column=0, pady=15, padx=5)

time_left = ttk.Label(songinfo_f, text="-0:00")
time_left.grid(row=0, column=2, pady=15, padx=5)

tree_musica = ttk.Treeview(songselect_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
tree_musica.heading("Nombre", text="Nombre")
tree_musica.column("Nombre", width=100)
tree_musica.heading("Album", text="Álbum")
tree_musica.column("Album", width=100)
tree_musica.heading("Artista", text="Artista")
tree_musica.column("Artista", width=110)
tree_musica.heading("Duracion", text="⏱️")
tree_musica.column("Duracion", width=30)
tree_musica.pack(fill="both", expand=True, padx=10, pady=10)#voy a hacer q las cancniones sean hijitos de las playlist para q se puedan hacer o algo asi, dps veo

tree_musica.bind("<ButtonRelease-1>", seleccionar_cancion)


tree_playlist = ttk.Treeview(playlists_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
tree_playlist.heading("Nombre", text="Nombre")
tree_playlist.column("Nombre", width=80)
tree_playlist.heading("Album", text="Álbum")
tree_playlist.column("Album", width=80)
tree_playlist.heading("Artista", text="Artista")
tree_playlist.column("Artista", width=70)
tree_playlist.heading("Duracion", text="⏱️")
tree_playlist.column("Duracion", width=30)
tree_playlist.pack(fill="both", expand=True, padx=10, pady=10)

agregar_a_pl = ttk.Button(pl_options_f, text="Añadir a la Playlist").grid(row=0, column=0, pady=10, padx=25)
eliminar_pl = ttk.Button(pl_options_f, text="Eliminar Playlist").grid(row=0, column=1, pady=15)

# ____________ . ✰ * Cargar * ✰ . ____________
cargar_json()
show_songs_tree()

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