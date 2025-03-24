# mon code

import tkinter as tk
import random

symboles = ['!', '§', '?', 'µ', '£']

sequence = []
user_input = []
buttons = {}

def debut_de_la_partie() :
    global sequence, user_input
    user_input  = []
    sequence.append(random.choice(symboles))
    show_sequence()

def show_sequence() :
    sequence
    display.config(text=" ".join(sequence))
    root.after(3000, lambda: display.config(text=""))

    def user_click(symboles):
        global user_input, sequence
        user_input.append(symboles)
        if user_input == sequence:
            label.config(text="Bravo ! Nouvelle séquence...")
            root.after(3000, debut_de_la_partie)
        elif not sequence[:len(user_input)] == user_input:
            label.config(text="Perdu ! Réessaye.")
            sequence = []


    # Initialisation de l'interface graphique
    root = tk.Tk()
    root.title("Jeu de Séquence")

    label = tk.Label(root, text="Reproduis la séquence", font=("Arial", 14))
    label.pack(pady=10)

    display = tk.Label(root, text="", font=("Arial", 20))
    display.pack(pady=10)

    buttons_frame = tk.Frame(root)
    buttons_frame.pack()

    for symbol in symboles :
        btn = tk.Button(buttons_frame, text=symboles, font=("Arial", 18), command=lambda s=symboles: user_click(s))
        btn.pack(side=tk.LEFT, padx=5)
        buttons[symbol] = btn

    start_button = tk.Button(root, text="Nouvelle séquence", command=debut_de_la_partie)
    start_button.pack(pady=10)

    # Lancer le jeu
    root.mainloop()
