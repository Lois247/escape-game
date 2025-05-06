import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random
import json
import os
from Amine.JEU import background_photo, pile_photo, face_photo, lancer_photo

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
        x_start = 400
        y_pos = 400
        if not (perdu or gagne):
            for i, btn in enumerate(boutons_lettres):
                btn.place(x=x_start + i * (largeur + espacement), y=y_pos)
        btn_reset.place(relx=0.4, rely=0.6)
        btn_quit.place(relx=0.5, rely=0.6)

    def show_sequence():
        if perdu or gagne:
            return
        titre.config(text="Séquence : " + " ".join(sequence))
        jeu.after(1500, lambda: titre.config(text="Reproduis la séquence..."))

    def choix(lettre,):
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
            if len(sequence) == 5:
                root.after(2000, lancer_jeu_pile_ou_face())
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

def lancer_jeu_pile_ou_face():
    chemin_background = "background1.png"
    chemin_lancer_piece = "lancer_piece.png"
    chemin_pile = "PILE.png"
    chemin_face = "FACE.png"
    chemin_sauvegarde = "sauvegarde_pile_ou_face.json"

    fenetre = tk.Tk()
    fenetre.title("Pile ou Face - Donjon VS Squelette")
    fenetre.geometry("800x600")
    fenetre.resizable(False, False)

    def charger_images():
        try:
            background_img = Image.open(chemin_background).resize((800, 600))
            background_photo = ImageTk.PhotoImage(background_img)

            lancer_img = Image.open(chemin_lancer_piece).resize((100, 100))
            lancer_photo = ImageTk.PhotoImage(lancer_img)

            pile_img = Image.open(chemin_pile).resize((100, 100))
            pile_photo = ImageTk.PhotoImage(pile_img)

            face_img = Image.open(chemin_face).resize((100, 100))
            face_photo = ImageTk.PhotoImage(face_img)

            return True
        except Exception as e:
            print("Erreur de chargement image :", e)
            return False

    if not charger_images():
        fenetre.destroy()
        return

    background_label = Label(fenetre, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # au lieu de fenetre.background_photo, etc.
    def charger_partie():
        if os.path.exists(chemin_sauvegarde):
            with open(chemin_sauvegarde, "r") as f:
                return json.load(f)
        return {
            "victoires": 0,
            "defaites": 0,
            "lancers": 0,
            "pouvoirs": {"voir": True, "rejouer": True},
            "dernier_resultat": None
        }

    def sauvegarder_partie(data):
        with open(chemin_sauvegarde, "w") as f:
            json.dump(data, f)

    etat_partie = charger_partie()
    choix_temporaire = ""
    resultat_prevu = None
    utilise_rejouer = False

    resultat_label = Label(fenetre, text="Choisis Pile ou Face !", font=("Tiffany", 20), fg="white", bg="black")
    resultat_label.place(x=270, y=200)

    lancer_label = Label(fenetre, bg="black")
    lancer_label.place_forget()

    resultat_image_label = Label(fenetre, bg="black")
    resultat_image_label.place_forget()

    dialogue_label = Label(fenetre, text="", font=("Tiffany", 14), fg="white", bg="black")
    dialogue_label.place(x=10, y=550)

    choix_joueur = StringVar(value="Pile")
    frame_choix = Frame(fenetre, bg="black")
    frame_choix.place(x=320, y=470)

    Radiobutton(frame_choix, text="Pile", variable=choix_joueur, value="Pile",
                font=("Tiffany", 16), bg="black", fg="white", selectcolor="black").pack(side=LEFT, padx=20)

    Radiobutton(frame_choix, text="Face", variable=choix_joueur, value="Face",
                font=("Tiffany", 16), bg="black", fg="white", selectcolor="black").pack(side=LEFT, padx=20)

    def afficher_resultat(resultat_force=None):
        nonlocal etat_partie, choix_temporaire, utilise_rejouer

        lancer_label.place_forget()
        resultat = resultat_force if resultat_force else random.choice(["Pile", "Face"])
        etat_partie["dernier_resultat"] = resultat

        if resultat == "Pile":
            resultat_image_label.config(image=pile_photo)
        else:
            resultat_image_label.config(image=face_photo)
        resultat_image_label.place(x=350, y=270)

        if choix_temporaire == resultat:
            etat_partie["victoires"] += 1
            message = f"Bravo ! Le squelette a lancé {resultat}.\nVictoires : {etat_partie['victoires']} / Défaites : {etat_partie['defaites']}"
        else:
            etat_partie["defaites"] += 1
            message = f"Perdu... Le squelette avait {resultat}.\nVictoires : {etat_partie['victoires']} / Défaites : {etat_partie['defaites']}"

        resultat_label.config(text=message)
        dialogue_label.config(text=random.choice([
            "Le destin a parlé !",
            "La pièce est tombée...",
            "Quel suspense !",
            "Tu as tenté ta chance."
        ]))

        if not utilise_rejouer:
            etat_partie["lancers"] += 1

        sauvegarder_partie(etat_partie)
        check_fin_partie()

    def lancer_piece():
        nonlocal choix_temporaire, resultat_prevu, utilise_rejouer
        choix_temporaire = choix_joueur.get()
        resultat_label.config(text="Lancer en cours...")
        resultat_image_label.place_forget()
        lancer_label.config(image=lancer_photo)
        lancer_label.place(x=350, y=250)
        dialogue_label.config(text="Suspens...")

        if resultat_prevu:
            temp_resultat = resultat_prevu
            resultat_prevu = None
            fenetre.after(2000, lambda: afficher_resultat(temp_resultat))
        else:
            fenetre.after(2000, afficher_resultat)

        utilise_rejouer = False

    def utiliser_voir():
        nonlocal resultat_prevu
        if etat_partie["pouvoirs"]["voir"]:
            resultat_prevu = random.choice(["Pile", "Face"])
            dialogue_label.config(text=f"✨ Le squelette va tirer : {resultat_prevu}")
            etat_partie["pouvoirs"]["voir"] = False
            sauvegarder_partie(etat_partie)
        else:
            dialogue_label.config(text="⚠️ Pouvoir déjà utilisé !")

    def utiliser_rejouer():
        nonlocal utilise_rejouer
        if etat_partie["pouvoirs"]["rejouer"] and etat_partie["dernier_resultat"]:
            etat_partie["lancers"] -= 1
            if choix_joueur.get() == etat_partie["dernier_resultat"]:
                etat_partie["victoires"] -= 1
            else:
                etat_partie["defaites"] -= 1
            utilise_rejouer = True
            etat_partie["pouvoirs"]["rejouer"] = False
            sauvegarder_partie(etat_partie)
            dialogue_label.config(text="🔄 Tour annulé. Relance disponible !")
            resultat_label.config(text="Résultat annulé.")
            resultat_image_label.place_forget()
        else:
            dialogue_label.config(text="⚠️ Rejouer déjà utilisé ou pas de tour précédent.")

    def check_fin_partie():
        if etat_partie["victoires"] == 3:
            resultat_label.config(text="💪 Tu as vaincu le squelette !")
            dialogue_label.config(text="Tu m'as battu... Impossible !")
            reset_partie()
        elif etat_partie["lancers"] == 5:
            if etat_partie["victoires"] > etat_partie["defaites"]:
                resultat_label.config(text="🏆 Tu as survécu au donjon !")
                dialogue_label.config(text="Tu es plus rusé que prévu.")
            else:
                resultat_label.config(text="💀 GAME OVER. Le squelette t’a eu.")
                dialogue_label.config(text="À la prochaine, humain !")
            reset_partie()

    def reset_partie():
        nonlocal etat_partie
        etat_partie = {
            "victoires": 0,
            "defaites": 0,
            "lancers": 0,
            "pouvoirs": {"voir": True, "rejouer": True},
            "dernier_resultat": None
        }
        sauvegarder_partie(etat_partie)

    Button(fenetre, text="Lancer la pièce", font=("Tiffany", 18),
           command=lancer_piece, bg="black", fg="white").place(x=320, y=520)

    Button(fenetre, text="Pouvoir : Voir à l'avance", font=("Tiffany", 12),
           command=utiliser_voir, bg="black", fg="cyan").place(x=20, y=20)

    Button(fenetre, text="Pouvoir : Rejouer", font=("Tiffany", 12),
           command=utiliser_rejouer, bg="black", fg="orange").place(x=220, y=20)

    fenetre.mainloop()

# === Fenêtre principale ===
root = tk.Tk()
root.geometry("800x500")
root.title("Jeu d'énigmes et de séquences")

boutons = []
lancer_interface()

root.mainloop()