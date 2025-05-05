import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os

# === Données des énigmes ===
toutes_les_enigmes = {
    "Je suis toujours devant toi mais jamais derrière. Qui suis-je ?":
    {"Le passé": False, "L’avenir": True, "L’ombre": False},
    "Je parle sans bouche et j’entends sans oreilles. Que suis-je ?":
    {"Un écho": True, "Un livre": False, "Le vent": False},
    "Je peux être cassé sans être touché. Que suis-je ?":
    {"Une promesse": True, "Un miroir": False, "Une ombre": False},
    "Je tombe sans jamais me blesser. Que suis-je ?":
    {"La nuit": True, "La pluie": False, "La température": False},
    "Je suis pris avant que vous ne me donniez. Que suis-je ?":
    {"Une photo": True, "Une promesse": False, "Une claque": False},
    "Je n’ai qu’un œil mais je ne vois pas. Que suis-je ?":
    {"Une aiguille": True, "Un cyclone": False, "Un pirate": False}
}

# === Variables du jeu ===
nb_question = 0
liste_enigmes = []
reponses_courantes = []

def reset_enigmes():
    global nb_question, liste_enigmes
    nb_question = 0
    liste_enigmes = random.sample(list(toutes_les_enigmes.items()), 3)
    label_question.config(text="Clique sur ▶️ Commencer pour débuter !")
    for b in boutons:
        b.config(text="", state="disabled")
    bouton_start.config(state="normal")

def commencer_jeu():
    bouton_start.config(state="disabled")
    nouvelle_enigme()

def nouvelle_enigme():
    global nb_question, reponses_courantes
    if nb_question == 3:
        afficher_fin_enigme(victoire=True)
        return
    enigme, reponses = liste_enigmes[nb_question]
    reponses_courantes = list(reponses.items())
    random.shuffle(reponses_courantes)
    label_question.config(text=f"Énigme {nb_question + 1} :\n{enigme}")
    for i, (texte, _) in enumerate(reponses_courantes):
        boutons[i].config(text=texte, state="normal", command=lambda i=i: verifier_reponse(i))

def verifier_reponse(index):
    global nb_question
    _, est_bonne = reponses_courantes[index]
    if est_bonne:
        nb_question += 1
        nouvelle_enigme()
    else:
        afficher_fin_enigme(victoire=False)

def afficher_fin_enigme(victoire=True):
    for widget in root.winfo_children():
        widget.destroy()
    image_path = "victoire.png" if victoire else "defaite.png"
    image = Image.open(image_path).resize((800, 500))
    bg = ImageTk.PhotoImage(image)
    label_img = tk.Label(root, image=bg)
    label_img.image = bg
    label_img.place(x=0, y=0, relwidth=1, relheight=1)

    if victoire:
        root.after(2000, lancer_jeu_sequence)
    else:
        bouton_restart = tk.Button(
            root, text="REJOUER", font=("Helvetica", 14, "bold"),
            bg="#dc143c", fg="white", bd=4, command=restart_game
        )
        bouton_restart.place(x=350, y=430)

def restart_game():
    for widget in root.winfo_children():
        widget.destroy()
    lancer_interface()

def lancer_interface():
    global label_question, boutons, bouton_start
    bg = ImageTk.PhotoImage(Image.open("background.png").resize((800, 500)))
    label_bg = tk.Label(root, image=bg)
    label_bg.image = bg
    label_bg.place(x=0, y=0, relwidth=1, relheight=1)

    label_question = tk.Label(root, text="", font=("Helvetica", 16), wraplength=700, bg="#000000", fg="white")
    label_question.place(x=50, y=30)

    boutons.clear()
    for i in range(3):
        btn = tk.Button(root, text="", font=("Georgia", 12, "bold"), width=40,
                        bg="#f7ecd0", fg="#3a2e1e", bd=5)
        btn.place(x=150, y=150 + i * 60)
        boutons.append(btn)

    bouton_start = tk.Button(root, text="▶️ Commencer", font=("Georgia", 13, "bold"),
                             bg="#f7ecd0", fg="#3a2e1e", bd=5, command=commencer_jeu)
    bouton_start.place(x=320, y=400)

    reset_enigmes()

