import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame as pg
from mutagen.mp3 import MP3
import json, random, os
from PIL import Image, ImageTk

# ____________ . ✰ * Variables * ✰ . ____________
filename_catalogo = None
filename_playlist = None
duration_song=0
current_song = None
paused = False
bar_moment = None
canciones=[]
orden_actual = {}
loop = False
aleatorio = False
tiempito_musica = 0
playlist_shuffle = []
estilo_actual = 0
estilos = ["rosa", "azul"]
offset= 0
last_song = None
drag_item = None

pg.mixer.init(frequency=16000)
pg.mixer.music.set_volume(0.5)
SONG_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(SONG_END)

# ____________ . ✰ * Funciones * ✰ . ____________
def segundos_a_minutos(segundos):
    minutos = segundos//60
    segundos = segundos % 60
    if segundos >= 0 and segundos <= 9:
        segundos = f"0{segundos}"
    return f"{minutos}:{segundos}"

def play(filename=None):
    global duration_song, current_song, paused, bar_moment, SONG_END, offset, last_song
    if filename is None:
        if tree_playlist.selection():
            filename = filename_playlist
        elif tree_musica.selection():
            filename = filename_catalogo
    if not filename:
        return
    
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
        last_song = current_song  
        pg.mixer.music.load(filename)
        pg.mixer.music.play()
        current_song = filename

        offset = 0
        
        show_img_album()

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
            segundos = (pos_ms / 1000) + offset
            progress_song["value"] = segundos

            restante = duration_song - segundos
            time_left["text"] = f"-{segundos_a_minutos(int(restante))}"

            time_song["text"] = segundos_a_minutos(int(segundos))
            tiempito_musica = int(segundos)
    bar_moment = root.after(200, increase_progress_bar)

def cargar_json():
    global canciones
    try:
        with open("songs.json", "r", encoding = "utf-8") as archivo:
            canciones = json.load(archivo)
    except FileNotFoundError:
        canciones = []

def show_songs_tree():
    for i, s in enumerate(canciones):
        tree_musica.insert("", tk.END, values=(
        s["Nombre"], s["Album"], s["Artista"], s["Duracion"], ))

def seleccionar_catalogo(event):
    global filename_catalogo
    tree_playlist.selection_set(())
    selec = tree_musica.selection()
    if selec:
        valores = tree_musica.item(selec[0])["values"]
        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                filename_catalogo = s["direc"]
                break

def seleccionar_playlist(event):
    global filename_playlist
    tree_musica.selection_set(())
    selec = tree_playlist.selection()
    if selec:
        valores = tree_playlist.item(selec[0])["values"]
        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                filename_playlist = s["direc"]
                break

def añadir_a_playlist(event=None):
    for s in canciones:
        if filename_catalogo == s["direc"]:
            for item in tree_playlist.get_children():
                valores = tree_playlist.item(item)["values"]
                if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                    respuesta = messagebox.askyesno(
                        "Canción duplicada",
                        "Esta canción ya está en la playlist.\n¿Querés agregarla igual?"
                    )
                    if not respuesta:
                        return
                    break
            tree_playlist.insert("", tk.END, values=(
                s["Nombre"], s["Album"], s["Artista"], s["Duracion"]))
            guardar_playlist()
            return

def eliminar_de_playlist():
    selec = tree_playlist.selection()
    if selec:
        tree_playlist.delete(selec[0])
    guardar_playlist()

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
    global tiempito_musica, duration_song, offset

    if current_song and not paused:
        if tiempito_musica >= int(duration_song) - 1:
            if loop:
                pg.mixer.music.play()
                offset=0
            else:
                siguiente_cancion()
                offset=0

    root.after(500, checkiar_musica_termino)

