import json

class Library:
    def __init__(self):
        self.canciones = []

    def load_json(self):
        try:
            with open("songs.json", "r", encoding="utf-8") as f:
                self.canciones = json.load(f)
        except FileNotFoundError:
            self.canciones = []

    def save_json(self):
        with open("songs.json", "w", encoding="utf-8") as f:
            json.dump(self.canciones, f, indent=4)