import tkinter as tk
import os
import random
from PIL import Image, ImageTk

# Initialisation de la fenêtre
root = tk.Tk()
root.title("Jeu de Séquence Médiéval")

# Taille de la fenêtre (correspond à l'image de fond)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 808
root.geometry(f"{IMAGE_WIDTH}x{IMAGE_HEIGHT}")

# Charger l'image de fond
base_dir = os.path.dirname(os.path.abspath(__file__))
chemin_images = os.path.join(base_dir, "images")
background_image_path = os.path.join(chemin_images, "fond_medieval.jpg")

if os.path.exists(background_image_path):
    bg_img = Image.open(background_image_path)
    bg_img = bg_img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    bg_img_tk = ImageTk.PhotoImage(bg_img)

    # Création du canvas pour l'image de fond
    canvas = tk.Canvas(root, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_img_tk)
else:
    print("❌ Image de fond introuvable !")

# Label de texte
label = tk.Label(root, text="Reproduis la séquence", font=("Old English Text MT", 18), fg="white", bg="#4B2E1D")
label.place(x=410, y=100)

# Affichage de la séquence
display = tk.Label(root, text="", font=("Old English Text MT", 80), fg="white", bg="#4B2E1D")
display.place(x=495, y=150)

# Lettres du jeu
lettres = ['𝖊', '𝖘', '𝖈', '𝖆', '𝖕', '𝖊']

def debut_de_la_partie():
    global sequence, user_input
    user_input = []
    sequence.append(random.choice(lettres))
    show_sequence()

# Fonction pour afficher la séquence
def show_sequence():
    display.config(text=" ".join(sequence))
    root.after(2000, lambda: display.config(text=""))

# Fonction de gestion du clic utilisateur
def user_click(lettre):
    global sequence, user_input
    user_input.append(lettre)
    if user_input == sequence:
        label.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        label.config(text="Perdu ! Réessaye.")
        sequence = []

def reset_game():
    global sequence, user_input
    # Réinitialisation de la séquence avec une lettre aléatoire
    sequence = [random.choice(lettres)]
    user_input = []  # Réinitialiser l'entrée de l'utilisateur
    show_sequence()

lettre_mapping = {
    '𝖊': 'e',
    '𝖘': 's',
    '𝖈': 'c',
    '𝖆': 'a',
    '𝖕': 'p',
}

# Dictionnaire pour stocker les images des boutons
button_images = {}
tk_image_refs = []  # Pour éviter que les images soient supprimées

# Chargement des images des boutons
for symbol in lettres:
    filename = f"wood_button_{lettre_mapping[symbol]}.png"
    image_path = os.path.join(chemin_images, filename)

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((80, 80))
        img_tk = ImageTk.PhotoImage(img)
        button_images[symbol] = img_tk
        tk_image_refs.append(img_tk)  # Stocker la référence pour éviter le garbage collector
    else:
        print(f"❌ Image introuvable pour {symbol}")

# Création des boutons
buttons = {}
x_start = 230  # Position de départ horizontale
y_position = 350  # Position verticale des boutons

for i, lettre in enumerate(lettres):
    btn = tk.Button(
        root,
        text=lettre,
        font=("Old English Text MT", 20),
        command=lambda s=lettre: user_click(s),
        image=button_images.get(lettre),  # Associer la bonne image
        compound="top",
        bd=0,
        fg="white",
        bg="#8b5a2b",
        activebackground="#a67c52"
    )
    btn.place(x=x_start + i * 100, y=y_position)  # Espacement entre les boutons
    buttons[lettre] = btn  # Stocker les boutons

# Liste pour stocker la séquence du jeu
sequence = []
user_input = []

# Charger l'image du bouton "Nouvelle séquence"
nouvelle_image_path = os.path.join(chemin_images, "nouvelle.png")

img_nouvelle_tk = None  # Initialisation de la variable img_nouvelle_tk

if os.path.exists(nouvelle_image_path):
    img_nouvelle = Image.open(nouvelle_image_path)

    # Découper l'image pour ne garder que le bouton en haut à gauche
    bouton_couper = img_nouvelle.crop((110, 170, 1258, 468))  # Ajustez les dimensions de la découpe
    bouton_couper = bouton_couper.resize((150, 75))  # Redimensionner si nécessaire

    # Convertir l'image découpée pour Tkinter
    img_nouvelle_tk = ImageTk.PhotoImage(bouton_couper)
else:
    print("❌ Image nouvelle.png introuvable !")

# Vérifier si l'image a été chargée avant d'ajouter le bouton
if img_nouvelle_tk:
    # Bouton pour démarrer une nouvelle partie avec l'image découpée
    start_button = tk.Button(
        root,
        text="Nouvelle séquence",
        command=lambda: reset_game(),  # Remplacez par la fonction de début de partie
        font=("Old English Text MT", 20),
        bd=0,
        fg="white",
        bg="#8b5a2b",
        activebackground="#a67c52",
        image=img_nouvelle_tk,  # Associer l'image découpée
        compound="top"  # Afficher le texte au-dessus de l'image
    )
    start_button.place(x=400, y=500)  # Positionner le bouton
else:
    print("❌ Impossible de charger l'image pour le bouton")

# Lancer l'application Tkinter
root.mainloop()

