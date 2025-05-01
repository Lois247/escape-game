from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import random

# === Liste des énigmes et leurs réponses ===
toutes_les_enigmes = {
    "Je suis toujours devant toi mais jamais derrière. Qui suis-je ?":
    {"Le passé": False, "L’avenir": True, "L’ombre": False},

    "Je suis toujours en train de courir, mais je ne vais jamais nulle part. Que suis-je ?":
    {"Un cercle": True, "Une rivière": False, "Le vent": False},

    "Je parle sans bouche et j’entends sans oreilles. Que suis-je ?":
    {"Un écho": True, "Un livre": False, "Le vent": False},

    "Je peux être cassé sans être touché. Que suis-je ?":
    {"Une promesse": True, "Un miroir": False, "Une ombre": False},

    "Plus tu en prends, plus tu laisses derrière toi. Que suis-je ?":
    {"Des empreintes": True, "Le vent": False, "Un secret": False},

    "On me trouve une fois dans une minute, deux fois dans un moment, mais jamais dans cent ans. Que suis-je ?":
    {"La lettre 'm'": True, "Le temps": False, "Le destin": False},

    "Je grandis sans vie, j’ai des racines sans feuilles. Que suis-je ?":
    {"Un arbre généalogique": True, "Une montagne": False, "Un fossile": False},

    "Je suis petit au début, mais je peux détruire des villes entières. Que suis-je ?":
    {"Une étincelle": True, "Une tornade": False, "Un secret": False},

    "Je n’ai pas de clé mais j’ouvre tout. Que suis-je ?":
    {"Un mot de passe": True, "Un sourire": False, "Un coffre": False},

    "Je suis pris avant que vous ne me donniez. Que suis-je ?":
    {"Une photo": True, "Une promesse": False, "Une claque": False},

    "J’ai des aiguilles mais je ne pique pas. Que suis-je ?":
    {"Une montre": True, "Une boussole": False, "Un sapin": False},

    "Je suis là sans y être, on me voit mais on ne me touche pas. Que suis-je ?":
    {"Un mirage": True, "Une illusion": False, "Une ombre": False},

    "Je ne parle qu’une fois que l’on m’a frappé. Que suis-je ?":
    {"Une cloche": True, "Un tambour": False, "Un enfant": False},

    "Je peux remplir une pièce mais je ne prends pas de place. Que suis-je ?":
    {"La lumière": True, "Le vide": False, "L’odeur": False},

    "Je tombe sans jamais me blesser. Que suis-je ?":
    {"La nuit": True, "La pluie": False, "La température": False},

    "Je n’ai qu’un œil mais je ne vois pas. Que suis-je ?":
    {"Une aiguille": True, "Un cyclone": False, "Un pirate": False},

    "Plus je sèche, plus je deviens mouillée. Que suis-je ?":
    {"Une serviette": True, "Un nuage": False, "La pluie": False},

    "Je n’ai pas de vie, mais je peux mourir si on m’oublie. Que suis-je ?":
    {"Un souvenir": True, "Une flamme": False, "Une étoile": False},

    "Je n’ai pas de jambes mais je peux courir. Que suis-je ?":
    {"L’eau": True, "Le sable": False, "Le vent": False},

    "Je possède des pages mais je ne suis pas un livre. Que suis-je ?":
    {"Un calendrier": True, "Une bibliothèque": False, "Un journal": False},

    "Je peux être élevé sans jamais tomber. Que suis-je ?":
    {"Le ton": True, "Un ballon": False, "Une fusée": False},

    "Je n’ai pas de bouche mais je murmure. Je n’ai pas d’oreilles mais je suis entendu. Que suis-je ?":
    {"Le vent": True, "Un fantôme": False, "Le silence": False},

    "Je suis invisible, mais tout le monde peut me sentir. Que suis-je ?":
    {"Le vent": True, "La peur": False, "L’âme": False},

    "Je suis parfois chaud, parfois froid. Je peux brûler sans feu et geler sans glace. Que suis-je ?":
    {"Le vent": True, "La colère": False, "Le regard": False},

    "Je monte mais je ne redescends jamais. Que suis-je ?":
    {"L’âge": True, "Une fusée": False, "La fièvre": False},

    "J’ai un cou mais pas de tête, deux bras mais pas de mains. Que suis-je ?":
    {"Une chemise": True, "Un fantôme": False, "Une ombre": False},

    "Je commence la nuit et finis le matin, mais je ne suis ni l’un ni l’autre. Que suis-je ?":
    {"Un rêve": True, "Une étoile": False, "Le sommeil": False},

    "Je peux te porter sans te toucher, t’élever sans te tenir. Que suis-je ?":
    {"La musique": True, "Le vent": False, "Un rêve": False},

    "J’apparais une fois par an, mais je marque un nouveau départ. Que suis-je ?":
    {"Le Nouvel An": True, "Une fête": False, "Un anniversaire": False},

    "Je suis plein de trous mais je retiens l’eau. Que suis-je ?":
    {"Une éponge": True, "Un filet": False, "Une passoire": False}
}



