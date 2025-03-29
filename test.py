import tkinter as tk
import random
import os
from tkinter import PhotoImage

symboles = ['𝖊', '𝖘', '𝖈', '𝖆', '𝖕', '𝖊']
sequence = []
user_input = []
buttons = {}

# Obtenir le chemin absolu du dossier d'images
chemin_images = os.path.join(os.path.dirname(__file__), "images")

# Initialisation de l'interface graphique
root = tk.Tk()
root.title("Jeu de Séquence Médiéval")
root.geometry("1080x980")

label = tk.Label(root, text="Reproduis la séquence", font=("Old English Text MT", 14), fg="#5a3e1b")
label.pack(pady=10)

display = tk.Label(root, text="", font=("Old English Text MT", 20), fg="#8b4513")
display.pack(pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack()

# Charger une image spécifique pour chaque symbole
button_images = {}
for symbol in symboles:
    image_path = os.path.join(chemin_images, f"wood_button_{symbol}.png")
    if os.path.exists(image_path):  # Vérifier si l'image existe
        button_images[symbol] = PhotoImage(file=image_path)
    else:
        print(f"⚠ Image non trouvée pour {symbol} : {image_path}")
        button_images[symbol] = None  # Pas d'image disponible

def debut_de_la_partie():
    global sequence, user_input
    user_input = []
    sequence.append(random.choice(symboles))
    show_sequence()

def show_sequence():
    display.config(text=" ".join(sequence))
    root.after(2000, lambda: display.config(text=""))

def user_click(symbol):
    global sequence, user_input
    user_input.append(symbol)
    if user_input == sequence:
        label.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        label.config(text="Perdu ! Réessaye.")
        sequence = []

start_button = tk.Button(root, text="Nouvelle séquence", command=debut_de_la_partie, font=("Old English Text MT", 12),
                         bd=0, fg="white", bg="#8b5a2b", activebackground="#a67c52")
start_button.pack(pady=10)

# Lancer le jeu
root.mainloop()