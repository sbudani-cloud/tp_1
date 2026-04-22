import tkinter as tk
from tkinter import ttk
import pygame as pg
from player import Player
from library import Library

class Luliiapp:
    def __init__(self, root):
        self.root = root

        # ____________ . ✰ * Imagenes * ✰ . ____________
        self.img_boton_loop = tk.PhotoImage(file="images/button_loop.png")
        self.img_boton_loop_act = tk.PhotoImage(file="images/button_loop_act.png")

        self.img_blue_boton_loop = tk.PhotoImage(file="images/blue_button_loop.png")
        self.img_blue_boton_loop_act = tk.PhotoImage(file="images/blue_button_loop_act.png")

        self.img_boton_aleatorio = tk.PhotoImage(file="images/button_aleatorio.png")
        self.img_boton_aleatorio_act = tk.PhotoImage(file="images/button_aleatorio_act.png")

        self.img_blue_boton_aleatorio = tk.PhotoImage(file="images/blue_button_aleatorio.png")
        self.img_blue_boton_aleatorio_act = tk.PhotoImage(file="images/blue_button_aleatorio_act.png")

        #____________ . ✰ * Variables * ✰ . ____________
        self.player = Player()
        self.library = Library()
        self.loop = False
        self.aleatorio = False
        self.img_album = tk.PhotoImage(file="albums/none.png")
        self.temas = ["rosa", "azul"]
        self.tema_actual = 0

        #____________ . ✰ * Iniciar * ✰ . ____________
        self.setup_ui()
        self.setup_events()
        self.load_data()
        self.setup_styles()
        self.tema_rosita() #temporal
    
    def setup_ui(self):
        # ____________ . ✰ * Frames * ✰ . ____________
        self.songinfo_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.songinfo_f.place(x=10, y=10, width=385, height=400)

        self.songselect_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.songselect_f.place(x=405, y=10, width=385, height=400)

        self.options_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.options_f.place(x=10, y=420, width=780, height=80)

        for i in range(5):
            self.options_f.columnconfigure(i, weight=1)

        self.playlists_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.playlists_f.place(x=800, y=10, width=290, height=350)

        self.pl_options_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.pl_options_f.place(x=800, y=370, width=290, height=130)

        for i in range(2):
            self.pl_options_f.columnconfigure(i, weight=1)

        self.vol_frame = ttk.LabelFrame(self.root, text="  + . * ✰ * . +  ")
        self.vol_frame.place(x=1100, y=10, width=90, height=490)

        # ____________ . ✰ * Botones * ✰ . ____________
        anterior_b = ttk.Button(self.options_f, text="Anterior").grid(row=0, column=1, pady=15) #si esta en medio d la cancnion tiene q reiniciarla en vez de ir a lka anetrior (comom spotify)
        play_b = ttk.Button(self.options_f, text="Play/Pausar").grid(row=0, column=2, pady=15)
        siguiente_b = ttk.Button(self.options_f, text="Siguiente").grid(row=0, column=3, pady=15)

        aleatorio_b = ttk.Button(self.options_f, style="Aleatorio.TButton")
        aleatorio_b.grid(row=0, column=0)
        loop_b = ttk.Button(self.options_f, style="Loop.TButton")
        loop_b.grid(row=0, column=4)

        # ____________ . ✰ * Progress Bar * ✰ . ____________
        progress_song = ttk.Progressbar(self.songinfo_f, orient="horizontal", length=290, maximum=67, mode='determinate', style="Custom.Horizontal.TProgressbar")
        progress_song.grid(row=1, column=1, pady=15, padx=5)

        time_song = ttk.Label(self.songinfo_f, text="0:00")
        time_song.grid(row=1, column=0, pady=15, padx=5)

        time_left = ttk.Label(self.songinfo_f, text="-0:00")
        time_left.grid(row=1, column=2, pady=15, padx=5)

        # ____________ . ✰ * Volumen * ✰ . ____________
        self.volumen_slider = tk.Scale(
            self.vol_frame,
            from_=100,
            to=0,
            orient="vertical",
            length=450,
            width=30,
            showvalue=0,
            highlightthickness=0,
            bd=0    
        )
        self.volumen_slider.set(50)
        self.volumen_slider.grid(row=0, column=0, padx=30, pady=10)

        # ____________ . ✰ * Barra de Busqueda * ✰ . ____________
        search_var = tk.StringVar()
        search_entry = ttk.Entry(self.songselect_f, textvariable=search_var, style="Search.TEntry")
        search_entry.pack(fill="x", padx=10, pady=5)
        search_entry.insert(0, "Buscar...")
        search_entry.config(foreground="gray")

        # ____________ . ✰ * Tree Catálogo * ✰ . ____________
        tree_musica = ttk.Treeview(self.songselect_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
        tree_musica.heading("Nombre", text="Nombre")
        tree_musica.column("Nombre", width=100)
        tree_musica.heading("Album", text="Álbum")
        tree_musica.column("Album", width=100)
        tree_musica.heading("Artista", text="Artista")
        tree_musica.column("Artista", width=110)
        tree_musica.heading("Duracion", text="⏱️")
        tree_musica.column("Duracion", width=30)
        tree_musica.pack(fill="both", expand=True, padx=10, pady=10)

        # ____________ . ✰ * Tree Playlist * ✰ . ____________
        tree_playlist = ttk.Treeview(self.playlists_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
        tree_playlist.heading("Nombre", text="Nombre")
        tree_playlist.column("Nombre", width=80)
        tree_playlist.heading("Album", text="Álbum")
        tree_playlist.column("Album", width=80)
        tree_playlist.heading("Artista", text="Artista")
        tree_playlist.column("Artista", width=70)
        tree_playlist.heading("Duracion", text="⏱️")
        tree_playlist.column("Duracion", width=30)
        tree_playlist.pack(fill="both", expand=True, padx=10, pady=10)

        agregar_a_pl = ttk.Button(self.pl_options_f, text="Añadir a la Playlist").grid(row=0, column=0, pady=10)
        eliminar_pl = ttk.Button(self.pl_options_f, text="Eliminar de la Playlist").grid(row=0, column=1, pady=10)
        cambiar_estilo_b = ttk.Button(self.pl_options_f, text="Cambiar Estilo", command=self.cambiar_tema).grid(row=1, column=0, pady=10)
        abrir_archivo_b = ttk.Button(self.pl_options_f, text="Abrir archivo...")
        abrir_archivo_b.grid(row=1, column=1, pady=10)

        # ____________ . ✰ * Fotos de Album * ✰ . ____________
        self.album_label = tk.Label(self.songinfo_f, image=self.img_album, borderwidth=0)
        self.album_label.grid(row=0, column=1, pady=15)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.element_create(
            "PLoop.button", "image", self.img_boton_loop, ("selected", self.img_boton_loop_act)
        )
        self.style.element_create(
            "PAleatorio.button", "image", self.img_boton_aleatorio, ("selected", self.img_boton_aleatorio_act)
        )
        self.style.element_create(
            "BLoop.button", "image", self.img_blue_boton_loop, ("selected", self.img_blue_boton_loop_act)
        )
        self.style.element_create(
            "BAleatorio.button", "image", self.img_blue_boton_aleatorio, ("selected", self.img_blue_boton_aleatorio_act)
        )

    def tema_rosita(self):
        self.style.configure("TLabelframe", background="#f79eb9")
        self.style.configure("TLabelframe.Label", foreground="white", background="#f79eb9", font=("Arial", 10))
        self.root.configure(bg="#ffc9d6")

        self.album_label.config(bg="#f79eb9")

        self.style.configure("TButton", background="#e97799", foreground="white")

        self.style.configure("Treeview.Heading", background="#e97799", foreground="white")
        self.style.configure("Treeview", background="#fadce2", fieldbackground="#fde9ed", foreground="#b4365b")

        self.style.configure("TLabel", foreground="white", background="#f79eb9", font=("Arial", 10))

        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor="#fde9ed", background="#e97799")

        self.style.layout("Loop.TButton", [
            ("PLoop.button", {"sticky": "nswe"})
        ])
        self.style.configure("Loop.TButton",
            background="#f79eb9",
            padding=0,
            borderwidth=0
        )

        self.style.layout("Aleatorio.TButton", [
            ("PAleatorio.button", {"sticky": "nswe"})
        ])
        self.style.configure("Aleatorio.TButton",
            background="#f79eb9",
            padding=0,
            borderwidth=0
        )

        self.style.configure("Search.TEntry", fieldbackground="#fde9ed", 
                        bordercolor="#e97799", padding=5)
        
        self.volumen_slider.config(bg="#e97799", troughcolor="#fde9ed", fg="white",
                            activebackground="#d55e82")

    def tema_azul(self):
        self.style.configure("TLabelframe", background="#9ec5f7")
        self.style.configure("TLabelframe.Label", foreground="white", background="#9ec5f7", font=("Arial", 10))
        self.root.configure(bg="#c9e0ff")

        self.album_label.config(bg="#9ec5f7")

        self.style.configure("TButton", background="#77b6e9", foreground="white")

        self.style.configure("Treeview.Heading", background="#63abe6", foreground="white")
        self.style.configure("Treeview", background="#dce4fa", fieldbackground="#e9effd", foreground="#3671b4")

        self.style.configure("TLabel", foreground="white", background="#9ec5f7", font=("Arial", 10))

        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor="#e9effd", background="#63abe6")

        self.style.layout("Loop.TButton", [
            ("BLoop.button", {"sticky": "nswe"})
        ])
        self.style.configure("Loop.TButton",
            background="#9ec5f7",
            padding=0,
            borderwidth=0
        )
        
        self.style.layout("Aleatorio.TButton", [
            ("BAleatorio.button", {"sticky": "nswe"})
        ])
        self.style.configure("Aleatorio.TButton",
            background="#9ec5f7",
            padding=0,
            borderwidth=0
        )

        self.style.configure("Search.TEntry", fieldbackground="#e9effd", 
                        bordercolor="#63abe6", padding=5)
        
        self.volumen_slider.config(bg="#63abe6", troughcolor="#e9effd", fg="white", 
                            activebackground="#5399d2")
    
    def actualizar_tema(self):
        try:
            a = self.temas[self.tema_actual]
        except IndexError:
            self.tema_actual = 0
        
        if self.temas[self.tema_actual] == "rosa":
            self.tema_rosita()
        else:
            self.tema_azul()

    def cambiar_tema(self):
        self.tema_actual += 1
        self.actualizar_tema()

    def setup_events(self):
        pass

    def load_data(self):
        self.library.load_json()
        print(self.library.canciones)