def siguiente_cancion():
    global current_song, filename_playlist, playlist_shuffle
    if aleatorio:
        global playlist_shuffle

        if not playlist_shuffle:
            shuffle()

        cancion = playlist_shuffle.pop(0)

        play(cancion["direc"])
        filename_playlist = cancion["direc"]
        current_song = cancion["direc"]
        
        for item in tree_playlist.get_children():
            valores = tree_playlist.item(item)["values"]
            for s in canciones:
                if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                    if s["direc"] == cancion["direc"]:
                        tree_playlist.selection_set(item)
                        tree_playlist.focus(item)
                        tree_playlist.see(item)
                        break
        return
    
    selec = tree_playlist.selection()
    items = tree_playlist.get_children()
    if not items:
        return
    if selec:
        index = items.index(selec[0])
        siguiente_index = index + 1
    else:
        siguiente_index = 0

    if siguiente_index < len(items):
        next_item = items[siguiente_index]
        tree_playlist.selection_set(next_item)
        tree_playlist.focus(next_item)
        valores = tree_playlist.item(next_item)["values"]

        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                play(s["direc"])
                
                filename_playlist = s["direc"]
                current_song = s["direc"]
                break
    else:
        tree_playlist.selection_set(items[0])
        tree_playlist.focus(items[0])
        valores = tree_playlist.item(items[0])["values"]
        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                play(s["direc"])
                filename_playlist = s["direc"]
                current_song = s["direc"]
                break

def anterior_cancion():
    global current_song, filename_playlist, tiempito_musica, offset

    if aleatorio and last_song:
        anterior = last_song
        play(anterior)
        for item in tree_playlist.get_children():
            valores = tree_playlist.item(item)["values"]
            for s in canciones:
                if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                    if s["direc"] == anterior:
                        tree_playlist.selection_set(item)
                        tree_playlist.focus(item)
                        tree_playlist.see(item)
                        break
        return
    
    selec = tree_playlist.selection()
    items = tree_playlist.get_children()
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
            tree_playlist.selection_set(item_anterior)
            tree_playlist.focus(item_anterior)
            valores = tree_playlist.item(item_anterior)["values"]

            for s in canciones:
                if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                    play(s["direc"])
                    
                    filename_playlist = s["direc"]
                    current_song = s["direc"]
                    break
    else:
        offset = 0
        pg.mixer.music.play()

def cambiar_loop():
    global loop
    if loop == True:
        loop_b.state(["!selected"])
        loop = False
    else:
        loop_b.state(["selected"])
        loop = True

def randum_orden():
    global aleatorio
    if aleatorio == True:
        aleatorio_b.state(["!selected"])
        aleatorio = False
    else:
        aleatorio_b.state(["selected"])
        aleatorio = True
        shuffle()

def shuffle():
    global playlist_shuffle
    playlist_shuffle = []

    for item in tree_playlist.get_children():
        valores = tree_playlist.item(item)["values"]

        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                playlist_shuffle.append(s)
                break

    random.shuffle(playlist_shuffle)

def show_img_album():
    global current_song, img_album
    album=""
    for e in canciones:
        if e["direc"] == current_song:
            if e["Album"].lower() == "desconocido":
                img = Image.open("albums/desconocido.png").convert("RGBA")
            else:
                for letra in e["Album"]:
                    if letra in "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ":
                        album+= letra
                img = Image.open(f"albums/{album}.png").convert("RGBA")
            img_album = ImageTk.PhotoImage(img)
            album_label.config(image=img_album)
            album_label.image = img_album
            break

def cambiar_estilo():
    global estilos, estilo_actual
    estilo_actual += 1
    actualizar_estilo()
    
def actualizar_estilo():
    global estilo_actual, estilos
    try:
        a = estilos[estilo_actual]
    except IndexError:
        estilo_actual = 0
    if estilos[estilo_actual] == "rosa":
        tema_rosita()
    else:
        tema_azul()

def cambiar_tiempo_cancion(event):
    global duration_song, offset, paused
    nuevo_tiempo = duration_song * (event.x / progress_song.winfo_width())
    offset = nuevo_tiempo 
    if paused:
        pg.mixer.music.play(start=nuevo_tiempo)
        pg.mixer.music.pause()
    else:
        pg.mixer.music.play(start=nuevo_tiempo)

def guardar_playlist():
    playlist = []
    for item in tree_playlist.get_children():
        valores = tree_playlist.item(item)["values"]
        for s in canciones:
            if (s["Nombre"], s["Album"], s["Artista"], s["Duracion"]) == tuple(valores):
                playlist.append(s["direc"])
                break
    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(playlist, f, indent=4)

def cargar_playlist():
    try:
        with open("playlist.json", "r", encoding="utf-8") as f:
            direcciones = json.load(f)

        for d in direcciones:
            for s in canciones:
                if s["direc"] == d:
                    tree_playlist.insert("", tk.END, values=(
                        s["Nombre"], s["Album"], s["Artista"], s["Duracion"]
                    ))
                    break
    except FileNotFoundError:
        pass

