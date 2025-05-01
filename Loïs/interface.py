import random
import tkinter as tk
from tkinter import PhotoImage

lettres = ['E', 'S', 'C', 'A', 'P']

sequence = []
user_input = []
perdu = False

def debut_de_la_partie():
    global sequence, user_input, perdu
    if perdu:
        return
    user_input = []
    sequence.append(random.choice(lettres))
    show_sequence()

def show_sequence():
    titre.config(text="Séquence : " + " ".join(sequence))
    root.after(1500, lambda: titre.config(text="Reproduis la séquence..."))

def choix(lettre):
    global sequence, user_input, perdu
    if perdu:
        return

    user_input.append(lettre)
    if user_input == sequence:
        titre.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        titre.config(text="Perdu ! La séquence était : " + " ".join(sequence) + "\nClique sur Reset ou Quitter.")
        perdu = True

def reset_game():
    global sequence, user_input, perdu
    sequence = []
    user_input = []
    perdu = False
    debut_de_la_partie()

# --- Interface Tkinter ---
root = tk.Tk()
root.title("Jeu de séquence")
root.geometry("350x250")

# --- Image de fond ---
bg_image = PhotoImage(file="backgbl.png")  # Remplace "ton_image.png" par le nom exact du fichier
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Étire l'image sur toute la fenêtre

# --- Widgets ---
titre = tk.Label(root, text="Bienvenue dans le jeu de séquence !", font=("Arial", 12), bg="#ffffff")
titre.pack(pady=10)

frame_lettres = tk.Frame(root, bg="#ffffff")
frame_lettres.pack(pady=10)

for lettre in lettres:
    bouton = tk.Button(frame_lettres, text=lettre, width=4, height=2, font=("Arial", 12),
                       command=lambda l=lettre: choix(l))
    bouton.pack(side=tk.LEFT, padx=5)

frame_control = tk.Frame(root, bg="#ffffff")
frame_control.pack(pady=20)

btn_reset = tk.Button(frame_control, text="Reset", command=reset_game)
btn_reset.pack(side=tk.LEFT, padx=20)

btn_quit = tk.Button(frame_control, text="Quitter", command=root.quit)
btn_quit.pack(side=tk.RIGHT, padx=20)

# Démarrage du jeu
debut_de_la_partie()

root.mainloop()