"""def setup_ui(self):
        # ____________ . ✰ * Frames * ✰ . ____________
        self.songinfo_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.songinfo_f.place(x=10, y=10, width=385, height=400)

        self.songselect_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.songselect_f.place(x=405, y=10, width=385, height=400)

        self.options_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.options_f.place(x=10, y=420, width=780, height=80)

        for i in range(5):
            self.options_f.columnconfigure(i, weight=1)

        self.playlists_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.playlists_f.place(x=800, y=10, width=290, height=350)

        self.pl_options_f = ttk.LabelFrame(self.root, text="+ . * ✰ * . +")
        self.pl_options_f.place(x=800, y=370, width=290, height=130)

        for i in range(2):
            self.pl_options_f.columnconfigure(i, weight=1)

        self.vol_frame = ttk.LabelFrame(self.root, text="  + . * ✰ * . +  ")
        self.vol_frame.place(x=1100, y=10, width=90, height=490)

        # ____________ . ✰ * Botones * ✰ . ____________
        anterior_b = ttk.Button(self.options_f, text="Anterior", command=anterior_cancion).grid(row=0, column=1, pady=15) #si esta en medio d la cancnion tiene q reiniciarla en vez de ir a lka anetrior (comom spotify)
        play_b = ttk.Button(self.options_f, text="Play/Pausar", command=lambda: play()).grid(row=0, column=2, pady=15)
        siguiente_b = ttk.Button(self.options_f, text="Siguiente", command=siguiente_cancion).grid(row=0, column=3, pady=15)

        aleatorio_b = ttk.Button(self.options_f, style="Aleatorio.TButton", command=randum_orden)
        aleatorio_b.grid(row=0, column=0)
        loop_b = ttk.Button(self.options_f, style="Loop.TButton", command=cambiar_loop)
        loop_b.grid(row=0, column=4)

        # ____________ . ✰ * Progress Bar * ✰ . ____________
        progress_song = ttk.Progressbar(self.songinfo_f, orient="horizontal", length=290, maximum=duration_song, mode='determinate', style="Custom.Horizontal.TProgressbar")
        progress_song.grid(row=1, column=1, pady=15, padx=5)

        progress_song.bind("<Button-1>", cambiar_tiempo_cancion)

        time_song = ttk.Label(self.songinfo_f, text=segundos_a_minutos(int(duration_song)))
        time_song.grid(row=1, column=0, pady=15, padx=5)

        time_left = ttk.Label(self.songinfo_f, text="-0:00")
        time_left.grid(row=1, column=2, pady=15, padx=5)

        # ____________ . ✰ * Volumen * ✰ . ____________
        volumen_slider = tk.Scale(
            self.vol_frame,
            from_=100,
            to=0,
            orient="vertical",
            command=cambiar_volumen,
            length=450,
            width=30,
            showvalue=0,
            highlightthickness=0,
            bd=0    
        )
        volumen_slider.set(50)
        volumen_slider.grid(row=0, column=0, padx=30, pady=10)

        # ____________ . ✰ * Barra de Busqueda * ✰ . ____________
        search_var = tk.StringVar()
        search_entry = ttk.Entry(self.songselect_f, textvariable=search_var, style="Search.TEntry")
        search_entry.pack(fill="x", padx=10, pady=5)
        search_entry.bind("<KeyRelease>", filtrar_canciones)
        search_entry.insert(0, "Buscar...")
        search_entry.config(foreground="gray")
        search_entry.bind("<FocusIn>", quitar_placeholder)
        search_entry.bind("<FocusOut>", poner_placeholder)

        # ____________ . ✰ * Tree Catálogo * ✰ . ____________
        tree_musica = ttk.Treeview(self.songselect_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
        tree_musica.heading("Nombre", text="Nombre", command=lambda: ordenar("Nombre"))
        tree_musica.column("Nombre", width=100)
        tree_musica.heading("Album", text="Álbum", command=lambda: ordenar("Album"))
        tree_musica.column("Album", width=100)
        tree_musica.heading("Artista", text="Artista", command=lambda: ordenar("Artista"))
        tree_musica.column("Artista", width=110)
        tree_musica.heading("Duracion", text="⏱️")
        tree_musica.column("Duracion", width=30)
        tree_musica.pack(fill="both", expand=True, padx=10, pady=10)#voy a hacer q las cancniones sean hijitos de las playlist para q se puedan hacer o algo asi, dps veo

        tree_musica.bind("<ButtonRelease-1>", seleccionar_catalogo)
        tree_musica.bind("<Double-Button-1>", lambda e: play())

        # ____________ . ✰ * Tree Playlist * ✰ . ____________
        tree_playlist = ttk.Treeview(self.playlists_f, columns=("Nombre", "Album", "Artista", "Duracion"), show="headings")
        tree_playlist.heading("Nombre", text="Nombre")
        tree_playlist.column("Nombre", width=80)
        tree_playlist.heading("Album", text="Álbum")
        tree_playlist.column("Album", width=80)
        tree_playlist.heading("Artista", text="Artista")
        tree_playlist.column("Artista", width=70)
        tree_playlist.heading("Duracion", text="⏱️")
        tree_playlist.column("Duracion", width=30)
        tree_playlist.pack(fill="both", expand=True, padx=10, pady=10)

        agregar_a_pl = ttk.Button(self.pl_options_f, text="Añadir a la Playlist", command=añadir_a_playlist).grid(row=0, column=0, pady=10)
        eliminar_pl = ttk.Button(self.pl_options_f, text="Eliminar de la Playlist", command=eliminar_de_playlist).grid(row=0, column=1, pady=10)
        cambiar_estilo_b = ttk.Button(self.pl_options_f, text="Cambiar Estilo", command=cambiar_estilo).grid(row=1, column=0, pady=10)
        abrir_archivo_b = ttk.Button(self.pl_options_f, text="Abrir archivo...", command=abrir_archivos)
        abrir_archivo_b.grid(row=1, column=1, pady=10)

        tree_playlist.bind("<Double-Button-1>", lambda e: play())
        tree_playlist.bind("<ButtonPress-1>", on_button_press)
        tree_playlist.bind("<B1-Motion>", on_motion)
        tree_playlist.bind("<ButtonRelease-1>", seleccionar_y_soltar)

        # ____________ . ✰ * Fotos de Album * ✰ . ____________
        album_label = tk.Label(self.songinfo_f, image=self.img_album, borderwidth=0)
        album_label.grid(row=0, column=1, pady=15)"""