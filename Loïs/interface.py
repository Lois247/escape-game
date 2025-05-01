import random
import tkinter as tk
from PIL import Image, ImageTk

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
        if len(sequence) == 5:
            titre.config(text="Bravo ! Tu as gagné le jeu ! 🎉")
            background_label.config(image=bg_win)
            cacher_boutons()
        else:
            titre.config(text="Bravo ! Nouvelle séquence...")
            root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        titre.config(text="Perdu ! La séquence était : " + " ".join(sequence) + "\nClique sur Reset ou Quitter.")
        background_label.config(image=bg_lose)
        perdu = True
        cacher_boutons()

def cacher_boutons():
    frame_central.place_forget()

def reset_game():
    global sequence, user_input, perdu
    sequence = []
    user_input = []
    perdu = False
    background_label.config(image=bg_normal)
    frame_central.place(relx=0.5, rely=0.5, anchor="center")  # Réaffiche les boutons centrés
    debut_de_la_partie()

# Créer la fenêtre
root = tk.Tk()
root.title("Jeu de séquence")
root.geometry("1920x980")

# Charger les images de fond
bg_normal = ImageTk.PhotoImage(Image.open("backgbl.png"))
bg_win = ImageTk.PhotoImage(Image.open("win.png"))
bg_lose = ImageTk.PhotoImage(Image.open("lose.png"))

# Image de fond
background_label = tk.Label(root, image=bg_normal)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame central pour centrer tous les éléments
frame_central = tk.Frame(root)  # Pas de fond spécifié
frame_central.place(relx=0.5, rely=0.5, anchor="center")

# Titre
titre = tk.Label(frame_central, text="Bienvenue dans le jeu de séquence !", font=("Arial", 14), bg="#ffffff")
titre.pack(pady=10)

# Lettres
frame_lettres = tk.Frame(frame_central)  # Pas de fond spécifié
frame_lettres.pack(pady=10)

for lettre in lettres:
    bouton = tk.Button(frame_lettres, text=lettre, width=4, height=2, font=("Arial", 12),
                       command=lambda l=lettre: choix(l), bg="SystemButtonFace", highlightthickness=0, relief="flat", bd=0)
    bouton.pack(side=tk.LEFT, padx=5, pady=5)

# Contrôles
frame_control = tk.Frame(frame_central)  # Pas de fond spécifié
frame_control.pack(pady=20)

btn_reset = tk.Button(frame_control, text="Reset", command=reset_game, bg="SystemButtonFace", highlightthickness=0, relief="flat", bd=0)
btn_reset.pack(side=tk.LEFT, padx=20)

btn_quit = tk.Button(frame_control, text="Quitter", command=root.quit, bg="SystemButtonFace", highlightthickness=0, relief="flat", bd=0)
btn_quit.pack(side=tk.RIGHT, padx=20)

# Démarrer le jeu
debut_de_la_partie()

root.mainloop()
