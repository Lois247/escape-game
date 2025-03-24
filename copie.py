import tkinter as tk
import random

SYMBOLS = ['!', '§', '?', 'µ', '£']

# Variables globales
sequence = []  # Séquence générée
user_input = []  # Entrée du joueur
root = None
label = None
display = None
buttons = {}

def start_game():
    global sequence, user_input
    user_input = []  # Réinitialisation de l'entrée du joueur
    sequence.append(random.choice(SYMBOLS))
    show_sequence()

def show_sequence():
    global sequence
    display.config(text=" ".join(sequence))
    root.after(1000, lambda: display.config(text=""))

def user_click(symbol):
    global user_input, sequence
    user_input.append(symbol)
    if user_input == sequence:
        label.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, start_game)
    elif not sequence[:len(user_input)] == user_input:
        label.config(text="Perdu ! Réessaye.")
        sequence = []  # Réinitialisation du jeu

# Initialisation de l'interface graphique
root = tk.Tk()
root.title("Jeu de Séquence")

label = tk.Label(root, text="Reproduis la séquence !", font=("Arial", 14))
label.pack(pady=10)

display = tk.Label(root, text="", font=("Arial", 20))
display.pack(pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack()

for symbol in SYMBOLS:
    btn = tk.Button(buttons_frame, text=symbol, font=("Arial", 18), command=lambda s=symbol: user_click(s))
    btn.pack(side=tk.LEFT, padx=5)
    buttons[symbol] = btn

start_button = tk.Button(root, text="Nouvelle séquence", command=start_game)
start_button.pack(pady=10)

# Lancer le jeu
root.mainloop()
