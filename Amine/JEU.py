from tkinter import *
from PIL import Image, ImageTk
import random
import json
import os
import sys

# === Chemins relatifs ===
chemin_background = "background.png"
chemin_lancer_piece = "lancer_piece.png"
chemin_pile = "PILE.png"
chemin_face = "FACE.png"
chemin_sauvegarde = "sauvegarde_pile_ou_face.json"

# === Fonctions de sauvegarde ===
def charger_partie():
    if os.path.exists(chemin_sauvegarde):
        with open(chemin_sauvegarde, "r") as f:
            return json.load(f)
    return {
        "victoires": 0,
        "defaites": 0,
        "lancers": 0,
        "pouvoirs": {
            "voir": True,
            "rejouer": True
        },
        "dernier_resultat": None
    }

def sauvegarder_partie(data):
    with open(chemin_sauvegarde, "w") as f:
        json.dump(data, f)

etat_partie = charger_partie()
choix_temporaire = ""
resultat_prevu = None
utilise_rejouer = False

# === Fenêtre principale ===
fenetre = Tk()
fenetre.title("Pile ou Face - Donjon VS Squelette")
fenetre.geometry("800x600")
fenetre.resizable(False, False)

# === Chargement des images ===
try:
    # Ouverture et redimensionnement des images
    background_img = Image.open(chemin_background).resize((800, 600))
    background_photo = ImageTk.PhotoImage(background_img)

    lancer_img = Image.open(chemin_lancer_piece).resize((100, 100))
    lancer_photo = ImageTk.PhotoImage(lancer_img)

    pile_img = Image.open(chemin_pile).resize((100, 100))
    pile_photo = ImageTk.PhotoImage(pile_img)

    face_img = Image.open(chemin_face).resize((100, 100))
    face_photo = ImageTk.PhotoImage(face_img)

except Exception as e:
    print("Erreur de chargement image :", e)
    fenetre.destroy()
    sys.exit()

# === Placement des widgets ===
background_label = Label(fenetre, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

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

# === Fonctions principales ===
def afficher_resultat(resultat_force=None):
    global etat_partie, choix_temporaire, utilise_rejouer

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
    global choix_temporaire, resultat_prevu, utilise_rejouer
    choix_temporaire = choix_joueur.get()
    resultat_label.config(text="Lancer en cours...")
    resultat_image_label.place_forget()
    lancer_label.config(image=lancer_photo)
    lancer_label.place(x=350, y=250)
    dialogue_label.config(text="Suspens...")

    if resultat_prevu:
        fenetre.after(2000, lambda: afficher_resultat(resultat_prevu))
        resultat_prevu = None
    else:
        fenetre.after(2000, afficher_resultat)

    utilise_rejouer = False

def utiliser_voir():
    global resultat_prevu
    if etat_partie["pouvoirs"]["voir"]:
        resultat_prevu = random.choice(["Pile", "Face"])
        dialogue_label.config(text=f"✨ Le squelette va tirer : {resultat_prevu}")
        etat_partie["pouvoirs"]["voir"] = False
        sauvegarder_partie(etat_partie)
    else:
        dialogue_label.config(text="⚠️ Pouvoir déjà utilisé !")

def utiliser_rejouer():
    global utilise_rejouer
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
    global etat_partie
    etat_partie = {
        "victoires": 0,
        "defaites": 0,
        "lancers": 0,
        "pouvoirs": {"voir": True, "rejouer": True},
        "dernier_resultat": None
    }
    sauvegarder_partie(etat_partie)

def effacer_resultat():
    resultat_label.config(text="")
    resultat_image_label.place_forget()
    dialogue_label.config(text="")

# === Boutons ===
Button(fenetre, text="Lancer la pièce", font=("Tiffany", 18),
       command=lancer_piece, bg="black", fg="white").place(x=320, y=520)

Button(fenetre, text="Pouvoir : Voir à l'avance", font=("Tiffany", 12),
       command=utiliser_voir, bg="black", fg="cyan").place(x=20, y=20)

Button(fenetre, text="Pouvoir : Rejouer", font=("Tiffany", 12),
       command=utiliser_rejouer, bg="black", fg="orange").place(x=220, y=20)

Button(fenetre, text="Effacer le résultat", font=("Tiffany", 12),
       command=effacer_resultat, bg="black", fg="white").place(x=600, y=20)

# === Lancement ===
fenetre.mainloop()
