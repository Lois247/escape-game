import random
import tkinter as tk
from PIL import Image, ImageTk

lettres = ['E', 'S', 'C', 'A', 'P']
sequence = []
user_input = []
perdu = False  # indique si le joueur a perdu
gagne = False  # indique si le joueur a gagné

def debut_de_la_partie():
    global sequence, user_input, perdu, gagne
    if perdu or gagne:  # ne commence pas une nouvelle séquence si le jeu est terminé
        return
    user_input = []
    sequence.append(random.choice(lettres))
    show_sequence()

def show_sequence():
    if perdu or gagne:  # n'afficher la séquence si le joueur a perdu ou gagné
        return
    titre.config(text="Séquence : " + " ".join(sequence))
    root.after(1500, lambda: titre.config(text="Reproduis la séquence..."))

def choix(lettre):
    global sequence, user_input, perdu, gagne
    if perdu or gagne:  # ne permet pas de choix si le jeu est terminé
        return
    user_input.append(lettre)
    if user_input == sequence:
        if len(sequence) == 5:
            background_label.config(image=bg_win)
            titre.config(text="Bravo ! Tu as gagné le jeu")
            gagne = True
            cacher_boutons()
            afficher_boutons()  # Réaffiche les boutons Reset et Quitter
        else:
            titre.config(text="Bravo ! Nouvelle séquence...")
            root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        titre.config(text="Perdu ! La séquence était : " + " ".join(sequence) + "\nClique sur Reset ou Quitter.")
        background_label.config(image=bg_lose)
        perdu = True
        cacher_boutons()  # Cacher les boutons de lettres quand on perd
        afficher_boutons()  # Réafficher les boutons Reset et Quitter

def cacher_boutons():
    for btn in boutons_lettres:
        btn.place_forget()  # Masquer les boutons de lettres
    btn_reset.place_forget()
    btn_quit.place_forget()

def reset_game():
    global sequence, user_input, perdu, gagne
    sequence = []
    user_input = []
    perdu = False
    gagne = False  # Réinitialiser la variable gagne
    background_label.config(image=bg_normal)
    afficher_boutons()
    debut_de_la_partie()

def afficher_boutons():
    largeur_bouton = 100
    espacement = 60
    total_width = len(lettres) * largeur_bouton + (len(lettres) - 1) * espacement
    x_start = (root.winfo_width() - total_width) // 2
    y_pos = 400

    # centrer les boutons lettres uniquement après un reset
    if not (perdu or gagne):  # Ne pas afficher les boutons lettres après une perte ou une victoire
        for i, btn in enumerate(boutons_lettres):
            btn.place(x=x_start + i * (largeur_bouton + espacement), y=y_pos)

    # centrer les boutons Reset et Quitter en dessous
    total_buttons_width = 2 * 80 + 20  # largeur boutons + espacement
    x_start_buttons = (root.winfo_width() - total_buttons_width) // 2
    btn_reset.place(x=x_start_buttons, y=550)
    btn_quit.place(x=x_start_buttons + 100, y=550)

# créer la fenêtre
root = tk.Tk()
root.title("Jeu de séquence")
root.geometry("1920x1080")

# charger les images de fond
bg_normal = ImageTk.PhotoImage(Image.open("backgbl.png"))
bg_win = ImageTk.PhotoImage(Image.open("win.png"))
bg_lose = ImageTk.PhotoImage(Image.open("lose.png"))

# fond
background_label = tk.Label(root, image=bg_normal)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# titre
titre = tk.Label(root, text="Bienvenue dans le jeu de séquence !", font=("Old English Text MT", 20), bg="#4e4b3e", fg="#e2d1b3", relief="raised", bd=10,  highlightbackground="#d4af37", highlightcolor="#f2d45f")
titre.place(relx=0.5, y=30, anchor="n")

# boutons lettres
boutons_lettres = []
for lettre in lettres:
    btn = tk.Button(root, text=lettre,font=("Old English Text MT", 30), bg="#4e4b3e", fg="#e2d1b3", relief="raised", bd=10,  highlightbackground="#d4af37", highlightcolor="#f2d45f", command=lambda l=lettre: choix(l))
    boutons_lettres.append(btn)

# boutons Reset et Quitter
btn_reset = tk.Button(root, text="Reset", font=("Old English Text MT", 15), bg="#4e4b3e", fg="#e2d1b3", relief="raised", bd=10,  highlightbackground="#d4af37", highlightcolor="#f2d45f", command=reset_game)
btn_quit = tk.Button(root, text="Quitter", font=("Old English Text MT", 15), bg="#4e4b3e", fg="#e2d1b3", relief="raised", bd=10,  highlightbackground="#d4af37", highlightcolor="#f2d45f", command=root.quit)

# afficher les boutons après que la fenêtre soit prête
root.update_idletasks()
afficher_boutons()

# démarrer le jeu
debut_de_la_partie()

root.mainloop()


