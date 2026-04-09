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
orden_actual = {}
loop = False
tiempito_musica = 0

pg.mixer.init(frequency=16000)
SONG_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(SONG_END)

# ____________ . ✰ * Funciones * ✰ . ____________
def segundos_a_minutos(segundos):
    minutos = segundos//60
    segundos = segundos % 60
    if segundos >= 0 and segundos <= 9:
        segundos = f"0{segundos}"
    return f"{minutos}:{segundos}"
def play(filename): #arreglar para q ande con lo q se seleccione en el coso de playlists
    global duration_song, current_song, paused, bar_moment, SONG_END
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

        duration_song = MP3(current_song).info.length
        progress_song["maximum"] = duration_song

        paused = False
        progress_song["value"] = 0 
        increase_progress_bar()

def increase_progress_bar():
    global bar_moment, tiempito_musica
    if not paused and current_song:
        pos_ms = pg.mixer.music.get_pos()
        if pos_ms != -1:
            segundos = pos_ms / 1000
            progress_song["value"] = segundos

            restante = duration_song - segundos
            time_left["text"] = f"-{segundos_a_minutos(int(restante))}"

            time_song["text"] = segundos_a_minutos(int(segundos))
            tiempito_musica = int(segundos)
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

def seleccionar_cancion(event): #que se deseleccione uno si se selecciono uno en el otro treeview
    global filename
    selec = tree_musica.selection()
    if selec:
        item = tree_musica.item(selec[0])
        valores = item["values"]
        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                filename = s["direc"]
                break

def anadir_a_playlist():
    for s in canciones:
        if filename == s["direc"]:
            tree_playlist.insert("", tk.END, values=(
                s["Nombre"], s["Album"], s["Artista"], s["Duracion"], ))

def eliminar_de_playlist():
    selec = tree_playlist.selection()
    if selec:
        tree_playlist.delete(selec[0])

def refrescar_treeview_musica():
    for item in tree_musica.get_children():
        tree_musica.delete(item)
    for s in canciones:
        tree_musica.insert("", tk.END, values=(
            s["Nombre"], s["Album"], s["Artista"], s["Duracion"]
        ))

def ordenar(columna):
    global canciones
    reverso = orden_actual.get(columna, False)
    canciones.sort(key=lambda x: x[columna].lower(), reverse=reverso)
    orden_actual[columna] = not reverso
    refrescar_treeview_musica()

def checkiar_musica_termino():
    for event in pg.event.get():
        if event.type == SONG_END:
            if loop == False:
                siguiente_cancion()
            else:
                pg.mixer.music.play()
                progress_song["value"] = 0
    root.after(200, checkiar_musica_termino)

def siguiente_cancion():
    global current_song, filename
    selec = tree_musica.selection()
    items = tree_musica.get_children()
    if not items:
        return
    if selec:
        index = items.index(selec[0])
        siguiente_index = index + 1
    else:
        siguiente_index = 0

    if siguiente_index < len(items):
        next_item = items[siguiente_index]
        tree_musica.selection_set(next_item)
        tree_musica.focus(next_item)
        valores = tree_musica.item(next_item)["values"]

        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                play(s["direc"])
                
                filename = s["direc"]
                current_song = s["direc"]
                break
    else:
        tree_musica.selection_set(items[0])
        tree_musica.focus(items[0])
        valores = tree_musica.item(items[0])["values"]
        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                play(s["direc"])
                filename = s["direc"]
                current_song = s["direc"]
                break

def anterior_cancion():
    global current_song, filename, tiempito_musica
    selec = tree_musica.selection()
    items = tree_musica.get_children()
    if not items:
        return
    if selec:
        index = items.index(selec[0])
        anterior_index = index - 1
    else:
        anterior_index = 0

    if tiempito_musica < 3:
        if anterior_index < len(items) and anterior_index >= 0:
            item_anterior = items[anterior_index]
            tree_musica.selection_set(item_anterior)
            tree_musica.focus(item_anterior)
            valores = tree_musica.item(item_anterior)["values"]

            for s in canciones:
                if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                    play(s["direc"])
                    
                    filename = s["direc"]
                    current_song = s["direc"]
                    break
    else:
        pg.mixer.music.play()

def cambiar_loop():
    global loop
    if loop == True:
        loop = False
    else:
        loop = True

# ____________ . ✰ * Root * ✰ . ____________
pg.init()

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

for i in range(2):
    pl_options_f.columnconfigure(i, weight=1)

# ____________ . ✰ * Adentro de los Frames * ✰ . ____________
aleatorio_b = ttk.Button(options_f, text="Aleatorio").grid(row=0, column=0, pady=15)
anterior_b = ttk.Button(options_f, text="Anterior", command=anterior_cancion).grid(row=0, column=1, pady=15) #si esta en medio d la cancnion tiene q reiniciarla en vez de ir a lka anetrior (comom spotify)
play_b = ttk.Button(options_f, text="Play/Pausar", command=lambda: play(filename)).grid(row=0, column=2, pady=15)
siguiente_b = ttk.Button(options_f, text="Siguiente", command=siguiente_cancion).grid(row=0, column=3, pady=15)
loop_b = ttk.Button(options_f, text="Repetir", command=cambiar_loop).grid(row=0, column=4, pady=15)

progress_song = ttk.Progressbar(songinfo_f, orient="horizontal", length=290, maximum=duration_song, mode='determinate', style="Custom.Horizontal.TProgressbar")
progress_song.grid(row=0, column=1, pady=15, padx=5) #quiero q arriba d ekla profress bar aparexca la fotito del album

time_song = ttk.Label(songinfo_f, text=segundos_a_minutos(int(duration_song)))
time_song.grid(row=0, column=0, pady=15, padx=5)

time_left = ttk.Label(songinfo_f, text="-0:00")
time_left.grid(row=0, column=2, pady=15, padx=5)

tree_musica = ttk.Treeview(songselect_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
tree_musica.heading("Nombre", text="Nombre", command=lambda: ordenar("Nombre"))
tree_musica.column("Nombre", width=100)
tree_musica.heading("Album", text="Álbum", command=lambda: ordenar("Album"))
tree_musica.column("Album", width=100)
tree_musica.heading("Artista", text="Artista", command=lambda: ordenar("Artista"))
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

agregar_a_pl = ttk.Button(pl_options_f, text="Añadir a la Playlist", command=anadir_a_playlist).grid(row=0, column=0, pady=10)
eliminar_pl = ttk.Button(pl_options_f, text="Eliminar de la Playlist", command=eliminar_de_playlist).grid(row=0, column=1, pady=10)

tree_playlist.bind("<ButtonRelease-1>", seleccionar_cancion)
# ____________ . ✰ * Cargar * ✰ . ____________
cargar_json()
show_songs_tree()

# ____________ . ✰ * MainLoop * ✰ . ____________
checkiar_musica_termino()
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