# === Jeu de séquence (s'ouvre après victoire) ===
def lancer_jeu_sequence():
    lettres = ['E', 'S', 'C', 'A', 'P']
    sequence = []
    user_input = []
    perdu = False
    gagne = False

    jeu = tk.Toplevel()
    jeu.geometry("1536x1024")
    jeu.title("Jeu de Séquence")

    bg_normal = ImageTk.PhotoImage(Image.open("backgbl.png"))
    bg_win = ImageTk.PhotoImage(Image.open("win.png"))
    bg_lose = ImageTk.PhotoImage(Image.open("lose.png"))

    background_label = tk.Label(jeu, image=bg_normal)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    titre = tk.Label(jeu, text="Bienvenue dans le jeu de séquence !", font=("Old English Text MT", 20),
                     bg="#4e4b3e", fg="#e2d1b3", bd=10)
    titre.place(relx=0.5, y=30, anchor="n")

    boutons_lettres = []
    def cacher_boutons():
        for btn in boutons_lettres:
            btn.place_forget()
        btn_reset.place_forget()
        btn_quit.place_forget()

    def afficher_boutons():
        largeur = 100
        espacement = 60
        total = len(lettres) * largeur + (len(lettres) - 1) * espacement
        x_start = (jeu.winfo_width() - total) // 2
        y_pos = 400
        if not (perdu or gagne):
            for i, btn in enumerate(boutons_lettres):
                btn.place(x=x_start + i * (largeur + espacement), y=y_pos)
        x_start_btns = (jeu.winfo_width() - 180) // 2
        btn_reset.place(x=x_start_btns, y=550)
        btn_quit.place(x=x_start_btns + 100, y=550)

    def show_sequence():
        if perdu or gagne:
            return
        titre.config(text="Séquence : " + " ".join(sequence))
        jeu.after(1500, lambda: titre.config(text="Reproduis la séquence..."))

    def choix(lettre):
        nonlocal perdu, gagne
        if perdu or gagne:
            return
        user_input.append(lettre)
        if user_input == sequence:
            if len(sequence) == 5:
                background_label.config(image=bg_win)
                titre.config(text="Bravo ! Tu as gagné le jeu")
                gagne = True
                cacher_boutons()
                afficher_boutons()
                root.after(2000, lancer_jeu_pile_ou_face)  # Transition vers le jeu Pile ou Face
            else:
                titre.config(text="Bravo ! Nouvelle séquence...")
                jeu.after(1000, debut_partie)
        elif not sequence[:len(user_input)] == user_input:
            titre.config(text="Perdu ! La séquence était : " + " ".join(sequence))
            background_label.config(image=bg_lose)
            perdu = True
            cacher_boutons()
            afficher_boutons()

    def debut_partie():
        if perdu or gagne:
            return
        user_input.clear()
        sequence.append(random.choice(lettres))
        show_sequence()

    def reset():
        nonlocal perdu, gagne, sequence, user_input
        sequence = []
        user_input = []
        perdu = False
        gagne = False
        background_label.config(image=bg_normal)
        afficher_boutons()
        debut_partie()

    for lettre in lettres:
        btn = tk.Button(jeu, text=lettre, font=("Old English Text MT", 30), bg="#4e4b3e", fg="#e2d1b3",
                        bd=10, command=lambda l=lettre: choix(l))
        boutons_lettres.append(btn)

    btn_reset = tk.Button(jeu, text="Reset", font=("Old English Text MT", 20), bg="#4e4b3e", fg="#e2d1b3", bd=10, command=reset)
    btn_quit = tk.Button(jeu, text="Quitter", font=("Old English Text MT", 20), bg="#e2d1b3", fg="#4e4b3e", bd=10, command=jeu.destroy)
    afficher_boutons()
    debut_partie()

# === Jeu de Pile ou Face (version corrigée) ===
def lancer_jeu_pile_ou_face():
    def choix(choix_utilisateur):
        face_ou_pile = random.choice(["Pile", "Face"])
        if choix_utilisateur == face_ou_pile:
            message.config(text=f"Bravo ! C'était {face_ou_pile}. Vous avez gagné !", fg="green")
        else:
            message.config(text=f"Dommage ! C'était {face_ou_pile}. Vous avez perdu !", fg="red")

    jeu_pile_ou_face = tk.Toplevel()
    jeu_pile_ou_face.geometry("500x300")
    jeu_pile_ou_face.title("Pile ou Face")

    message = tk.Label(jeu_pile_ou_face, text="Choisissez Pile ou Face", font=("Helvetica", 18), bg="lightblue")
    message.pack(pady=30)

    bouton_pile = tk.Button(jeu_pile_ou_face, text="Pile", font=("Helvetica", 14), command=lambda: choix("Pile"))
    bouton_pile.pack(side="left", padx=50)

    bouton_face = tk.Button(jeu_pile_ou_face, text="Face", font=("Helvetica", 14), command=lambda: choix("Face"))
    bouton_face.pack(side="right", padx=50)

# === Fenêtre principale ===
root = tk.Tk()
root.geometry("800x500")
root.title("Jeu d'énigmes et de séquences")

boutons = []
lancer_interface()

root.mainloop()
