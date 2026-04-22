import tkinter as tk
from app import Luliiapp

def main():
    root = tk.Tk()  
    root.title("✩ + . * Luliify * . + ✩")
    root.geometry("1200x510")
    root.resizable(False, False)
    app = Luliiapp(root)
    root.mainloop()

if __name__ == "__main__":
    main()