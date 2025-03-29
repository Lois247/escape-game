import tkinter as tk
import random
import os
from PIL import Image, ImageTk

lettre = ['𝖊', '𝖘', '𝖈', '𝖆', '𝖕',]
sequence = []
user_input = []
buttons = {}

# Initialisation de l'interface graphique
root = tk.Tk()
root.title("Jeu de Séquence Médiéval")
root.geometry("1080x808")

# Charger l'image de fond médiéval
base_dir = os.path.dirname(os.path.abspath(__file__))
chemin_images = os.path.join(base_dir, "images")  # Dossier "images"
background_image_path = os.path.join(chemin_images, "fond_medieval.jpg")

if os.path.exists(background_image_path):  # Vérifier que l'image existe
    bg_img = Image.open(background_image_path)
    bg_img_tk = ImageTk.PhotoImage(bg_img)
else:
    print(f"❌ Échec du chargement de l'image de fond : {background_image_path}")
    bg_img_tk = None

# Créer un Canvas pour le fond
canvas = tk.Canvas(root, width=1080, height=980)
canvas.pack()

# Ajouter l'image de fond au Canvas si elle existe
if bg_img_tk:
    canvas.create_image(0, 0, anchor="nw", image=bg_img_tk)

# Créer un Frame par-dessus le Canvas pour les autres éléments
frame = tk.Frame(root, bg="#8b5a2b")
frame.place(x=0, y=0, relwidth=1, relheight=1)

# Labels et boutons
label = tk.Label(frame, text="Reproduis la séquence", font=("Old English Text MT", 18), fg="#5a3e1b")
label.pack(pady=10)

display = tk.Label(frame, text="", font=("Old English Text MT", 20), fg="#8b4513")
display.pack(pady=10)

buttons_frame = tk.Frame(frame)
buttons_frame.pack()

lettre_mapping = {
    '𝖊': 'e',
    '𝖘': 's',
    '𝖈': 'c',
    '𝖆': 'a',
    '𝖕': 'p',
}

lettre = list(lettre_mapping.keys())  # Liste des symboles médiévaux utilisés
button_images = {}

# Chargement des images des boutons
for symbol in lettre:
    filename = f"wood_button_{lettre_mapping[symbol]}.png"
    image_path = os.path.join(chemin_images, filename)

    if os.path.exists(image_path):  # Vérifier que l'image existe
        img = Image.open(image_path)
        img = img.resize((80, 80))  # Redimensionner l'image
        button_images[symbol] = ImageTk.PhotoImage(img)
    else:
        button_images[symbol] = None

# Création des boutons avec des images et du texte
def user_click(lettre):
    global sequence, user_input
    user_input.append(lettre)
    if user_input == sequence:
        label.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        label.config(text="Perdu ! Réessaye.")
        sequence = []

for symbol in lettre:
    btn = tk.Button(
        buttons_frame,
        text=symbol,  # Afficher la lettre
        font=("Old English Text MT", 20),
        command=lambda s=symbol: user_click(s),
        image=button_images[symbol] if button_images[symbol] else None,  # Utiliser l'image si disponible
        compound="top",  # Affiche le texte au-dessus de l'image
        bd=0,
        fg="white",
        bg="#8b5a2b",
        activebackground="#a67c52"
    )
    btn.pack(side=tk.LEFT, padx=5)
    buttons[symbol] = btn

def debut_de_la_partie():
    global sequence, user_input
    user_input = []
    sequence.append(random.choice(lettre))
    show_sequence()

def show_sequence():
    display.config(text=" ".join(sequence))
    root.after(2000, lambda: display.config(text=""))

# Bouton pour démarrer la séquence
start_button = tk.Button(frame, text="Nouvelle séquence", command=debut_de_la_partie, font=("Old English Text MT", 20),
                         bd=0, fg="white", bg="#8b5a2b", activebackground="#a67c52")
start_button.pack(pady=10)

# Lancer le jeu
root.mainloop()