def on_button_press(event):
    global drag_item
    item = tree_playlist.identify_row(event.y)
    if item:
        drag_item = item

def on_motion(event):
    global drag_item
    if not drag_item:
        return

    target = tree_playlist.identify_row(event.y)
    if target and target != drag_item:
        index = tree_playlist.index(target)
        tree_playlist.move(drag_item, "", index)

def on_button_release(event):
    global drag_item
    drag_item = None
    guardar_playlist()

def seleccionar_y_soltar(event):
    seleccionar_playlist(event)
    on_button_release(event)

def filtrar_canciones(event=None):
    texto = search_var.get().lower()

    if texto == "buscar...":
        texto = ""

    for item in tree_musica.get_children():
        tree_musica.delete(item)

    for s in canciones:
        if (texto in s["Nombre"].lower() or
            texto in s["Album"].lower() or
            texto in s["Artista"].lower()):
            
            tree_musica.insert("", tk.END, values=(
                s["Nombre"], s["Album"], s["Artista"], s["Duracion"]
            ))

def poner_placeholder(event=None):
    if search_entry.get() == "":
        search_entry.insert(0, "Buscar...")
        search_entry.config(foreground="#c89dfd")

def quitar_placeholder(event):
    if search_entry.get() == "Buscar...":
        search_entry.delete(0, tk.END)
        search_entry.config(foreground="#893ae9")

def abrir_archivos():
    global canciones

    archivos = filedialog.askopenfilenames(
        title="Seleccionar canciones",
        filetypes=[("Archivos MP3", "*.mp3")]
    )

    for ruta in archivos:
        try:
            audio = MP3(ruta)
            duracion = int(audio.info.length)

            nombre = os.path.basename(ruta).replace(".mp3", "")
            
            nueva = {
                "Nombre": nombre,
                "Album": "Desconocido",
                "Artista": "Desconocido",
                "Duracion": segundos_a_minutos(duracion),
                "direc": ruta
            }
            if any(s["direc"] == ruta for s in canciones):
                continue
            canciones.append(nueva)

        except Exception as e:
            print("Error con:", ruta)

    with open("songs.json", "w", encoding="utf-8") as f:
        json.dump(canciones, f, indent=4)

    refrescar_treeview_musica()

def cambiar_volumen(valor):
    volumen = float(valor) / 100
    pg.mixer.music.set_volume(volumen)
    num_vol["text"] = valor

# ____________ . ✰ * Root * ✰ . ____________
pg.init()

root = tk.Tk()
root.title("✩ + . * Luliify * . + ✩")
root.geometry("1200x510")
root.resizable(False, False)

# ____________ . ✰ * Imagenes * ✰ . ____________
img_boton_loop = tk.PhotoImage(file="images/button_loop.png")
img_boton_loop_act = tk.PhotoImage(file="images/button_loop_act.png")

img_blue_boton_loop = tk.PhotoImage(file="images/blue_button_loop.png")
img_blue_boton_loop_act = tk.PhotoImage(file="images/blue_button_loop_act.png")

img_boton_aleatorio = tk.PhotoImage(file="images/button_aleatorio.png")
img_boton_aleatorio_act = tk.PhotoImage(file="images/button_aleatorio_act.png")

img_blue_boton_aleatorio = tk.PhotoImage(file="images/blue_button_aleatorio.png")
img_blue_boton_aleatorio_act = tk.PhotoImage(file="images/blue_button_aleatorio_act.png")

img_album = tk.PhotoImage(file="albums/none.png")

# ____________ . ✰ * Estilos * ✰ . ____________
style = ttk.Style()
style.theme_use('clam')

style.element_create("PLoop.button", "image", img_boton_loop, ("selected", img_boton_loop_act))
style.element_create("PAleatorio.button", "image", img_boton_aleatorio, ("selected", img_boton_aleatorio_act))

style.element_create("BLoop.button", "image", img_blue_boton_loop, ("selected", img_blue_boton_loop_act))
style.element_create("BAleatorio.button", "image", img_blue_boton_aleatorio, ("selected", img_blue_boton_aleatorio_act))