# === Variables globales ===
nb_question = 0
liste_enigmes = []
reponses_courantes = []

# === Fonction pour réinitialiser le jeu ===
def reset():
    global nb_question, liste_enigmes
    nb_question = 0
    liste_enigmes = random.sample(list(toutes_les_enigmes.items()), 3)
    label_question.config(text="Clique sur ▶️ Commencer pour débuter !")
    for b in boutons:
        b.config(text="", state="disabled")
    bouton_start.config(state="normal")

# === Fonction appelée quand on clique sur "Commencer" ===
def commencer_jeu():
    bouton_start.config(state="disabled")
    nouvelle_enigme()

# === Affiche une nouvelle énigme ===
def nouvelle_enigme():
    global nb_question, reponses_courantes

    if nb_question == 3:
        afficher_fin(victoire=True)
        return

    enigme_courante, reponses = liste_enigmes[nb_question]
    reponses_courantes = list(reponses.items())
    random.shuffle(reponses_courantes)

    label_question.config(text=f"Énigme {nb_question + 1} :\n{enigme_courante}")
    for i, (texte, _) in enumerate(reponses_courantes):
        boutons[i].config(text=texte, state="normal", command=lambda i=i: verifier_reponse(i))

# === Vérifie si la réponse est bonne ou non ===
def verifier_reponse(index):
    global nb_question
    _, est_bonne = reponses_courantes[index]
    if est_bonne:
        nb_question += 1
        nouvelle_enigme()
    else:
        afficher_fin(victoire=False)

# === Affiche l'image de fin (victoire ou défaite) ===
def afficher_fin(victoire=True):
    for widget in root.winfo_children():
        widget.destroy()

    image_path = "victoire.png" if victoire else "defaite.png"
    image = Image.open(image_path).resize((800, 500))
    bg_fin = ImageTk.PhotoImage(image)
    label_image = tk.Label(root, image=bg_fin)
    label_image.image = bg_fin  # évite que l'image disparaisse
    label_image.place(x=0, y=0, relwidth=1, relheight=1)

    # Si le joueur a perdu, on affiche un bouton pour rejouer
    if not victoire:
        bouton_restart = tk.Button(
            root,
            text="REJOUER",
            font=("Helvetica", 14, "bold"),
            bg="#dc143c",       # rouge carmin
            fg="white",         # texte blanc
            activebackground="#ff4d6d",
            activeforeground="white",
            relief="raised",
            bd=4,
            cursor="hand2",
            command=restart_game
        )
        bouton_restart.place(x=350, y=430)

# === Fonction pour relancer le jeu après défaite ===
def restart_game():
    for widget in root.winfo_children():
        widget.destroy()
    lancer_interface()

# === Crée l'interface principale du jeu ===
def lancer_interface():
    global root, label_question, boutons, bouton_start

    root.title("Jeu des Énigmes")
    root.geometry("800x500")
    root.resizable(False, False)

    bg_image = Image.open("background.png").resize((800, 500))
    bg = ImageTk.PhotoImage(bg_image)
    label_bg = tk.Label(root, image=bg)
    label_bg.image = bg
    label_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Texte de la question
    label_question = tk.Label(root, text="", font=("Helvetica", 16), wraplength=700, bg="#000000", fg="white")
    label_question.place(x=50, y=30)

    # Boutons pour les choix
    boutons = []
    for i in range(3):
        btn = tk.Button(
            root,
            text="",
            font=("Georgia", 12, "bold"),
            width=40,
            bg="#f7ecd0",
            fg="#3a2e1e",
            activebackground="#e0d1aa",
            activeforeground="#2c1e12",
            relief="groove",
            bd=5,
            cursor="hand2"
        )
        btn.place(x=150, y=150 + i * 60)
        boutons.append(btn)

    # Bouton pour commencer
    bouton_start = tk.Button(
        root,
        text="▶️ Commencer",
        font=("Georgia", 13, "bold"),
        bg="#f7ecd0",
        fg="#3a2e1e",
        activebackground="#e0d1aa",
        activeforeground="#2c1e12",
        relief="groove",
        bd=5,
        cursor="hand2",
        command=commencer_jeu
    )
    bouton_start.place(x=320, y=400)

    reset()

# === Lancement du jeu ===
root = tk.Tk()
lancer_interface()
root.mainloop()