def tema_rosita():
    style.configure("TLabelframe", background="#f79eb9")
    style.configure("TLabelframe.Label", foreground="white", background="#f79eb9", font=("Trebuchet MS", 10, "bold"))
    root.configure(bg="#ffc9d6")

    album_label.config(bg="#f79eb9")

    style.configure("TButton", background="#e97799", foreground="white")

    style.configure("Treeview.Heading", background="#e97799", foreground="white")
    style.configure("Treeview", background="#fadce2", fieldbackground="#fde9ed", foreground="#b4365b")

    style.configure("TLabel", foreground="white", background="#f79eb9", font=("Arial", 10))

    style.configure("Custom.Horizontal.TProgressbar", troughcolor="#fde9ed", background="#e97799")

    style.layout("Loop.TButton", [
        ("PLoop.button", {"sticky": "nswe"})
    ])
    style.configure("Loop.TButton",
        background="#f79eb9",
        padding=0,
        borderwidth=0
    )

    style.layout("Aleatorio.TButton", [
        ("PAleatorio.button", {"sticky": "nswe"})
    ])
    style.configure("Aleatorio.TButton",
        background="#f79eb9",
        padding=0,
        borderwidth=0
    )

    style.configure("Search.TEntry", fieldbackground="#fde9ed", 
                    bordercolor="#e97799", padding=5)
    
    volumen_slider.config(bg="#e97799", troughcolor="#fde9ed", fg="white",
                        activebackground="#d55e82")

def tema_azul():
    style.configure("TLabelframe", background="#9ec5f7")
    style.configure("TLabelframe.Label", foreground="white", background="#9ec5f7", font=("Trebuchet MS", 10, "bold"))
    root.configure(bg="#c9e0ff")

    album_label.config(bg="#9ec5f7")

    style.configure("TButton", background="#77b6e9", foreground="white")

    style.configure("Treeview.Heading", background="#63abe6", foreground="white")
    style.configure("Treeview", background="#dce4fa", fieldbackground="#e9effd", foreground="#3671b4")

    style.configure("TLabel", foreground="white", background="#9ec5f7", font=("Arial", 10))

    style.configure("Custom.Horizontal.TProgressbar", troughcolor="#e9effd", background="#63abe6")

    style.layout("Loop.TButton", [
        ("BLoop.button", {"sticky": "nswe"})
    ])
    style.configure("Loop.TButton",
        background="#9ec5f7",
        padding=0,
        borderwidth=0
    )
    
    style.layout("Aleatorio.TButton", [
        ("BAleatorio.button", {"sticky": "nswe"})
    ])
    style.configure("Aleatorio.TButton",
        background="#9ec5f7",
        padding=0,
        borderwidth=0
    )

    style.configure("Search.TEntry", fieldbackground="#e9effd", 
                    bordercolor="#63abe6", padding=5)
    
    volumen_slider.config(bg="#63abe6", troughcolor="#e9effd", fg="white", 
                        activebackground="#5399d2")

# ____________ . ✰ * Frames * ✰ . ____________
songinfo_f = ttk.LabelFrame(root, text="+ . * ✰ Canción ✰ * . +")
songinfo_f.place(x=10, y=10, width=385, height=400)

songselect_f = ttk.LabelFrame(root, text="+ . * ✰ Catálogo ✰ * . +")
songselect_f.place(x=405, y=10, width=385, height=400)

options_f = ttk.LabelFrame(root, text="+ . * ✰ Opciones ✰ * . +")
options_f.place(x=10, y=420, width=780, height=80)

for i in range(5):
    options_f.columnconfigure(i, weight=1)

playlists_f = ttk.LabelFrame(root, text="+ . * ✰ Playlist ✰ * . +")
playlists_f.place(x=800, y=10, width=290, height=350)

pl_options_f = ttk.LabelFrame(root, text="+ . * ✰ Opciones ✰ * . +")
pl_options_f.place(x=800, y=370, width=290, height=130)

for i in range(2):
    pl_options_f.columnconfigure(i, weight=1)

vol_frame = ttk.LabelFrame(root, text="✰ Volumen ✰")
vol_frame.place(x=1100, y=10, width=90, height=490)

# ____________ . ✰ * Adentro de los Frames * ✰ . ____________
anterior_b = ttk.Button(options_f, text="Anterior", command=anterior_cancion).grid(row=0, column=1, pady=15) #si esta en medio d la cancnion tiene q reiniciarla en vez de ir a lka anetrior (comom spotify)
play_b = ttk.Button(options_f, text="Play/Pausar", command=lambda: play()).grid(row=0, column=2, pady=15)
siguiente_b = ttk.Button(options_f, text="Siguiente", command=siguiente_cancion).grid(row=0, column=3, pady=15)

aleatorio_b = ttk.Button(options_f, style="Aleatorio.TButton", command=randum_orden)
aleatorio_b.grid(row=0, column=0)
loop_b = ttk.Button(options_f, style="Loop.TButton", command=cambiar_loop)
loop_b.grid(row=0, column=4)

progress_song = ttk.Progressbar(songinfo_f, orient="horizontal", length=290, maximum=duration_song, mode='determinate', style="Custom.Horizontal.TProgressbar")
progress_song.grid(row=1, column=1, pady=15, padx=5)

progress_song.bind("<Button-1>", cambiar_tiempo_cancion)

time_song = ttk.Label(songinfo_f, text=segundos_a_minutos(int(duration_song)))
time_song.grid(row=1, column=0, pady=15, padx=5)

time_left = ttk.Label(songinfo_f, text="-0:00")
time_left.grid(row=1, column=2, pady=15, padx=5)

volumen_slider = tk.Scale(
    vol_frame,
    from_=100,
    to=0,
    orient="vertical",
    command=cambiar_volumen,
    length=420, #450
    width=30,
    showvalue=0,
    highlightthickness=0,
    bd=0    
)
volumen_slider.set(50)
volumen_slider.grid(row=0, column=0, padx=30, pady=5)

num_vol = ttk.Label(vol_frame, text="50")
num_vol.grid(row=1, column=0, padx=30, pady=5)


search_var = tk.StringVar()
search_entry = ttk.Entry(songselect_f, textvariable=search_var, style="Search.TEntry")
search_entry.pack(fill="x", padx=10, pady=5)
search_entry.bind("<KeyRelease>", filtrar_canciones)
search_entry.insert(0, "Buscar...")
search_entry.config(foreground="gray")
search_entry.bind("<FocusIn>", quitar_placeholder)
search_entry.bind("<FocusOut>", poner_placeholder)

tree_musica = ttk.Treeview(songselect_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
tree_musica.heading("Nombre", text="Nombre", command=lambda: ordenar("Nombre"))
tree_musica.column("Nombre", width=100)
tree_musica.heading("Album", text="Álbum", command=lambda: ordenar("Album"))
tree_musica.column("Album", width=100)
tree_musica.heading("Artista", text="Artista", command=lambda: ordenar("Artista"))
tree_musica.column("Artista", width=110)
tree_musica.heading("Duracion", text="⏱️", command=lambda: ordenar("Duracion"))
tree_musica.column("Duracion", width=30)
tree_musica.pack(fill="both", expand=True, padx=10, pady=10)#voy a hacer q las cancniones sean hijitos de las playlist para q se puedan hacer o algo asi, dps veo

tree_musica.bind("<ButtonRelease-1>", seleccionar_catalogo)
tree_musica.bind("<Double-Button-1>", lambda e: play())

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

agregar_a_pl = ttk.Button(pl_options_f, text="Añadir a la Playlist", command=añadir_a_playlist).grid(row=0, column=0, pady=10)
eliminar_pl = ttk.Button(pl_options_f, text="Eliminar de la Playlist", command=eliminar_de_playlist).grid(row=0, column=1, pady=10)
cambiar_estilo_b = ttk.Button(pl_options_f, text="Cambiar Estilo", command=cambiar_estilo).grid(row=1, column=0, pady=10)
abrir_archivo_b = ttk.Button(pl_options_f, text="Abrir archivo...", command=abrir_archivos)
abrir_archivo_b.grid(row=1, column=1, pady=10)

tree_playlist.bind("<Double-Button-1>", lambda e: play())
tree_playlist.bind("<ButtonPress-1>", on_button_press)
tree_playlist.bind("<B1-Motion>", on_motion)
tree_playlist.bind("<ButtonRelease-1>", seleccionar_y_soltar)

# ____________ . ✰ * Albums * ✰ . ____________
album_label = tk.Label(songinfo_f, image=img_album, borderwidth=0)
album_label.grid(row=0, column=1, pady=15)

# ____________ . ✰ * Cargar * ✰ . ____________
cargar_json()
cargar_playlist()
show_songs_tree()
checkiar_musica_termino()
actualizar_estilo()

# ____________ . ✰ * MainLoop * ✰ . ____________
root.mainloop()